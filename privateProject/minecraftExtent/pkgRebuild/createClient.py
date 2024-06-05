#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/5/23 下午3:36
# 当前项目名: Python
# 编码模式: utf-8
# 注释: minecraft-protocol\src\createClient.js
# -------------------------<edocsitahw>----------------------------
from client_ import Client as DefaultClientImpl
from version import defaultVersion
import minecraftData.index as minecraft_data
from tcp_dns import export as tcpDns
from warnings import warn
from client import auth, microsoftAuth  # type: ignore
from asyncio import run
from uuid_ import nameToMcOfflineUUID


class GameError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


async def realm_authenticate(client, options):
    pass


async def authenticate(client, options):
    pass

async def authenticate_realms(client, options):
    try:
        await realm_authenticate(client, options)
        await authenticate(client, options)
    except Exception as e:
        client.emit("error", e)

async def authenticate_normal(client, options):
    try:
        await authenticate(client, options)
    except Exception as e:
        client.emit("error", e)


def createClient(options):
    assert options, "options is required"
    assert options["username"], "username is required"

    if not options["version"] and not options["realms"]:
        options["version"] = False

    if options["realms"] and options["auth"] != "minecraft": raise GameError(
        "Currently Realms can only be joined with auth: \"microsoft\"")

    optVersion = v if (v := options["version"]) else defaultVersion

    mcData = minecraft_data.export(optVersion)

    if not mcData:
        raise GameError(
            f"unsupport protocal version: {optVersion}")

    version = mcData.version  # TODO: exports的返回应具有version属性

    options.majorVersion = version.majorVersion

    options.protocolVersion = version.version

    hideErrors = e if (e := options.hideErrors) else False

    Client = c if (c := options.Client) else DefaultClientImpl

    client = Client(False, version.minecraftVersion, options.customPackets, hideErrors)

    tcpDns(client, options)

    if callable(options['auth']):
        options['auth'](client, options)

    else:
        match options['auth']:
            case 'mojang':
                warn(
                    '[deprecated] mojang auth servers no longer accept mojang accounts to login. convert your account.\nhttps://help.minecraft.net/hc/en-us/articles/4403181904525-How-to-Migrate-Your-Mojang-Account-to-a-Microsoft-Account')

                auth(client, options)
            case 'microsoft':
                if options['realms']:
                    run(authenticate_realms(client, options))

                else:
                    run(authenticate_normal(client, options))

            case 'offline':
                pass
            case _:
                client.username = options['username']
                client.uuid = nameToMcOfflineUUID(options['username'])
                options["auth"] = "offline"
                options["connect"](client)

    if options['version'] is False: autoVersion(client, options)
    setProtocol(client, options)
    keepalive(client, options)
    encrypt(client, options)
    play(client, options)
    compress(client, options)
    pluginChannels(client, options)
    versionChecking(client, options)

    return client

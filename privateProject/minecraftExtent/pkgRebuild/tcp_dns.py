#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/5/23 下午4:40
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
import socket
import dns.resolver


def export(client, options):
    # Default options
    options['port'] = options.get('port', 25565)
    options['host'] = options.get('host', 'localhost')

    if 'connect' not in options:
        def connect_func(client):
            # Use stream if provided
            if 'stream' in options:
                client.setSocket(options['stream'])
                client.emit('connect')
                return

            if options['port'] == 25565 and not socket.inet_pton(socket.AF_INET, options['host']) and options['host'] != 'localhost':
                # Try to resolve SRV records for the domain
                try:
                    srv_records = dns.resolver.resolve('_minecraft._tcp.' + options['host'], 'SRV')
                    if srv_records:
                        srv_record = srv_records[0]
                        options['host'] = str(srv_record.target)
                        options['port'] = srv_record.port
                        client.setSocket(socket.create_connection((options['host'], options['port'])))
                except dns.exception.DNSException as e:
                    print("Error resolving domain:", e)
                    # Could not resolve SRV lookup, connect directly
                    client.setSocket(socket.create_connection((options['host'], options['port'])))
            else:
                # Otherwise, just connect using the provided hostname and port
                client.setSocket(socket.create_connection((options['host'], options['port'])))

        options['connect'] = connect_func

    return options



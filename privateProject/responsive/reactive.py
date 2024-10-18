#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/8/27 上午1:37
# 当前项目名: ansiDefine.py
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------

"""
Vue3流程
1. 在编码阶段,开发者将需要响应的数据放入vue提供的如data(), computed()这些钩子中
2. vue会对这些数据进行处理,如将data()中的数据使用ref()或者reactive()包装成响应式数据
,而computed()(或者methods,<template>)中的函数则会被包装成Effect
3. Effect本质上包装了一个函数并且执行前会把自己(this)赋值给全局的记录变量activeEffect,后执行函数,执行完毕后会清除activeEffect
# 需要注意的是,
    1. 情况一: 一个effect调用另一个改变了响应式数据的effect,那么会触发两次effect吗?
        个人觉得effect只会触发直接改变了响应式数据的effect(effect1覆盖了effect2设置的activeEffect)
    2. 情况二: 一个effect调用了一个改变了响应式数据的普通函数,那么怎么收集effect?
        收集effect而不是普通函数,可能也收集不到普通函数
4. 先插入说一下响应式数据,vue3中有两种响应式数据,ref()和reactive()
5. ref包装的数据(基本数据类型),而reactive包装的数据(容器类数据)
6. 这些响应式数据都有getter,setter,和一个dep(dependencies)数组,用来收集effect
7. 当setter(不止,还有Array的push,pop等)被触发时,会调用一个叫trigger的函数
8. trigger接收一个object作为键,然后通过这个键从一个全局WeakMap<object, Map<any, Dep>>类型的全局变量
中获取到对应的dep数组Map<any, Dep>[],如何索引不到就返回了,有就赋给自己的deps属性,然后对dep数组做了一些新操作,之后遍历dep数组,调用
triggerEffects函数,这个函数接收Dep类型Map<ReactiveEffect, number>类型的参数,然后遍历这个参数的键,
即effect,接着对比一dep记录的effect的id和effect的属性中的id是否一致,然后调用effect的trigger属性(其实是方法)
接着设置activeEffect为effect,然后执行包裹的函数,最后清除activeEffect
9. 当getter被触发时,先调用track函数,接收一个类型为object的键和字符串key,从全局变量targetMap中获取类型为Map<any, Dep>的值,
如果该值为空,则创建一个新的Map,然后将该值存入targetMap中,接着获取key对应的Dep,如果该值为空,则创建一个新的Dep,然后将该值存入key对应的Dep中
接着调用trackEffect,接收一个ReactiveEffect类型effect,这个effect就是activeEffect中的effect,然后对比id,如果id的不一致就设置id,接着
根据索引获取Dep为旧Dep,接着对比该dep和接收到的dep是否一致,如果一致就索引自增,不一致就从表中删除该dep,接着就该索引设置新的dep
reactive就只是使用Proxy包装了数据,get中调用了track,set中调用了trigger
10. 最后所有effect,关于该响应式数据包括输入effect(用户输入触发)和渲染effect(数据改变触发)都被收集或触发.
总结:
    * ref: 包装数据, 有get和set方法
    * reactive: 包装容器类数据, 有get和set方法, 还可以用数组方法如push,pop等
    * effect: 包装函数, 调用时会收集依赖, 调用完毕后清除依赖
    * dep: 记录依赖, 触发effect
    * computed: 包装effect, 调用时会收集依赖, 调用完毕后清除依赖
    * activeEffect: 当前正在执行的effect
    * trigger: 触发effect
    * track: 记录依赖
    * targetMap: 全局变量, 用来记录依赖
"""
from typing import Any, Callable
from collections.abc import Collection
from warnings import warn

# -------ref.ts
# RefImpl
# triggerRef


# -------reactivateEffect.ts
# track
# trigger
# getDepFromReactive


# -------reactive.ts
# reactive


# -------effect.ts
# activeEffect
# triggerComputed
# triggerEffects
# triggerEffect
# cleanupDepEffect
# effect


# -------dep.ts
# Dep -> cleanup -> computed


# -------computed.ts
# computed
# ComputedRefImpl
ACTIVE_EFFECT: 'Effect' = None
TARGET_MAP: dict[Any, dict[Any, 'Dep']] = {}
PROXY_MAP: dict[int, Any] = {}


def track(effect: 'Effect', dep: 'Dep'):
    if dep.get(effect) != effect.trackId:
        dep[effect] = effect.trackId

        try:
            oldDep: 'Dep' = effect.deps[effect.idx]
        except IndexError:
            oldDep = None

        if oldDep != dep:
            if oldDep:
                if oldDep.get(effect) != effect.trackId:
                    oldDep.pop(effect, None)
                    if len(oldDep) == 0:
                        oldDep.cleanup()
            effect.deps.append(dep)
        effect.idx += 1


def trigger(dep: 'Dep'):
    """
    更新某个响应式数据的dep中的所有依赖effect.

    :param dep: 响应式数据的dep
    :return:
    """
    for effect in dep:
        if dep.get(effect) == effect.trackId:
            effect()


def trackReac(target: Any, key: str):
    if ACTIVE_EFFECT:
        deps = TARGET_MAP.setdefault(id(target), {})

        def cleanup():
            deps.pop(key, None)

        dep = deps.get(key)
        if not dep:
            dep = Dep(cleanup)
            deps[key] = dep

        track(ACTIVE_EFFECT, dep)


def triggerReac(target: Any, key: str):
    deps = TARGET_MAP.get(id(target))
    if not deps:
        return

    for dep in deps.values():
        if dep:
            trigger(dep)


class Dep(dict):
    def __init__(self, cleanup: Callable[[None], None]):
        super().__init__()
        self.cleanup = cleanup


class Ref:
    def __init__(self, value: Any):
        self._value = value
        self._dep = None

    def _cleanup(self):
        self._dep = None

    @property
    def value(self):
        if ACTIVE_EFFECT:
            if not self._dep:
                self._dep = Dep(lambda: self._cleanup())
            track(ACTIVE_EFFECT, self._dep)
        return self._value

    @value.setter
    def value(self, value: Any):
        # if hanChangee
        self._value = value
        # is reactive?
        if self._dep:
            trigger(self._dep)


class Reactive:
    def __new__(cls, target: Any):
        if not isinstance(target, Collection):
            warn("Reactive only accept collection type, use Ref instead")
            return Ref(target)
        elif self := PROXY_MAP.get(id(target)):
            return self
        else:
            return super().__new__(cls)

    def __init__(self, target: Any):
        self.__dict__['_target'] = target
        self._target = target
        PROXY_MAP[id(target)] = self

    def __getitem__(self, item):
        res = self._target[item]

        if not isinstance(res, str) and isinstance(res, Collection):
            res = Reactive(res)
        elif isinstance(res, Ref):
            res = res.value
        else:
            res = Ref(res)

        trackReac(self._target, item)
        return res

    def __setitem__(self, key: Any, value: Any):
        self._target[key] = value
        triggerReac(self._target, key)


class Effect:
    def __init__(self, fn: Callable[[], Any]):
        self._fn = fn
        self.deps = []
        self.idx = self.trackId = 0

    def __call__(self):
        global ACTIVE_EFFECT
        try:
            ACTIVE_EFFECT = self
            self.trackId += 1
            self.idx = 0
            return self._fn()
        except Exception as e:
            raise e


if __name__ == '__main__':
    value = Ref(1)

    @Effect
    def inputValue(val: Any) -> Any:
        try:
            value.value = val
        except Exception as e:
            return 1
        return 0

    @Effect
    def renderValue(val: Any) -> Any:
        print(f"Value changed to {value.value}")
        return 0

    inputValue()
    renderValue()

    value.value = 3
    value.value = 4

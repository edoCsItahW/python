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
                    if not len(oldDep):
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

    def inputValue(val: Any) -> Any:
        try:
            value.value = val

        except Exception as e:
            return 1

        return 0

    def renderValue(val: Any) -> Any:
        print(f"Value changed to {value.value}")

        return 0

    effect = Effect(lambda: inputValue(input("Enter a value: ")))
    effect()

    effect = Effect(lambda: renderValue(value.value))
    effect()

    value.value = 3
    value.value = 4

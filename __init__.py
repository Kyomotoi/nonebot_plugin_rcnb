#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/12/06 14:04:06
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

from nonebot.plugin import on_command
from nonebot.typing import Bot, Event

from .data_source import RCNB

rcnb = RCNB()

rcnbEncode = on_command('RC一下', aliases={'rc一下', '啊西一下', '阿西一下'})


@rcnbEncode.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    msg = str(event.message).strip()

    if msg:
        state['msg'] = msg


@rcnbEncode.got('msg', prompt='请告诉咱需要RC一下的字符~！')
async def _(bot: Bot, event: Event, state: dict) -> None:
    msg = state['msg']
    await rcnbEncode.finish(rcnb._encode(msg))


rcnbDecode = on_command('一下RC', aliases={'一下rc', '一下啊西', '一下阿西'})


@rcnbDecode.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    msg = str(event.message).strip()

    if msg:
        state['msg'] = msg


@rcnbDecode.got('msg', prompt='请告诉咱需要一下RC的字符~！')
async def _(bot: Bot, event: Event, state: dict) -> None:
    msg = state['msg']
    await rcnbDecode.finish(rcnb._decode(msg))

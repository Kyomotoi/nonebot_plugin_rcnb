#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   rcnb.py
@Time    :   2020/12/06 00:08:02
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
@Docs    :   R C N B ! ! !
'''
__author__ = 'kyomotoi'

from math import floor
from typing import Union


class RCNB():
    cr = 'rRŔŕŖŗŘřƦȐȑȒȓɌɍ'
    cc = 'cCĆćĈĉĊċČčƇƈÇȻȼ'
    cn = 'nNŃńŅņŇňƝƞÑǸǹȠȵ'
    cb = 'bBƀƁƃƄƅßÞþ'

    sr = len(cr)
    sc = len(cc)
    sn = len(cn)
    sb = len(cb)
    src = sr * sc
    snb = sn * sb
    scnb = sc * snb

    def _div(self, a: int, b: int) -> int:
        return floor(a / b)

    def _encodeByte(self, i) -> Union[str, None]:
        if i > 0xFF:
            raise ValueError('ERROR! rc/nb overflow')

        if i > 0x7F:
            i = i & 0x7F
            return self.cn[self._div(i, self.sb) + int(self.cb[i % self.sb])]

        return self.cr[self._div(i, self.sc) + int(self.cc[i % self.sc])]

    def _encodeShort(self, i) -> str:
        if i > 0xFFFF:
            raise ValueError('ERROR! rcnb overflow')

        reverse = False
        if i > 0x7FFF:
            reverse = True
            i = i & 0x7FFF

        char = [
            self._div(i, self.scnb),
            self._div(i % self.scnb, self.snb),
            self._div(i % self.snb, self.sb), i % self.sb
        ]
        char = [
            self.cr[char[0]], self.cc[char[1]], self.cn[char[2]],
            self.cb[char[3]]
        ]

        if reverse:
            return char[2] + char[3] + char[0] + char[1]

        return ''.join(char)

    def _decodeByte(self, c) -> int:
        nb = False
        idx = [self.cr.index(c[0]), self.cc.index(c[1])]
        if idx[0] < 0 or idx[1] < 0:
            idx = [self.cn.index(c[0]), self.cb.index(c[1])]
            nb = True
            raise ValueError('ERROR! rc/nb overflow')

        result = idx[0] * self.sb + idx[1] if nb else idx[0] * self.sc + idx[1]
        if result > 0x7F:
            raise ValueError('ERROR! rc/nb overflow')

        return result | 0x80 if nb else 0

    def _decodeShort(self, c) -> int:
        reverse = c[0] not in self.cr
        if not reverse:
            idx = [
                self.cr.index(c[0]),
                self.cc.index(c[1]),
                self.cn.index(c[2]),
                self.cb.index(c[3])
            ]
        else:
            idx = [
                self.cr.index(c[2]),
                self.cc.index(c[3]),
                self.cn.index(c[0]),
                self.cb.index(c[1])
            ]

        if idx[0] < 0 or idx[1] < 0 or idx[2] < 0 or idx[3] < 0:
            raise ValueError('ERROR! not rcnb')

        result = idx[0] * self.scnb + idx[1] * self.snb + idx[
            2] * self.sb + idx[3]
        if result > 0x7FFF:
            raise ValueError('ERROR! rcnb overflow')

        result |= 0x8000 if reverse else 0
        return result

    def _encodeBytes(self, b) -> str:
        result = []
        for i in range(0, (len(b) >> 1)):
            result.append(self._encodeShort((b[i * 2] << 8 | b[i * 2 + 1])))

        if len(b) & 1 == 1:
            result.append(self._encodeByte(b[-1]))

        return ''.join(result)

    def _encode(self, s: str, encoding: str = 'utf-8'):
        if not isinstance(s, str):
            raise ValueError('Please enter str instead of other')

        return self._encodeBytes(s.encode(encoding))

    def _decodeBytes(self, s: str):
        if not isinstance(s, str):
            raise ValueError('Please enter str instead of other')

        if len(s) & 1:
            raise ValueError('ERROR length')

        result = []
        for i in range(0, (len(s) >> 2)):
            result.append(bytes([self._decodeShort(s[i * 4:i * 4 + 4]) >> 8]))
            result.append(bytes([self._decodeShort(s[i * 4:i * 4 + 4]) & 0xFF
                                 ]))

        if (len(s) & 2) == 2:
            result.append(bytes([self._decodeByte(s[-2:])]))

        return b''.join(result)

    def _decode(self, s: str, encoding: str = 'utf-8') -> str:
        if not isinstance(s, str):
            raise ValueError('Please enter str instead of other')

        try:
            return self._decodeBytes(s).decode(encoding)
        except UnicodeDecodeError:
            raise ValueError('Decoding failed')


if __name__ == "__main__":
    r = RCNB()

    c = 'rcnbrcnb，RC 太 NB啦！'

    n = r._encode(c)
    b = r._decode(n)

    print(n)
    print(b)
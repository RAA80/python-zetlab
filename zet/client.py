#! /usr/bin/env python3

"""Реализация класса для управления АЦП/ЦАП фирмы ZetLab."""

from __future__ import annotations

import contextlib
import itertools
import os.path
from ctypes import (POINTER, WINFUNCTYPE, _Pointer, byref, c_char, c_char_p,
                    c_double, c_long, c_ulong, c_void_p, cdll, pointer, sizeof)
from enum import IntEnum
from functools import partial
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from _ctypes import _CData, _PyCFuncPtrType


_lib = cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), "libs", "Zadc.dll"))


class ZetError(Exception):
    pass


class Z_DEVICE(IntEnum):
    """Определения типов плат/модулей."""

    ADC_16_200 = 0      # АЦП устройства ADC 16/200
    APC_216 = 1         # АЦП устройства APC 216
    ADC_16_500 = 2      # АЦП устройства ADC 16/500
    ADC_16_500P = 3     # АЦП устройства ADC 16/500P
    ADC_816 = 4         # АЦП устройства ADC 816
    ADC_1002 = 5        # АЦП устройства ADC 1002
    ADC_216_USB = 6     # АЦП устройства ADC 216 USB
    ADC_24 = 7          # АЦП устройства ADC 24
    ADC_1432 = 8        # АЦП устройства ADC 1432
    ACPB_USB = 9        # АЦП устройства ACPB USB
    ZET210 = 10         # АЦП устройства ZET210
    PD14_USB = 11       # АЦП устройства PD14 USB
    ZET110 = 12         # АЦП устройства ZET110
    ZET302 = 13         # АЦП устройства ZET302
    ZET017 = 14         # АЦП устройства ZET017
    ZET017_U2 = 15      # АЦП устройства ZET017-U2, ZET019-U2
    ZET220 = 16         # АЦП устройства ZET220
    ZET230 = 17         # АЦП устройства ZET230
    ZET240 = 18         # АЦП устройства ZET240
    ZET048 = 19         # АЦП устройства ZET240, ZET048


class IDaqZDevice(c_void_p):
    def __init__(self, device: int, dsp: int) -> None:
        self.device = device
        self.dsp = dsp
        self.name = ""

    _functions_ = {
        "ZOpen": WINFUNCTYPE(c_long, c_long, c_long),
        "ZClose": WINFUNCTYPE(c_long, c_long, c_long),
        "ZResetDSP": WINFUNCTYPE(c_long, c_long, c_long),
        "ZInitDSP": WINFUNCTYPE(c_long, c_long, c_long, c_char_p),
        "ZGetSerialNumberDSP": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetNameDevice": WINFUNCTYPE(c_long, c_long, c_long, c_char_p, c_long),
        "ZGetVersion": WINFUNCTYPE(c_long, c_long, c_long, c_char_p, c_char_p, c_char_p),
        "ZGetTypeConnection": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetError": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetModify": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetFlag": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_ulong)),
        "ZGetEnableExtFreq": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZSetEnableExtFreq": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZGetEnableExtStart": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZSetEnableExtStart": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZGetQuantityChannelDigPort": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetDigOutEnable": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_ulong)),
        "ZSetDigOutEnable": WINFUNCTYPE(c_long, c_long, c_long, c_ulong),
        "ZGetDigInput": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_ulong)),
        "ZGetDigOutput": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_ulong)),
        "ZSetDigOutput": WINFUNCTYPE(c_long, c_long, c_long, c_ulong),
        "ZGetDigitalMode": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZSetDigitalMode": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZGetMasterSynchr": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZSetMasterSynchr": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZFindPWM": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetEnableADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetEnableDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZSetTypeADC": WINFUNCTYPE(c_long, c_long, c_long),
        "ZSetTypeDAC": WINFUNCTYPE(c_long, c_long, c_long),
        "ZGetStartADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetStartDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZStartADC": WINFUNCTYPE(c_long, c_long, c_long),
        "ZStartDAC": WINFUNCTYPE(c_long, c_long, c_long),
        "ZStopADC": WINFUNCTYPE(c_long, c_long, c_long),
        "ZStopDAC": WINFUNCTYPE(c_long, c_long, c_long),
        "ZGetQuantityChannelADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetQuantityChannelDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetDigitalResolutionADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_double)),
        "ZGetDigitalResolutionDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_double)),
        "ZGetDigitalResolChanADC": WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        "ZGetDigitalResolChanDAC": WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        "ZGetBitsADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetBitsDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetWordsADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetWordsDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetFreqADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_double)),
        "ZGetFreqDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_double)),
        "ZGetListFreqADC": WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        "ZGetListFreqDAC": WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        "ZSetNextFreqADC": WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        "ZSetNextFreqDAC": WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        "ZSetFreqADC": WINFUNCTYPE(c_long, c_long, c_long, c_double, POINTER(c_double)),
        "ZSetFreqDAC": WINFUNCTYPE(c_long, c_long, c_long, c_double, POINTER(c_double)),
        "ZGetExtFreqADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_double)),
        "ZGetExtFreqDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_double)),
        "ZSetExtFreqADC": WINFUNCTYPE(c_long, c_long, c_long, c_double),
        "ZSetExtFreqDAC": WINFUNCTYPE(c_long, c_long, c_long, c_double),
        "ZGetEnableExtFreqADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetEnableExtFreqDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZSetEnableExtFreqADC": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZSetEnableExtFreqDAC": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZGetEnableExtStartADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetEnableExtStartDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZSetEnableExtStartADC": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZSetEnableExtStartDAC": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZGetInterruptADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetInterruptDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetMaxInterruptADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetMaxInterruptDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZSetInterruptADC": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZSetInterruptDAC": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZGetSizePacketADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetSizePacketDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetMaxSizePacketADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetMaxSizePacketDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZSetSizePacketADC": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZSetSizePacketDAC": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZGetQuantityPacketsADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetQuantityPacketsDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetMaxQuantityPacketsADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetMaxQuantityPacketsDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZSetQuantityPacketsADC": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZSetQuantityPacketsDAC": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZSetCycleSampleADC": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZSetCycleSampleDAC": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZSetBufferSizeADC": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZSetBufferSizeDAC": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZGetBufferADC": WINFUNCTYPE(c_long, c_long, c_long, c_void_p, POINTER(c_long)),
        "ZGetBufferDAC": WINFUNCTYPE(c_long, c_long, c_long, c_void_p, POINTER(c_long)),
        "ZRemBufferADC": WINFUNCTYPE(c_long, c_long, c_long, c_void_p),
        "ZRemBufferDAC": WINFUNCTYPE(c_long, c_long, c_long, c_void_p),
        "ZGetPointerADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetPointerDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetNumberInputADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetNumberOutputDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetInputADC": WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_long)),
        "ZGetOutputDAC": WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_long)),
        "ZSetInputADC": WINFUNCTYPE(c_long, c_long, c_long, c_long, c_long),
        "ZSetOutputDAC": WINFUNCTYPE(c_long, c_long, c_long, c_long, c_long),
        "ZGetLastDataADC": WINFUNCTYPE(c_long, c_long, c_long, c_long, c_void_p, c_long),
        "ZGetAmplifyADC": WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        "ZGetListAmplifyADC": WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        "ZSetNextAmplifyADC": WINFUNCTYPE(c_long, c_long, c_long, c_long, c_long, POINTER(c_double)),
        "ZSetAmplifyADC": WINFUNCTYPE(c_long, c_long, c_long, c_long, c_double, POINTER(c_double)),
        "ZGetPreAmplifyADC": WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        "ZGetListPreAmplifyADC": WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        "ZSetNextPreAmplifyADC": WINFUNCTYPE(c_long, c_long, c_long, c_long, c_long, POINTER(c_double)),
        "ZSetPreAmplifyADC": WINFUNCTYPE(c_long, c_long, c_long, c_long, c_double, POINTER(c_double)),
        "ZFindHCPADC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetHCPADC": WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_long)),
        "ZSetHCPADC": WINFUNCTYPE(c_long, c_long, c_long, c_long, c_long),
        "ZGetInputDiffADC": WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_long)),
        "ZSetInputDiffADC": WINFUNCTYPE(c_long, c_long, c_long, c_long, c_long),
        "ZSetExtCycleDAC": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZFindSoftAtten": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetAttenDAC": WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        "ZSetAttenDAC": WINFUNCTYPE(c_long, c_long, c_long, c_long, c_double, POINTER(c_double)),
        "ZGetMaxSizeBufferDSPDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZGetSizeBufferDSPDAC": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        "ZSetSizeBufferDSPDAC": WINFUNCTYPE(c_long, c_long, c_long, c_long),

        "ZTestCode": WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long), POINTER(c_long), POINTER(c_long)),
        "ZSetBitDigOutEnable": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZSetBitMaskDigOutEnable": WINFUNCTYPE(c_long, c_long, c_long, c_ulong),
        "ZClrBitDigOutEnable": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZClrBitMaskDigOutEnable": WINFUNCTYPE(c_long, c_long, c_long, c_ulong),
        "ZSetBitDigOutput": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZSetBitMaskDigOutput": WINFUNCTYPE(c_long, c_long, c_long, c_ulong),
        "ZClrBitDigOutput": WINFUNCTYPE(c_long, c_long, c_long, c_long),
        "ZClrBitMaskDigOutput": WINFUNCTYPE(c_long, c_long, c_long, c_ulong),
        "ZStartPWM": WINFUNCTYPE(c_long, c_long, c_long, c_long, c_long, c_long),
        "ZStopPWM": WINFUNCTYPE(c_long, c_long, c_long, c_long, c_long, c_long),
        "ZSetFreqPWM": WINFUNCTYPE(c_long, c_long, c_long, c_long, c_long),
        "ZSetOnDutyPWM": WINFUNCTYPE(c_long, c_long, c_long, c_long, c_long, c_long, c_long, c_long),
        "ZRegulatorPWM": WINFUNCTYPE(c_long, c_long, c_long, c_void_p, POINTER(c_long)),
    }

    def __call__(self, prototype: _PyCFuncPtrType, *arguments: tuple[_CData, ...]) -> bool:
        if ret := prototype((self.name, _lib))(*(self.device, self.dsp, *arguments)):
            msg = f"{self.name} error {ret:04X}"
            raise ZetError(msg)

        return True

    def __getattr__(self, name: str) -> Callable[..., bool]:
        self.name = name
        return partial(self.__call__, self._functions_[name])


class ZET:
    """Python wrapper for Zadc library."""

    def __init__(self, device: int, dsp: int) -> None:
        """Инициализация класса клиента с указанными параметрами."""

        self._zdev = IDaqZDevice(device, dsp)

    def __enter__(self) -> ZET:
        """Входной блок контекстного менеджера."""

        self.ZOpen()
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        """Выходной блок контекстного менеджера."""

        self.ZClose()

# Подключение к драйверу и отключение

    def ZOpen(self) -> bool:
        """Подключиться к драйверу."""

        return self._zdev.ZOpen()

    def ZClose(self) -> bool:
        """Отключиться от драйвера."""

        return self._zdev.ZClose()

# Сброс и инициализация

    def ZInitDSP(self, filename: str = "") -> bool:
        """Проинициализировать сигнальный процессор."""

        return self._zdev.ZInitDSP(filename.encode("ascii"))

    def ZResetDSP(self) -> bool:
        """Сброс и останов сигнальных процессоров (влияет на все DSP одного
        устройства).
        """

        return self._zdev.ZResetDSP()

# Сервисные функции

    def ZGetVersion(self) -> dict[str, bytes]:
        """Опрос версии программ и драйвера."""

        dsp = (c_char * 100)()
        drv = (c_char * 100)()
        lib = (c_char * 100)()

        self._zdev.ZGetVersion(dsp, drv, lib)
        return {"dsp": dsp.value,
                "drv": drv.value,
                "lib": lib.value}

    def ZGetError(self) -> int:
        """Прочитать код ошибки."""

        error = c_long()

        self._zdev.ZGetError(byref(error))
        return error.value

    def ZGetModify(self) -> int:
        """Определить кол-во изменений параметров с момента загрузки."""

        modify = c_long()

        self._zdev.ZGetModify(byref(modify))
        return modify.value

# Установка режима работы сигнального процессора

    def ZSetTypeADC(self) -> bool:
        """Установить сигнальный процессор в режим АЦП."""

        return self._zdev.ZSetTypeADC()

    def ZSetTypeDAC(self) -> bool:
        """Установить сигнальный процессор в режим ЦАП."""

        return self._zdev.ZSetTypeDAC()

# Опрос основных характеристик модулей АЦП и ЦАП

    def ZGetEnableADC(self) -> int:
        """Опрос возможности работы сигнального процессора с модулем АЦП."""

        enable = c_long()

        self._zdev.ZGetEnableADC(byref(enable))
        return enable.value

    def ZGetEnableDAC(self) -> int:
        """Опрос возможности работы сигнального процессора с модулем ЦАП."""

        enable = c_long()

        self._zdev.ZGetEnableDAC(byref(enable))
        return enable.value

    def ZGetQuantityChannelADC(self) -> int:
        """Опрос максимального количества каналов модуля АЦП."""

        quantity = c_long()

        self._zdev.ZGetQuantityChannelADC(byref(quantity))
        return quantity.value

    def ZGetQuantityChannelDAC(self) -> int:
        """Опрос максимального количества каналов модуля ЦАП."""

        quantity = c_long()

        self._zdev.ZGetQuantityChannelDAC(byref(quantity))
        return quantity.value

    def ZGetDigitalResolutionADC(self) -> float:
        """Опрос веса младшего разряда АЦП (устаревшая функция)."""

        resolution = c_double()

        self._zdev.ZGetDigitalResolutionADC(byref(resolution))
        return resolution.value

    def ZGetDigitalResolutionDAC(self) -> float:
        """Опрос веса младшего разряда ЦАП (устаревшая функция)."""

        resolution = c_double()

        self._zdev.ZGetDigitalResolutionDAC(byref(resolution))
        return resolution.value

    def ZGetDigitalResolChanADC(self, channel: int) -> float:
        """Прочитать откалиброванный поканально вес младшего разряда АЦП."""

        resolution = c_double()

        self._zdev.ZGetDigitalResolChanADC(c_long(channel), byref(resolution))
        return resolution.value

    def ZGetDigitalResolChanDAC(self, channel: int) -> float:
        """Прочитать откалиброванный поканально вес младшего разряда ЦАП."""

        resolution = c_double()

        self._zdev.ZGetDigitalResolChanDAC(c_long(channel), byref(resolution))
        return resolution.value

    def ZGetBitsADC(self) -> int:
        """Опрос количества двоичных разрядов АЦП."""

        nbits = c_long()

        self._zdev.ZGetBitsADC(byref(nbits))
        return nbits.value

    def ZGetBitsDAC(self) -> int:
        """Опрос количества двоичных разрядов ЦАП."""

        nbits = c_long()

        self._zdev.ZGetBitsDAC(byref(nbits))
        return nbits.value

    def ZGetWordsADC(self) -> int:
        """Опрос размера каждого отсчета АЦП в 16-разрядных словах."""

        nwords = c_long()

        self._zdev.ZGetWordsADC(byref(nwords))
        return nwords.value

    def ZGetWordsDAC(self) -> int:
        """Опрос размера каждого отсчета ЦАП в 16-разрядных словах."""

        nwords = c_long()

        self._zdev.ZGetWordsDAC(byref(nwords))
        return nwords.value

# Установка частоты дискретизации и режима синхронизации АЦП/ЦАП

    def ZGetListFreqADC(self) -> tuple[float, ...]:
        """Получение списка возможных частот дискретизации АЦП."""

        freq = c_double()
        freq_list = []

        with contextlib.suppress(Exception):
            for i in itertools.count():
                self._zdev.ZGetListFreqADC(c_long(i), byref(freq))
                freq_list.append(freq.value)

        return tuple(freq_list)

    def ZGetListFreqDAC(self) -> tuple[float, ...]:
        """Получение списка возможных частот дискретизации ЦАП."""

        freq = c_double()
        freq_list = []

        with contextlib.suppress(Exception):
            for i in itertools.count():
                self._zdev.ZGetListFreqDAC(c_long(i), byref(freq))
                freq_list.append(freq.value)

        return tuple(freq_list)

    def ZSetNextFreqADC(self, next: int) -> float:
        """Установить следующую из списка частоту дискретизации АЦП."""

        freq = c_double()

        self._zdev.ZSetNextFreqADC(c_long(next), byref(freq))
        return freq.value

    def ZSetNextFreqDAC(self, next: int) -> float:
        """Установить следующую из списка частоту дискретизации ЦАП."""

        freq = c_double()

        self._zdev.ZSetNextFreqDAC(c_long(next), byref(freq))
        return freq.value

    def ZGetFreqADC(self) -> float:
        """Опрос текущей частоты дискретизации АЦП."""

        freq = c_double()

        self._zdev.ZGetFreqADC(byref(freq))
        return freq.value

    def ZGetFreqDAC(self) -> float:
        """Опрос текущей частоты дискретизации ЦАП."""

        freq = c_double()

        self._zdev.ZGetFreqDAC(byref(freq))
        return freq.value

    def ZSetFreqADC(self, freq: float) -> float:
        """Установка частоты дискретизации АЦП."""

        freq_out = c_double()

        self._zdev.ZSetFreqADC(c_double(freq), byref(freq_out))
        return freq_out.value

    def ZSetFreqDAC(self, freq: float) -> float:
        """Установка частоты дискретизации ЦАП."""

        freq_out = c_double()

        self._zdev.ZSetFreqDAC(c_double(freq), byref(freq_out))
        return freq_out.value

    def ZGetExtFreqADC(self) -> float:
        """Опрос текущей опорной частоты АЦП."""

        freq = c_double()

        self._zdev.ZGetExtFreqADC(byref(freq))
        return freq.value

    def ZGetExtFreqDAC(self) -> float:
        """Опрос текущей опорной частоты ЦАП."""

        freq = c_double()

        self._zdev.ZGetExtFreqDAC(byref(freq))
        return freq.value

    def ZSetExtFreqADC(self, freq: float) -> bool:
        """Установка значения внешней опорной частоты АЦП."""

        return self._zdev.ZSetExtFreqADC(c_double(freq))

    def ZSetExtFreqDAC(self, freq: float) -> bool:
        """Установка значения внешней опорной частоты ЦАП."""

        return self._zdev.ZSetExtFreqDAC(c_double(freq))

    def ZGetEnableExtFreq(self) -> int:
        """Прочитать статус синхронизации по внешней частоте (устаревшая функция)."""

        enable = c_long()

        self._zdev.ZGetEnableExtFreq(byref(enable))
        return enable.value

    def ZSetEnableExtFreq(self, enable: int) -> bool:
        """Вкл./выкл. синхронизации по внешней частоте (устаревшая функция)."""

        return self._zdev.ZSetEnableExtFreq(c_long(enable))

    def ZGetEnableExtStart(self) -> int:
        """Прочитать статус внешнего запуска (устаревшая функция)."""

        enable = c_long()

        self._zdev.ZGetEnableExtStart(byref(enable))
        return enable.value

    def ZSetEnableExtStart(self, enable: int) -> bool:
        """Вкл./выкл. внешнего запуска (устаревшая функция)."""

        return self._zdev.ZSetEnableExtStart(c_long(enable))

# Управление каналами ввода (вывода) АЦП/ЦАП

    def ZGetNumberInputADC(self) -> int:
        """Опрос количества включенных каналов АЦП."""

        channel = c_long()

        self._zdev.ZGetNumberInputADC(byref(channel))
        return channel.value

    def ZGetNumberOutputDAC(self) -> int:
        """Опрос количества включенных каналов ЦАП."""

        channel = c_long()

        self._zdev.ZGetNumberOutputDAC(byref(channel))
        return channel.value

    def ZGetInputADC(self, channel: int) -> int:
        """Опрос включен ли заданный канал АЦП."""

        enable = c_long()

        self._zdev.ZGetInputADC(c_long(channel), byref(enable))
        return enable.value

    def ZGetOutputDAC(self, channel: int) -> int:
        """Опрос включен ли заданный канал ЦАП."""

        enable = c_long()

        self._zdev.ZGetOutputDAC(c_long(channel), byref(enable))
        return enable.value

    def ZSetInputADC(self, channel: int, enable: int) -> bool:
        """Включить/выключить заданный канал АЦП."""

        return self._zdev.ZSetInputADC(c_long(channel), c_long(enable))

    def ZSetOutputDAC(self, channel: int, enable: int) -> bool:
        """Включить/выключить заданный канал ЦАП."""

        return self._zdev.ZSetOutputDAC(c_long(channel), c_long(enable))

    def ZGetInputDiffADC(self, channel: int) -> int:
        """Опрос дифференциального режима заданного канала для ввода АЦП."""

        enable = c_long()

        self._zdev.ZGetInputDiffADC(c_long(channel), byref(enable))
        return enable.value

    def ZSetInputDiffADC(self, channel: int, enable: int) -> bool:
        """Установить-сбросить заданный канал для ввода в дифференциальный
        режим АЦП.
        """

        return self._zdev.ZSetInputDiffADC(c_long(channel), c_long(enable))

# Управление коэффициентами усиления АЦП

    def ZGetListAmplifyADC(self) -> tuple[float, ...]:
        """Получение списка возможных коэффициентов усиления АЦП."""

        amplify = c_double()
        amplify_list = []

        with contextlib.suppress(Exception):
            for i in itertools.count():
                self._zdev.ZGetListAmplifyADC(c_long(i), byref(amplify))
                amplify_list.append(amplify.value)

        return tuple(amplify_list)

    def ZSetNextAmplifyADC(self, channel: int, next: int) -> float:
        """Установка большего или меньшего коэффициента усиления из списка
        выбранного канала АЦП.
        """

        amplify = c_double()

        self._zdev.ZSetNextAmplifyADC(c_long(channel), c_long(next), byref(amplify))
        return amplify.value

    def ZGetAmplifyADC(self, channel: int) -> float:
        """Опрос коэффициента усиления выбранного канала АЦП."""

        amplify = c_double()

        self._zdev.ZGetAmplifyADC(c_long(channel), byref(amplify))
        return amplify.value

    def ZSetAmplifyADC(self, channel: int, amplify: float) -> float:
        """Установка коэффициента усиления выбранного канала АЦП."""

        amplify_out = c_double()

        self._zdev.ZSetAmplifyADC(c_long(channel), c_double(amplify), byref(amplify_out))
        return amplify_out.value

# Управление коэффициентами усиления ПУ 8/10

    def ZGetListPreAmplifyADC(self) -> tuple[float, ...]:
        """Получение списка возможных коэффициентов усиления предварительного
        усилителя.
        """

        amplify = c_double()
        amplify_list = []

        with contextlib.suppress(Exception):
            for i in itertools.count():
                self._zdev.ZGetListPreAmplifyADC(c_long(i), byref(amplify))
                amplify_list.append(amplify.value)

        return tuple(amplify_list)

    def ZSetNextPreAmplifyADC(self, channel: int, next: int) -> float:
        """Установка большего или меньшего коэффициента усиления из списка
        предварительного усилителя.
        """

        amplify = c_double()

        self._zdev.ZSetNextPreAmplifyADC(c_long(channel), c_long(next), byref(amplify))
        return amplify.value

    def ZSetPreAmplifyADC(self, channel: int, amplify: float) -> float:
        """Установка коэффициента усиления предварительного усилителя выбранного
        канала.
        """

        amplify_out = c_double()

        self._zdev.ZSetPreAmplifyADC(c_long(channel), c_double(amplify), byref(amplify_out))
        return amplify_out.value

    def ZGetPreAmplifyADC(self, channel: int) -> float:
        """Опрос коэффициента усиления предварительного усилителя выбранного
        канала.
        """

        amplify = c_double()

        self._zdev.ZGetPreAmplifyADC(c_long(channel), byref(amplify))
        return amplify.value

# Управление коэффициентами ослабления аттенюатора ЦАП

    def ZGetAttenDAC(self, channel: int) -> float:
        """Опрос коэффициента ослабления аттенюатора выбранного канала."""

        reduction = c_double()

        self._zdev.ZGetAttenDAC(c_long(channel), byref(reduction))
        return reduction.value

    def ZSetAttenDAC(self, channel: int, reduction: float) -> float:
        """Установка коэффициента ослабления аттенюатора выбранного канала."""

        reduction_out = c_double()

        self._zdev.ZSetAttenDAC(c_long(channel), c_double(reduction), byref(reduction_out))
        return reduction_out.value

# Управление процессом перекачки данных

    def ZSetExtCycleDAC(self, enable: int) -> bool:
        """Установка режима внешней подкачки данных или внутренней генерации
        сигналов.
        """

        return self._zdev.ZSetExtCycleDAC(c_long(enable))

    def ZGetInterruptADC(self) -> int:
        """Опрос размера буфера для перекачки данных АЦП."""

        size = c_long()

        self._zdev.ZGetInterruptADC(byref(size))
        return size.value

    def ZGetInterruptDAC(self) -> int:
        """Опрос размера буфера для перекачки данных ЦАП."""

        size = c_long()

        self._zdev.ZGetInterruptDAC(byref(size))
        return size.value

    def ZGetMaxInterruptADC(self) -> int:
        """Опрос максимального размера буфера для перекачки данных АЦП."""

        size = c_long()

        self._zdev.ZGetMaxInterruptADC(byref(size))
        return size.value

    def ZGetMaxInterruptDAC(self) -> int:
        """Опрос максимального размера буфера для перекачки данных ЦАП."""

        size = c_long()

        self._zdev.ZGetMaxInterruptDAC(byref(size))
        return size.value

    def ZSetInterruptADC(self, size: int) -> bool:
        """Установка размера буфера для перекачки данных АЦП."""

        return self._zdev.ZSetInterruptADC(c_long(size))

    def ZSetInterruptDAC(self, size: int) -> bool:
        """Установка размера буфера для перекачки данных ЦАП."""

        return self._zdev.ZSetInterruptDAC(c_long(size))

    def ZSetBufferSizeADC(self, size: int) -> bool:
        """Задать размер буфера АЦП в ОЗУ ПК."""

        return self._zdev.ZSetBufferSizeADC(c_long(size))

    def ZSetBufferSizeDAC(self, size: int) -> bool:
        """Задать размер буфера ЦАП в ОЗУ ПК."""

        return self._zdev.ZSetBufferSizeDAC(c_long(size))

    def ZGetBufferADC(self) -> tuple[_Pointer[c_long], int]:
        """Запросить буфер в ОЗУ ПК для АЦП."""

        buff_ptr = pointer(c_long())
        size = c_long()

        self._zdev.ZGetBufferADC(byref(buff_ptr), byref(size))
        return buff_ptr, size.value

    def ZGetBufferDAC(self) -> tuple[_Pointer[c_long], int]:
        """Запросить буфер в ОЗУ ПК для ЦАП."""

        buff_ptr = pointer(c_long())
        size = c_long()

        self._zdev.ZGetBufferDAC(byref(buff_ptr), byref(size))
        return buff_ptr, size.value

    def ZRemBufferADC(self, buff_ptr: _Pointer[c_long]) -> bool:
        """Освободить буфер в ОЗУ ПК для АЦП."""

        return self._zdev.ZRemBufferADC(byref(buff_ptr))

    def ZRemBufferDAC(self, buff_ptr: _Pointer[c_long]) -> bool:
        """Освободить буфер в ОЗУ ПК для ЦАП."""

        return self._zdev.ZRemBufferDAC(byref(buff_ptr))

    def ZSetCycleSampleADC(self, enable: int) -> bool:
        """Установка циклического или одноразового накопления АЦП."""

        return self._zdev.ZSetCycleSampleADC(c_long(enable))

    def ZSetCycleSampleDAC(self, enable: int) -> bool:
        """Установка циклического или одноразового накопления ЦАП."""

        return self._zdev.ZSetCycleSampleDAC(c_long(enable))

    def ZGetLastDataADC(self, channel: int, size: int) -> c_void_p:
        """Пересылка последних накопленных данных АЦП."""

        buff_ptr = c_void_p()

        self._zdev.ZGetLastDataADC(c_long(channel), buff_ptr, c_long(size))
        return buff_ptr

    def ZGetPointerADC(self) -> int:
        """Чтение указателя буфера в ОЗУ ПК для АЦП."""

        ptr = c_long()

        self._zdev.ZGetPointerADC(byref(ptr))
        return ptr.value

    def ZGetPointerDAC(self) -> int:
        """Чтение указателя буфера в ОЗУ ПК для ЦАП."""

        ptr = c_long()

        self._zdev.ZGetPointerDAC(byref(ptr))
        return ptr.value

    def ZGetFlag(self) -> int:
        """Опрос флага прерываний."""

        flag = c_ulong()

        self._zdev.ZGetFlag(byref(flag))
        return flag.value

    def ZGetStartADC(self) -> int:
        """Опрос состояния накопления данных АЦП."""

        status = c_long()

        self._zdev.ZGetStartADC(byref(status))
        return status.value

    def ZGetStartDAC(self) -> int:
        """Опрос состояния накопления данных ЦАП."""

        status = c_long()

        self._zdev.ZGetStartDAC(byref(status))
        return status.value

    def ZStartADC(self) -> bool:
        """Старт накопления данных АЦП."""

        return self._zdev.ZStartADC()

    def ZStartDAC(self) -> bool:
        """Старт накопления данных ЦАП."""

        return self._zdev.ZStartDAC()

    def ZStopADC(self) -> bool:
        """Останов накопления данных АЦП."""

        return self._zdev.ZStopADC()

    def ZStopDAC(self) -> bool:
        """Останов накопления данных ЦАП."""

        return self._zdev.ZStopDAC()

# Управление модулем HCP

    def ZFindHCPADC(self) -> int:
        """Опрос поддержки и подключения модуля HCP."""

        present = c_long()

        self._zdev.ZFindHCPADC(byref(present))
        return present.value

    def ZGetHCPADC(self, channel: int) -> int:
        """Опрос режима работы заданного канала модуля HCP."""

        enable = c_long()

        self._zdev.ZGetHCPADC(c_long(channel), byref(enable))
        return enable.value

    def ZSetHCPADC(self, channel: int, enable: int) -> bool:
        """Установка режима работы заданного канала модуля HCP."""

        return self._zdev.ZSetHCPADC(c_long(channel), c_long(enable))

# Управление цифровым портом

    def ZGetDigOutEnable(self) -> int:
        """Опрос маски выходов цифрового порта."""

        mask = c_ulong()

        self._zdev.ZGetDigOutEnable(byref(mask))
        return mask.value

    def ZSetDigOutEnable(self, mask: int) -> bool:
        """Установить маску выходов цифрового порта."""

        return self._zdev.ZSetDigOutEnable(c_ulong(mask))

    def ZGetDigInput(self) -> int:
        """Прочитать данные с входов цифрового порта."""

        inputs = c_ulong()

        self._zdev.ZGetDigInput(byref(inputs))
        return inputs.value

    def ZGetDigOutput(self) -> int:
        """Прочитать данные, выдаваемые на выходы цифрового порта."""

        outputs = c_ulong()

        self._zdev.ZGetDigOutput(byref(outputs))
        return outputs.value

    def ZSetDigOutput(self, output: int) -> bool:
        """Записать данные в цифровой порт."""

        return self._zdev.ZSetDigOutput(c_ulong(output))

# ----------------------------

    def ZGetSerialNumberDSP(self) -> int:
        """Получить серийный номер DSP."""

        serial = c_long()

        self._zdev.ZGetSerialNumberDSP(byref(serial))
        return serial.value

    def ZGetNameDevice(self) -> bytes:
        """Получить имя устройства."""

        name = (c_char * 16)()

        self._zdev.ZGetNameDevice(name, sizeof(name))
        return name.value

    def ZGetTypeConnection(self) -> int:
        """Получить тип интерфейса."""

        iface = c_long()

        self._zdev.ZGetTypeConnection(byref(iface))
        return iface.value

    def ZGetQuantityChannelDigPort(self) -> int:
        """Запросить кол-во линий цифрового порта."""

        quantity = c_long()

        self._zdev.ZGetQuantityChannelDigPort(byref(quantity))
        return quantity.value

    def ZGetDigitalMode(self) -> int:
        """Опросить режим потокового ввода-вывода."""

        mode = c_long()

        self._zdev.ZGetDigitalMode(byref(mode))
        return mode.value

    def ZSetDigitalMode(self, mode: int) -> bool:
        """Переключить режим потокового ввода-вывода."""

        return self._zdev.ZSetDigitalMode(c_long(mode))

    def ZGetMasterSynchr(self) -> int:
        """Опрос разрешения генерации сигналов синхронизации на цифровой порт."""

        enable = c_long()

        self._zdev.ZGetMasterSynchr(byref(enable))
        return enable.value

    def ZSetMasterSynchr(self, enable: int) -> bool:
        """Разрешить генерацию сигналов синхронизации на цифровой порт."""

        return self._zdev.ZSetMasterSynchr(c_long(enable))

    def ZFindPWM(self) -> int:
        """Проверить поддерживается ли модуль ШИМ."""

        present = c_long()

        self._zdev.ZFindPWM(byref(present))
        return present.value

    def ZGetEnableExtFreqADC(self) -> int:
        """Прочитать статус синхронизации по внешней частоте АЦП."""

        enable = c_long()

        self._zdev.ZGetEnableExtFreqADC(byref(enable))
        return enable.value

    def ZGetEnableExtFreqDAC(self) -> int:
        """Прочитать статус синхронизации по внешней частоте ЦАП."""

        enable = c_long()

        self._zdev.ZGetEnableExtFreqDAC(byref(enable))
        return enable.value

    def ZSetEnableExtFreqADC(self, enable: int) -> bool:
        """Вкл./выкл. синхронизации по внешней частоте АЦП."""

        return self._zdev.ZSetEnableExtFreqADC(c_long(enable))

    def ZSetEnableExtFreqDAC(self, enable: int) -> bool:
        """Вкл./выкл. синхронизации по внешней частоте ЦАП."""

        return self._zdev.ZSetEnableExtFreqDAC(c_long(enable))

    def ZGetEnableExtStartADC(self) -> int:
        """Прочитать статус внешнего запуска АЦП."""

        enable = c_long()

        self._zdev.ZGetEnableExtStartADC(byref(enable))
        return enable.value

    def ZGetEnableExtStartDAC(self) -> int:
        """Прочитать статус внешнего запуска ЦАП."""

        enable = c_long()

        self._zdev.ZGetEnableExtStartDAC(byref(enable))
        return enable.value

    def ZSetEnableExtStartADC(self, enable: int) -> bool:
        """Вкл./выкл. внешнего запуска АЦП."""

        return self._zdev.ZSetEnableExtStartADC(c_long(enable))

    def ZSetEnableExtStartDAC(self, enable: int) -> bool:
        """Вкл./выкл. внешнего запуска ЦАП."""

        return self._zdev.ZSetEnableExtStartDAC(c_long(enable))

    def ZGetSizePacketADC(self) -> int:
        """Определить установленный размер пакета данных DSP АЦП."""

        size = c_long()

        self._zdev.ZGetSizePacketADC(byref(size))
        return size.value

    def ZGetSizePacketDAC(self) -> int:
        """Определить установленный размер пакета данных DSP ЦАП."""

        size = c_long()

        self._zdev.ZGetSizePacketDAC(byref(size))
        return size.value

    def ZGetMaxSizePacketADC(self) -> int:
        """Определить макс. возможный размер пакета данных DSP АЦП."""

        size = c_long()

        self._zdev.ZGetMaxSizePacketADC(byref(size))
        return size.value

    def ZGetMaxSizePacketDAC(self) -> int:
        """Определить макс. возможный размер пакета данных DSP ЦАП."""

        size = c_long()

        self._zdev.ZGetMaxSizePacketDAC(byref(size))
        return size.value

    def ZSetSizePacketADC(self, size: int) -> bool:
        """Установить размер пакета данных DSP АЦП."""

        return self._zdev.ZSetSizePacketADC(c_long(size))

    def ZSetSizePacketDAC(self, size: int) -> bool:
        """Установить размер пакета данных DSP ЦАП."""

        return self._zdev.ZSetSizePacketDAC(c_long(size))

    def ZGetQuantityPacketsADC(self) -> int:
        """Определить установленное кол-во пакетов за одно прерывание АЦП."""

        size = c_long()

        self._zdev.ZGetQuantityPacketsADC(byref(size))
        return size.value

    def ZGetQuantityPacketsDAC(self) -> int:
        """Определить установленное кол-во пакетов за одно прерывание ЦАП."""

        size = c_long()

        self._zdev.ZGetQuantityPacketsDAC(byref(size))
        return size.value

    def ZGetMaxQuantityPacketsADC(self) -> int:
        """Определить макс. возможное кол-во пакетов за одно прерывание АЦП."""

        size = c_long()

        self._zdev.ZGetMaxQuantityPacketsADC(byref(size))
        return size.value

    def ZGetMaxQuantityPacketsDAC(self) -> int:
        """Определить макс. возможное кол-во пакетов за одно прерывание ЦАП."""

        size = c_long()

        self._zdev.ZGetMaxQuantityPacketsDAC(byref(size))
        return size.value

    def ZSetQuantityPacketsADC(self, size: int) -> bool:
        """Установить кол-во пакетов за одно прерывание АЦП."""

        return self._zdev.ZSetQuantityPacketsADC(c_long(size))

    def ZSetQuantityPacketsDAC(self, size: int) -> bool:
        """Установить кол-во пакетов за одно прерывание ЦАП."""

        return self._zdev.ZSetQuantityPacketsDAC(c_long(size))

    def ZFindSoftAtten(self) -> int:
        """Определить поддерживается ли программный аттенюатор."""

        present = c_long()

        self._zdev.ZFindSoftAtten(byref(present))
        return present.value

    def ZGetMaxSizeBufferDSPDAC(self) -> int:
        """Опрос максимального размера буфера ЦАП в DSP."""

        size = c_long()

        self._zdev.ZGetMaxSizeBufferDSPDAC(byref(size))
        return size.value

    def ZGetSizeBufferDSPDAC(self) -> int:
        """Опрос размера буфера ЦАП в DSP."""

        size = c_long()

        self._zdev.ZGetSizeBufferDSPDAC(byref(size))
        return size.value

    def ZSetSizeBufferDSPDAC(self, size: int) -> bool:
        """Установить размер буфера ЦАП в DSP."""

        return self._zdev.ZSetSizeBufferDSPDAC(c_long(size))


__all__ = ["ZET"]

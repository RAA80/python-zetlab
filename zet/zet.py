#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import functools
import itertools
from ctypes import (cdll, byref, WINFUNCTYPE, POINTER, pointer, c_long, c_char,
                    c_char_p, c_double, c_void_p, c_ulong)


# тип устройства (платы) АЦП-ЦАП
ADC_16_200  = 0     # АЦП устройства ADC 16/200
APC_216     = 1     # АЦП устройства APC 216
ADC_16_500  = 2     # АЦП устройства ADC 16/500
ADC_16_500P = 3     # АЦП устройства ADC 16/500P
ADC_816     = 4     # АЦП устройства ADC 816
ADC_1002    = 5     # АЦП устройства ADC 1002
ADC_216_USB = 6     # АЦП устройства ADC 216 USB
ADC_24      = 7     # АЦП устройства ADC 24
ADC_1432    = 8     # АЦП устройства ADC 1432
ACPB_USB    = 9     # АЦП устройства ACPB USB
ZET210      = 10    # АЦП устройства ZET210
PD14_USB    = 11    # АЦП устройства PD14 USB
ZET110      = 12    # АЦП устройства ZET110
ZET302      = 13    # АЦП устройства ZET302
ZET017      = 14    # АЦП устройства ZET017
ZET017_U2   = 15    # АЦП устройства ZET017-U2, ZET019-U2
ZET220      = 16    # АЦП устройства ZET220
ZET230      = 17    # АЦП устройства ZET230
ZET240      = 18    # АЦП устройства ZET240
ZET048      = 19    # АЦП устройства ZET240, ZET048


_lib = cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), "Zadc.dll"))


class IDaqZDevice(c_void_p):
    _functions_ = {
        'ZOpen': WINFUNCTYPE(c_long, c_long, c_long),
        'ZClose': WINFUNCTYPE(c_long, c_long, c_long),
        'ZInitDSP': WINFUNCTYPE(c_long, c_long, c_long, c_char_p),
        'ZResetDSP': WINFUNCTYPE(c_long, c_long, c_long),
        'ZGetVersion': WINFUNCTYPE(c_long, c_long, c_long, c_char_p, c_char_p, c_char_p),
        'ZGetError': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZGetModify': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZSetTypeADC': WINFUNCTYPE(c_long, c_long, c_long),
        'ZSetTypeDAC': WINFUNCTYPE(c_long, c_long, c_long),
        'ZGetEnableADC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZGetEnableDAC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZGetQuantityChannelADC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZGetQuantityChannelDAC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZGetDigitalResolutionADC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_double)),
        'ZGetDigitalResolutionDAC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_double)),
        'ZGetDigitalResolChanADC': WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        'ZGetDigitalResolChanDAC': WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        'ZGetBitsADC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZGetBitsDAC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZGetWordsADC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZGetWordsDAC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZGetListFreqADC': WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        'ZGetListFreqDAC': WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        'ZSetNextFreqADC': WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        'ZSetNextFreqDAC': WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        'ZGetFreqADC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_double)),
        'ZGetFreqDAC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_double)),
        'ZSetFreqADC': WINFUNCTYPE(c_long, c_long, c_long, c_double, POINTER(c_double)),
        'ZSetFreqDAC': WINFUNCTYPE(c_long, c_long, c_long, c_double, POINTER(c_double)),
        'ZGetExtFreqADC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_double)),
        'ZGetExtFreqDAC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_double)),
        'ZSetExtFreqADC': WINFUNCTYPE(c_long, c_long, c_long, c_double),
        'ZSetExtFreqDAC': WINFUNCTYPE(c_long, c_long, c_long, c_double),
        'ZGetEnableExtFreq': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZSetEnableExtFreq': WINFUNCTYPE(c_long, c_long, c_long, c_long),
        'ZGetEnableExtStart': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZSetEnableExtStart': WINFUNCTYPE(c_long, c_long, c_long, c_long),
        'ZGetNumberInputADC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZGetNumberOutputDAC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZGetInputADC': WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_long)),
        'ZGetOutputDAC': WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_long)),
        'ZSetInputADC': WINFUNCTYPE(c_long, c_long, c_long, c_long, c_long),
        'ZSetOutputDAC': WINFUNCTYPE(c_long, c_long, c_long, c_long, c_long),
        'ZGetInputDiffADC': WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_long)),
        'ZSetInputDiffADC': WINFUNCTYPE(c_long, c_long, c_long, c_long, c_long),
        'ZGetListAmplifyADC': WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        'ZSetNextAmplifyADC': WINFUNCTYPE(c_long, c_long, c_long, c_long, c_long, POINTER(c_double)),
        'ZGetAmplifyADC': WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        'ZSetAmplifyADC': WINFUNCTYPE(c_long, c_long, c_long, c_long, c_double, POINTER(c_double)),
        'ZGetListPreAmplifyADC': WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        'ZSetNextPreAmplifyADC': WINFUNCTYPE(c_long, c_long, c_long, c_long, c_long, POINTER(c_double)),
        'ZSetPreAmplifyADC': WINFUNCTYPE(c_long, c_long, c_long, c_long, c_double, POINTER(c_double)),
        'ZGetPreAmplifyADC': WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        'ZGetAttenDAC': WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_double)),
        'ZSetAttenDAC': WINFUNCTYPE(c_long, c_long, c_long, c_long, c_double, POINTER(c_double)),
        'ZSetExtCycleDAC': WINFUNCTYPE(c_long, c_long, c_long, c_long),
        'ZGetInterruptADC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZGetInterruptDAC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZGetMaxInterruptADC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZGetMaxInterruptDAC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZSetInterruptADC': WINFUNCTYPE(c_long, c_long, c_long, c_long),
        'ZSetInterruptDAC': WINFUNCTYPE(c_long, c_long, c_long, c_long),
        'ZSetBufferSizeADC': WINFUNCTYPE(c_long, c_long, c_long, c_long),
        'ZSetBufferSizeDAC': WINFUNCTYPE(c_long, c_long, c_long, c_long),
        'ZGetBufferADC': WINFUNCTYPE(c_long, c_long, c_long, c_void_p, POINTER(c_long)),
        'ZGetBufferDAC': WINFUNCTYPE(c_long, c_long, c_long, c_void_p, POINTER(c_long)),
        'ZRemBufferADC': WINFUNCTYPE(c_long, c_long, c_long, c_void_p),
        'ZRemBufferDAC': WINFUNCTYPE(c_long, c_long, c_long, c_void_p),
        'ZSetCycleSampleADC': WINFUNCTYPE(c_long, c_long, c_long, c_long),
        'ZSetCycleSampleDAC': WINFUNCTYPE(c_long, c_long, c_long, c_long),
        'ZGetLastDataADC': WINFUNCTYPE(c_long, c_long, c_long, c_long, c_void_p, c_long),
        'ZGetPointerADC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZGetPointerDAC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZGetFlag': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_ulong)),
        'ZGetStartADC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZGetStartDAC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZStartADC': WINFUNCTYPE(c_long, c_long, c_long),
        'ZStartDAC': WINFUNCTYPE(c_long, c_long, c_long),
        'ZStopADC': WINFUNCTYPE(c_long, c_long, c_long),
        'ZStopDAC': WINFUNCTYPE(c_long, c_long, c_long),
        'ZFindHCPADC': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_long)),
        'ZGetHCPADC': WINFUNCTYPE(c_long, c_long, c_long, c_long, POINTER(c_long)),
        'ZSetHCPADC': WINFUNCTYPE(c_long, c_long, c_long, c_long, c_long),
        'ZGetDigOutEnable': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_ulong)),
        'ZSetDigOutEnable': WINFUNCTYPE(c_long, c_long, c_long, c_ulong),
        'ZGetDigInput': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_ulong)),
        'ZGetDigOutput': WINFUNCTYPE(c_long, c_long, c_long, POINTER(c_ulong)),
        'ZSetDigOutput': WINFUNCTYPE(c_long, c_long, c_long, c_ulong)
    }

    def __call__(self, *args):
        prototype = args[0]
        arguments = args[1:]

        ret = prototype((self.name, _lib))(*arguments)
        if ret:
            raise Exception("{} error {:04X}".format(self.name, ret))

        return ret

    def __getattr__(self, name):
        self.name = name
        if name in self._functions_:
            return functools.partial(self.__call__, self._functions_[name])


class ZET(object):
    ''' Python wrapper for zadc library '''

    def __init__(self, device, dsp):
        self._device = device
        self._dsp = dsp

        self._zdev = IDaqZDevice()

    def __enter__(self):
        if self.ZOpen():
            return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.ZClose()

# Подключение к драйверу и отключение

    def ZOpen(self):
        ''' Подключиться к драйверу '''

        return not self._zdev.ZOpen(self._device, self._dsp)

    def ZClose(self):
        ''' Отключиться от драйвера '''

        return not self._zdev.ZClose(self._device, self._dsp)

# Сброс и инициализация

    def ZInitDSP(self, filename=""):
        ''' Проинициализировать сигнальный процессор '''

        return not self._zdev.ZInitDSP(self._device, self._dsp, filename.encode("ascii"))

    def ZResetDSP(self):
        ''' Сброс и останов сигнальных процессоров (влияет на все DSP одного устройства) '''

        return not self._zdev.ZResetDSP(self._device, self._dsp)

# Сервисные функции

    def ZGetVersion(self):
        ''' Опрос версии программ и драйвера '''

        verDSP = (c_char*100)()
        verDRV = (c_char*100)()
        verLIB = (c_char*100)()

        if not self._zdev.ZGetVersion(self._device, self._dsp, verDSP, verDRV, verLIB):
            return {"verDSP": verDSP.value,
                    "verDRV": verDRV.value,
                    "verLIB": verLIB.value}

    def ZGetError(self):
        ''' Прочитать код ошибки '''

        error = c_long()

        if not self._zdev.ZGetError(self._device, self._dsp, byref(error)):
            return error.value

    def ZGetModify(self):
        ''' Определить кол-во изменений параметров с момента загрузки '''

        modify = c_long()

        if not self._zdev.ZGetModify(self._device, self._dsp, byref(modify)):
            return modify.value

# Установка режима работы сигнального процессора

    def ZSetTypeADC(self):
        ''' Установить сигнальный процессор в режим АЦП '''

        return not self._zdev.ZSetTypeADC(self._device, self._dsp)

    def ZSetTypeDAC(self):
        ''' Установить сигнальный процессор в режим ЦАП '''

        return not self._zdev.ZSetTypeDAC(self._device, self._dsp)

# Опрос основных характеристик модулей АЦП и ЦАП

    def ZGetEnableADC(self):
        ''' Опрос возможности работы сигнального процессора с модулем АЦП '''

        enable = c_long()

        if not self._zdev.ZGetEnableADC(self._device, self._dsp, byref(enable)):
            return enable.value

    def ZGetEnableDAC(self):
        ''' Опрос возможности работы сигнального процессора с модулем ЦАП '''

        enable = c_long()

        if not self._zdev.ZGetEnableDAC(self._device, self._dsp, byref(enable)):
            return enable.value

    def ZGetQuantityChannelADC(self):
        ''' Опрос максимального количества каналов модуля АЦП '''

        quantity = c_long()

        if not self._zdev.ZGetQuantityChannelADC(self._device, self._dsp, byref(quantity)):
            return quantity.value

    def ZGetQuantityChannelDAC(self):
        ''' Опрос максимального количества каналов модуля ЦАП '''

        quantity = c_long()

        if not self._zdev.ZGetQuantityChannelDAC(self._device, self._dsp, byref(quantity)):
            return quantity.value

    def ZGetDigitalResolutionADC(self):
        ''' Опрос веса младшего разряда АЦП (устаревшая функция) '''

        resolution = c_double()

        if not self._zdev.ZGetDigitalResolutionADC(self._device, self._dsp, byref(resolution)):
            return resolution.value

    def ZGetDigitalResolutionDAC(self):
        ''' Опрос веса младшего разряда ЦАП (устаревшая функция) '''

        resolution = c_double()

        if not self._zdev.ZGetDigitalResolutionDAC(self._device, self._dsp, byref(resolution)):
            return resolution.value

    def ZGetDigitalResolChanADC(self, channel):
        ''' Прочитать откалиброванный поканально вес младшего разряда АЦП '''

        resolution = c_double()
        channel = c_long(channel)

        if not self._zdev.ZGetDigitalResolChanADC(self._device, self._dsp, channel, byref(resolution)):
            return resolution.value

    def ZGetDigitalResolChanDAC(self, channel):
        ''' Прочитать откалиброванный поканально вес младшего разряда ЦАП '''

        resolution = c_double()
        channel = c_long(channel)

        if not self._zdev.ZGetDigitalResolChanDAC(self._device, self._dsp, channel, byref(resolution)):
            return resolution.value

    def ZGetBitsADC(self):
        ''' Опрос количества двоичных разрядов АЦП '''

        nbits = c_long()

        if not self._zdev.ZGetBitsADC(self._device, self._dsp, byref(nbits)):
            return nbits.value

    def ZGetBitsDAC(self):
        ''' Опрос количества двоичных разрядов ЦАП '''

        nbits = c_long()

        if not self._zdev.ZGetBitsDAC(self._device, self._dsp, byref(nbits)):
            return nbits.value

    def ZGetWordsADC(self):
        ''' Опрос размера каждого отсчета АЦП в 16-разрядных словах '''

        nwords = c_long()

        if not self._zdev.ZGetWordsADC(self._device, self._dsp, byref(nwords)):
            return nwords.value

    def ZGetWordsDAC(self):
        ''' Опрос размера каждого отсчета ЦАП в 16-разрядных словах '''

        nwords = c_long()

        if not self._zdev.ZGetWordsDAC(self._device, self._dsp, byref(nwords)):
            return nwords.value

# Установка частоты дискретизации и режима синхронизации АЦП/ЦАП

    def ZGetListFreqADC(self):
        ''' Получение списка возможных частот дискретизации АЦП '''

        freq = c_double()
        freq_list = []

        for next in itertools.count():
            try:
                self._zdev.ZGetListFreqADC(self._device, self._dsp, c_long(next), byref(freq))
                freq_list.append(freq.value)
            except Exception:
                break

        return freq_list

    def ZGetListFreqDAC(self):
        ''' Получение списка возможных частот дискретизации ЦАП '''

        freq = c_double()
        freq_list = []

        for next in itertools.count():
            try:
                self._zdev.ZGetListFreqDAC(self._device, self._dsp, c_long(next), byref(freq))
                freq_list.append(freq.value)
            except Exception:
                break

        return freq_list

    def ZSetNextFreqADC(self, next):
        ''' Установить следующую из списка частоту дискретизации АЦП '''

        next = c_long(next)
        freq = c_double()

        if not self._zdev.ZSetNextFreqADC(self._device, self._dsp, next, byref(freq)):
            return freq.value

    def ZSetNextFreqDAC(self, next):
        ''' Установить следующую из списка частоту дискретизации ЦАП '''

        next = c_long(next)
        freq = c_double()

        if not self._zdev.ZSetNextFreqDAC(self._device, self._dsp, next, byref(freq)):
            return freq.value

    def ZGetFreqADC(self):
        ''' Опрос текущей частоты дискретизации АЦП '''

        freq = c_double()

        if not self._zdev.ZGetFreqADC(self._device, self._dsp, byref(freq)):
            return freq.value

    def ZGetFreqDAC(self):
        ''' Опрос текущей частоты дискретизации ЦАП '''

        freq = c_double()

        if not self._zdev.ZGetFreqDAC(self._device, self._dsp, byref(freq)):
            return freq.value

    def ZSetFreqADC(self, freq_in):
        ''' Установка частоты дискретизации АЦП '''

        freq_in = c_double(freq_in)
        freq_out = c_double()

        if not self._zdev.ZSetFreqADC(self._device, self._dsp, freq_in, byref(freq_out)):
            return freq_out.value

    def ZSetFreqDAC(self, freq_in):
        ''' Установка частоты дискретизации ЦАП '''

        freq_in = c_double(freq_in)
        freq_out = c_double()

        if not self._zdev.ZSetFreqDAC(self._device, self._dsp, freq_in, byref(freq_out)):
            return freq_out.value

    def ZGetExtFreqADC(self):
        ''' Опрос текущей опорной частоты АЦП '''

        freq = c_double()

        if not self._zdev.ZGetExtFreqADC(self._device, self._dsp, byref(freq)):
            return freq.value

    def ZGetExtFreqDAC(self):
        ''' Опрос текущей опорной частоты ЦАП '''

        freq = c_double()

        if not self._zdev.ZGetExtFreqDAC(self._device, self._dsp, byref(freq)):
            return freq.value

    def ZSetExtFreqADC(self, ext_freq):
        ''' Установка значения внешней опорной частоты АЦП '''

        ext_freq = c_double(ext_freq)

        return not self._zdev.ZSetExtFreqADC(self._device, self._dsp, ext_freq)

    def ZSetExtFreqDAC(self, ext_freq):
        ''' Установка значения внешней опорной частоты ЦАП '''

        ext_freq = c_double(ext_freq)

        return not self._zdev.ZSetExtFreqDAC(self._device, self._dsp, ext_freq)

    def ZGetEnableExtFreq(self):
        ''' Прочитать статус синхронизации по внешней частоте (устаревшая функция) '''

        enable = c_long()

        if not self._zdev.ZGetEnableExtFreq(self._device, self._dsp, byref(enable)):
            return enable.value

    def ZSetEnableExtFreq(self, enable):
        ''' Вкл./выкл. синхронизации по внешней частоте (устаревшая функция) '''

        enable = c_long(enable)

        return not self._zdev.ZSetEnableExtFreq(self._device, self._dsp, enable)

    def ZGetEnableExtStart(self):
        ''' Прочитать статус внешнего запуска (устаревшая функция) '''

        enable = c_long()

        if not self._zdev.ZGetEnableExtStart(self._device, self._dsp, byref(enable)):
            return enable.value

    def ZSetEnableExtStart(self, enable):
        ''' Вкл./выкл. внешнего запуска (устаревшая функция) '''

        enable = c_long(enable)

        return not self._zdev.ZSetEnableExtStart(self._device, self._dsp, enable)

# Управление каналами ввода (вывода) АЦП/ЦАП

    def ZGetNumberInputADC(self):
        ''' Опрос количества включенных каналов АЦП '''

        channel = c_long()

        if not self._zdev.ZGetNumberInputADC(self._device, self._dsp, byref(channel)):
            return channel.value

    def ZGetNumberOutputDAC(self):
        ''' Опрос количества включенных каналов ЦАП '''

        channel = c_long()

        if not self._zdev.ZGetNumberOutputDAC(self._device, self._dsp, byref(channel)):
            return channel.value

    def ZGetInputADC(self, channel):
        ''' Опрос включен ли заданный канал АЦП '''

        enable = c_long()
        channel = c_long(channel)

        if not self._zdev.ZGetInputADC(self._device, self._dsp, channel, byref(enable)):
            return enable.value

    def ZGetOutputDAC(self, channel):
        ''' Опрос включен ли заданный канал ЦАП '''

        enable = c_long()
        channel = c_long(channel)

        if not self._zdev.ZGetOutputDAC(self._device, self._dsp, channel, byref(enable)):
            return enable.value

    def ZSetInputADC(self, channel, enable):
        ''' Включить/выключить заданный канал АЦП '''

        enable = c_long(enable)
        channel = c_long(channel)

        return not self._zdev.ZSetInputADC(self._device, self._dsp, channel, enable)

    def ZSetOutputDAC(self, channel, enable):
        ''' Включить/выключить заданный канал ЦАП '''

        enable = c_long(enable)
        channel = c_long(channel)

        return not self._zdev.ZSetOutputDAC(self._device, self._dsp, channel, enable)

    def ZGetInputDiffADC(self, channel):
        ''' Опрос дифференциального режима заданного канала для ввода АЦП '''

        enable = c_long()
        channel = c_long(channel)

        if not self._zdev.ZGetInputDiffADC(self._device, self._dsp, channel, byref(enable)):
            return enable.value

    def ZSetInputDiffADC(self, channel, enable):
        ''' Установить-сбросить заданный канал для ввода в дифференциальный режим АЦП '''

        enable = c_long(enable)
        channel = c_long(channel)

        return not self._zdev.ZSetInputDiffADC(self._device, self._dsp, channel, enable)

# Управление коэффициентами усиления АЦП

    def ZGetListAmplifyADC(self):
        ''' Получение списка возможных коэффициентов усиления АЦП '''

        amplify = c_double()
        amplify_list = []

        for next in itertools.count():
            try:
                self._zdev.ZGetListAmplifyADC(self._device, self._dsp, c_long(next), byref(amplify))
                amplify_list.append(amplify.value)
            except Exception:
                break

        return amplify_list

    def ZSetNextAmplifyADC(self, channel, next):
        ''' Установка большего или меньшего коэффициента усиления из списка выбранного канала АЦП '''

        next = c_long(next)
        channel = c_long(channel)
        amplify = c_double()

        if not self._zdev.ZSetNextAmplifyADC(self._device, self._dsp, channel, next, byref(amplify)):
            return amplify.value

    def ZGetAmplifyADC(self, channel):
        ''' Опрос коэффициента усиления выбранного канала АЦП '''

        amplify = c_double()
        channel = c_long(channel)

        if not self._zdev.ZGetAmplifyADC(self._device, self._dsp, channel, byref(amplify)):
            return amplify.value

    def ZSetAmplifyADC(self, channel, amplify_in):
        ''' Установка коэффициента усиления выбранного канала АЦП '''

        amplify_in = c_double(amplify_in)
        amplify_out = c_double()
        channel = c_long(channel)

        if not self._zdev.ZSetAmplifyADC(self._device, self._dsp, channel, amplify_in, byref(amplify_out)):
            return amplify_out.value

# Управление коэффициентами усиления ПУ 8/10

    def ZGetListPreAmplifyADC(self):
        ''' Получение списка возможных коэффициентов усиления предварительного усилителя '''

        amplify = c_double()
        amplify_list = []

        for next in itertools.count():
            try:
                self._zdev.ZGetListPreAmplifyADC(self._device, self._dsp, c_long(next), byref(amplify))
                amplify_list.append(amplify.value)
            except Exception:
                break

        return amplify_list

    def ZSetNextPreAmplifyADC(self, channel, next):
        ''' Установка большего или меньшего коэффициента усиления из списка предварительного усилителя '''

        next = c_long(next)
        channel = c_long(channel)
        amplify = c_double()

        if not self._zdev.ZSetNextPreAmplifyADC(self._device, self._dsp, channel, next, byref(amplify)):
            return amplify.value

    def ZSetPreAmplifyADC(self, channel, amplify_in):
        ''' Установка коэффициента усиления предварительного усилителя выбранного канала '''

        amplify_in = c_double(amplify_in)
        amplify_out = c_double()
        channel = c_long(channel)

        if not self._zdev.ZSetPreAmplifyADC(self._device, self._dsp, channel, amplify_in, byref(amplify_out)):
            return amplify_out.value

    def ZGetPreAmplifyADC(self, channel):
        ''' Опрос коэффициента усиления предварительного усилителя выбранного канала '''

        amplify = c_double()
        channel = c_long(channel)

        if not self._zdev.ZGetPreAmplifyADC(self._device, self._dsp, channel, byref(amplify)):
            return amplify.value

# Управление коэффициентами ослабления аттенюатора ЦАП

    def ZGetAttenDAC(self, channel):
        ''' Опрос коэффициента ослабления аттенюатора выбранного канала '''

        reduction = c_double()
        channel = c_long(channel)

        if not self._zdev.ZGetAttenDAC(self._device, self._dsp, channel, byref(reduction)):
            return reduction.value

    def ZSetAttenDAC(self, channel, reduction_in):
        ''' Установка коэффициента ослабления аттенюатора выбранного канала '''

        reduction_in = c_double(reduction_in)
        reduction_out = c_double()
        channel = c_long(channel)

        if not self._zdev.ZSetAttenDAC(self._device, self._dsp, channel, reduction_in, byref(reduction_out)):
            return reduction_out.value

# Управление процессом перекачки данных

    def ZSetExtCycleDAC(self, enable):
        ''' Установка режима внешней подкачки данных или внутренней генерации сигналов '''

        enable = c_long(enable)

        return not self._zdev.ZSetExtCycleDAC(self._device, self._dsp, enable)

    def ZGetInterruptADC(self):
        ''' Опрос размера буфера для перекачки данных АЦП '''

        size = c_long()

        if not self._zdev.ZGetInterruptADC(self._device, self._dsp, byref(size)):
            return size.value

    def ZGetInterruptDAC(self):
        ''' Опрос размера буфера для перекачки данных ЦАП '''

        size = c_long()

        if not self._zdev.ZGetInterruptDAC(self._device, self._dsp, byref(size)):
            return size.value

    def ZGetMaxInterruptADC(self):
        ''' Опрос максимального размера буфера для перекачки данных АЦП '''

        size = c_long()

        if not self._zdev.ZGetMaxInterruptADC(self._device, self._dsp, byref(size)):
            return size.value

    def ZGetMaxInterruptDAC(self):
        ''' Опрос максимального размера буфера для перекачки данных ЦАП '''

        size = c_long()

        if not self._zdev.ZGetMaxInterruptDAC(self._device, self._dsp, byref(size)):
            return size.value

    def ZSetInterruptADC(self, size):
        ''' Установка размера буфера для перекачки данных АЦП '''

        size = c_long(size)

        return not self._zdev.ZSetInterruptADC(self._device, self._dsp, size)

    def ZSetInterruptDAC(self, size):
        ''' Установка размера буфера для перекачки данных ЦАП '''

        size = c_long(size)

        return not self._zdev.ZSetInterruptDAC(self._device, self._dsp, size)

    def ZSetBufferSizeADC(self, size):
        ''' Задать размер буфера АЦП в ОЗУ ПК '''

        size = c_long(size)

        return not self._zdev.ZSetBufferSizeADC(self._device, self._dsp, size)

    def ZSetBufferSizeDAC(self, size):
        ''' Задать размер буфера ЦАП в ОЗУ ПК '''

        size = c_long(size)

        return not self._zdev.ZSetBufferSizeDAC(self._device, self._dsp, size)

    def ZGetBufferADC(self):
        ''' Запросить буфер в ОЗУ ПК для АЦП'''

        buff_ptr = pointer(c_long())
        size = c_long()

        if not self._zdev.ZGetBufferADC(self._device, self._dsp, byref(buff_ptr), byref(size)):
            return buff_ptr, size.value

    def ZGetBufferDAC(self):
        ''' Запросить буфер в ОЗУ ПК для ЦАП'''

        buff_ptr = pointer(c_long())
        size = c_long()

        if not self._zdev.ZGetBufferDAC(self._device, self._dsp, byref(buff_ptr), byref(size)):
            return buff_ptr, size.value

    def ZRemBufferADC(self, buff_ptr):
        ''' Освободить буфер в ОЗУ ПК для АЦП '''

        return not self._zdev.ZRemBufferADC(self._device, self._dsp, byref(buff_ptr))

    def ZRemBufferDAC(self, buff_ptr):
        ''' Освободить буфер в ОЗУ ПК для ЦАП '''

        return not self._zdev.ZRemBufferDAC(self._device, self._dsp, byref(buff_ptr))

    def ZSetCycleSampleADC(self, enable):
        ''' Установка циклического или одноразового накопления АЦП '''

        enable = c_long(enable)

        return not self._zdev.ZSetCycleSampleADC(self._device, self._dsp, enable)

    def ZSetCycleSampleDAC(self, enable):
        ''' Установка циклического или одноразового накопления ЦАП '''

        enable = c_long(enable)

        return not self._zdev.ZSetCycleSampleDAC(self._device, self._dsp, enable)

    def ZGetLastDataADC(self, channel, size):
        ''' Пересылка последних накопленных данных АЦП '''

        buff_ptr = c_void_p()
        channel = c_long(channel)
        size = c_long(size)

        return not self._zdev.ZGetLastDataADC(self._device, self._dsp, channel, buff_ptr, size)

    def ZGetPointerADC(self):
        ''' Чтение указателя буфера в ОЗУ ПК для АЦП '''

        ptr = c_long()

        if not self._zdev.ZGetPointerADC(self._device, self._dsp, byref(ptr)):
            return ptr.value

    def ZGetPointerDAC(self):
        ''' Чтение указателя буфера в ОЗУ ПК для ЦАП '''

        ptr = c_long()

        if not self._zdev.ZGetPointerDAC(self._device, self._dsp, byref(ptr)):
            return ptr.value

    def ZGetFlag(self):
        ''' Опрос флага прерываний '''

        flag = c_ulong()

        if not self._zdev.ZGetFlag(self._device, self._dsp, byref(flag)):
            return flag.value

    def ZGetStartADC(self):
        ''' Опрос состояния накопления данных АЦП '''

        status = c_long()

        if not self._zdev.ZGetStartADC(self._device, self._dsp, byref(status)):
            return status.value

    def ZGetStartDAC(self):
        ''' Опрос состояния накопления данных ЦАП '''

        status = c_long()

        if not self._zdev.ZGetStartDAC(self._device, self._dsp, byref(status)):
            return status.value

    def ZStartADC(self):
        ''' Старт накопления данных АЦП '''

        return not self._zdev.ZStartADC(self._device, self._dsp)

    def ZStartDAC(self):
        ''' Старт накопления данных ЦАП '''

        return not self._zdev.ZStartDAC(self._device, self._dsp)

    def ZStopADC(self):
        ''' Останов накопления данных АЦП '''

        return not self._zdev.ZStopADC(self._device, self._dsp)

    def ZStopDAC(self):
        ''' Останов накопления данных ЦАП '''

        return not self._zdev.ZStopDAC(self._device, self._dsp)

# Управление модулем HCP

    def ZFindHCPADC(self):
        ''' Опрос поддержки и подключения модуля HCP '''

        present = c_long()

        if not self._zdev.ZFindHCPADC(self._device, self._dsp, byref(present)):
            return present.value

    def ZGetHCPADC(self, channel):
        ''' Опрос режима работы заданного канала модуля HCP '''

        enable = c_long()
        channel = c_long(channel)

        if not self._zdev.ZGetHCPADC(self._device, self._dsp, channel, byref(enable)):
            return enable.value

    def ZSetHCPADC(self, channel, enable):
        ''' Установка режима работы заданного канала модуля HCP '''

        enable = c_long(enable)
        channel = c_long(channel)

        return not self._zdev.ZSetHCPADC(self._device, self._dsp, channel, enable)

# Управление цифровым портом

    def ZGetDigOutEnable(self):
        ''' Опрос маски выходов цифрового порта '''

        enable_mask = c_ulong()

        if not self._zdev.ZGetDigOutEnable(self._device, self._dsp, byref(enable_mask)):
            return enable_mask.value

    def ZSetDigOutEnable(self, enable_mask):
        ''' Установить маску выходов цифрового порта '''

        enable_mask = c_ulong(enable_mask)

        return not self._zdev.ZSetDigOutEnable(self._device, self._dsp, enable_mask)

    def ZGetDigInput(self):
        ''' Прочитать данные с входов цифрового порта '''

        digital_input = c_ulong()

        if not self._zdev.ZGetDigInput(self._device, self._dsp, byref(digital_input)):
            return digital_input.value

    def ZGetDigOutput(self):
        ''' Прочитать данные, выдаваемые на выходы цифрового порта '''

        digital_output = c_ulong()

        if not self._zdev.ZGetDigOutput(self._device, self._dsp, byref(digital_output)):
            return digital_output.value

    def ZSetDigOutput(self, digital_output):
        ''' Записать данные в цифровой порт '''

        digital_output = c_ulong(digital_output)

        return not self._zdev.ZSetDigOutput(self._device, self._dsp, digital_output)


__all__ = [ "ZET" ]

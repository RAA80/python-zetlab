#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import functools
from ctypes import (cdll, byref, WINFUNCTYPE, POINTER, pointer, c_long, c_char,
                    c_char_p, c_double, c_void_p, c_ulong, c_ushort)


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
    def __init__(self, device, dsp):
        self.typeDevice = device
        self.numberDSP = dsp

        self._zdev = IDaqZDevice()

    def __enter__(self):
        self.ZOpen()

    def __exit__(self, exc_type, exc_value, traceback):
        self.ZClose()

# Подключение к драйверу и отключение

    def ZOpen(self):
        ''' Подключиться к драйверу '''

        return not self._zdev.ZOpen(self.typeDevice, self.numberDSP)

    def ZClose(self):
        ''' Отключиться от драйвера '''

        return not self._zdev.ZClose(self.typeDevice, self.numberDSP)

# Сброс и инициализация

    def ZInitDSP(self, fileName=""):
        ''' Проинициализировать сигнальный процессор '''

        return not self._zdev.ZInitDSP(self.typeDevice, self.numberDSP, fileName.encode("ascii"))

    def ZResetDSP(self):
        ''' Сброс и останов сигнальных процессоров (влияет на все DSP одного устройства) '''

        return not self._zdev.ZResetDSP(self.typeDevice, self.numberDSP)

# Сервисные функции

    def ZGetVersion(self):
        ''' Опрос версии программ и драйвера '''

        verDSP = (c_char*100)()
        verDRV = (c_char*100)()
        verLIB = (c_char*100)()

        if not self._zdev.ZGetVersion(self.typeDevice, self.numberDSP, verDSP, verDRV, verLIB):
            return {"verDSP": verDSP.value,
                    "verDRV": verDRV.value,
                    "verLIB": verLIB.value}

    def ZGetError(self):
        ''' Прочитать код ошибки '''

        last_err = c_long()

        if not self._zdev.ZGetError(self.typeDevice, self.numberDSP, byref(last_err)):
            return last_err.value

    def ZGetModify(self):
        ''' Определить кол-во изменений параметров с момента загрузки '''

        modify = c_long()

        if not self._zdev.ZGetModify(self.typeDevice, self.numberDSP, byref(modify)):
            return modify.value

# Установка режима работы сигнального процессора

    def ZSetTypeADC(self):
        ''' Установить сигнальный процессор в режим АЦП '''

        return not self._zdev.ZSetTypeADC(self.typeDevice, self.numberDSP)

    def ZSetTypeDAC(self):
        ''' Установить сигнальный процессор в режим ЦАП '''

        return not self._zdev.ZSetTypeDAC(self.typeDevice, self.numberDSP)

# Опрос основных характеристик модулей АЦП и ЦАП

    def ZGetEnableADC(self):
        ''' Опрос возможности работы сигнального процессора с модулем АЦП '''

        enable = c_long()

        if not self._zdev.ZGetEnableADC(self.typeDevice, self.numberDSP, byref(enable)):
            return enable.value

    def ZGetEnableDAC(self):
        ''' Опрос возможности работы сигнального процессора с модулем ЦАП '''

        enable = c_long()

        if not self._zdev.ZGetEnableDAC(self.typeDevice, self.numberDSP, byref(enable)):
            return enable.value

    def ZGetQuantityChannelADC(self):
        ''' Опрос максимального количества каналов модуля АЦП '''

        quantity = c_long()

        if not self._zdev.ZGetQuantityChannelADC(self.typeDevice, self.numberDSP, byref(quantity)):
            return quantity.value

    def ZGetQuantityChannelDAC(self):
        ''' Опрос максимального количества каналов модуля ЦАП '''

        quantity = c_long()

        if not self._zdev.ZGetQuantityChannelDAC(self.typeDevice, self.numberDSP, byref(quantity)):
            return quantity.value

    def ZGetDigitalResolutionADC(self):
        ''' Опрос веса младшего разряда АЦП (устаревшая функция) '''

        resolution = c_double()

        if not self._zdev.ZGetDigitalResolutionADC(self.typeDevice, self.numberDSP, byref(resolution)):
            return resolution.value

    def ZGetDigitalResolutionDAC(self):
        ''' Опрос веса младшего разряда ЦАП (устаревшая функция) '''

        resolution = c_double()

        if not self._zdev.ZGetDigitalResolutionDAC(self.typeDevice, self.numberDSP, byref(resolution)):
            return resolution.value

    def ZGetDigitalResolChanADC(self, channel):
        ''' Прочитать откалиброванный поканально вес младшего разряда АЦП '''

        resolution = c_double()
        channel = c_long(channel)

        if not self._zdev.ZGetDigitalResolChanADC(self.typeDevice, self.numberDSP, channel, byref(resolution)):
            return resolution.value

    def ZGetDigitalResolChanDAC(self, channel):
        ''' Прочитать откалиброванный поканально вес младшего разряда ЦАП '''

        resolution = c_double()
        channel = c_long(channel)

        if not self._zdev.ZGetDigitalResolChanDAC(self.typeDevice, self.numberDSP, channel, byref(resolution)):
            return resolution.value

    def ZGetBitsADC(self):
        ''' Опрос количества двоичных разрядов АЦП '''

        nbits = c_long()

        if not self._zdev.ZGetBitsADC(self.typeDevice, self.numberDSP, byref(nbits)):
            return nbits.value

    def ZGetBitsDAC(self):
        ''' Опрос количества двоичных разрядов ЦАП '''

        nbits = c_long()

        if not self._zdev.ZGetBitsDAC(self.typeDevice, self.numberDSP, byref(nbits)):
            return nbits.value

    def ZGetWordsADC(self):
        ''' Опрос размера каждого отсчета АЦП в 16-разрядных словах '''

        nwords = c_long()

        if not self._zdev.ZGetWordsADC(self.typeDevice, self.numberDSP, byref(nwords)):
            return nwords.value

    def ZGetWordsDAC(self):
        ''' Опрос размера каждого отсчета ЦАП в 16-разрядных словах '''

        nwords = c_long()

        if not self._zdev.ZGetWordsDAC(self.typeDevice, self.numberDSP, byref(nwords)):
            return nwords.value

# Установка частоты дискретизации и режима синхронизации АЦП/ЦАП

    def ZGetListFreqADC(self):
        ''' Получение списка возможных частот дискретизации АЦП '''

        next = c_long(0)
        freq = c_double()
        freq_list = []

        i = 0
        while True:
            try:
                self._zdev.ZGetListFreqADC(self.typeDevice, self.numberDSP, next, byref(freq))
                freq_list.append(freq.value)
            except Exception as err:
                break
            else:
                i += 1
                next = c_long(i)

        return freq_list

    def ZGetListFreqDAC(self):
        ''' Получение списка возможных частот дискретизации ЦАП '''

        next = c_long(0)
        freq = c_double()
        freq_list = []

        i = 0
        while True:
            try:
                self._zdev.ZGetListFreqDAC(self.typeDevice, self.numberDSP, next, byref(freq))
                freq_list.append(freq.value)
            except Exception as err:
                break
            else:
                i += 1
                next = c_long(i)

        return freq_list

    def ZSetNextFreqADC(self, next):
        ''' Установить следующую из списка частоту дискретизации АЦП '''

        next = c_long(next)
        freq = c_double()

        if not self._zdev.ZSetNextFreqADC(self.typeDevice, self.numberDSP, next, byref(freq)):
            return freq.value

    def ZSetNextFreqDAC(self, next):
        ''' Установить следующую из списка частоту дискретизации ЦАП '''

        next = c_long(next)
        freq = c_double()

        if not self._zdev.ZSetNextFreqDAC(self.typeDevice, self.numberDSP, next, byref(freq)):
            return freq.value

    def ZGetFreqADC(self):
        ''' Опрос текущей частоты дискретизации АЦП '''

        freq = c_double()

        if not self._zdev.ZGetFreqADC(self.typeDevice, self.numberDSP, byref(freq)):
            return freq.value

    def ZGetFreqDAC(self):
        ''' Опрос текущей частоты дискретизации ЦАП '''

        freq = c_double()

        if not self._zdev.ZGetFreqDAC(self.typeDevice, self.numberDSP, byref(freq)):
            return freq.value

    def ZSetFreqADC(self, freqIn):
        ''' Установка частоты дискретизации АЦП '''

        freqIn = c_double(freqIn)
        freqOut = c_double()

        if not self._zdev.ZSetFreqADC(self.typeDevice, self.numberDSP, freqIn, byref(freqOut)):
            return freqOut.value

    def ZSetFreqDAC(self, freqIn):
        ''' Установка частоты дискретизации ЦАП '''

        freqIn = c_double(freqIn)
        freqOut = c_double()

        if not self._zdev.ZSetFreqDAC(self.typeDevice, self.numberDSP, freqIn, byref(freqOut)):
            return freqOut.value

    def ZGetExtFreqADC(self):
        ''' Опрос текущей опорной частоты АЦП '''

        freq = c_double()

        if not self._zdev.ZGetExtFreqADC(self.typeDevice, self.numberDSP, byref(freq)):
            return freq.value

    def ZGetExtFreqDAC(self):
        ''' Опрос текущей опорной частоты ЦАП '''

        freq = c_double()

        if not self._zdev.ZGetExtFreqDAC(self.typeDevice, self.numberDSP, byref(freq)):
            return freq.value

    def ZSetExtFreqADC(self, extFreq):
        ''' Установка значения внешней опорной частоты АЦП '''

        extFreq = c_double(extFreq)

        return not self._zdev.ZSetExtFreqADC(self.typeDevice, self.numberDSP, extFreq)

    def ZSetExtFreqDAC(self, extFreq):
        ''' Установка значения внешней опорной частоты ЦАП '''

        extFreq = c_double(extFreq)

        return not self._zdev.ZSetExtFreqDAC(self.typeDevice, self.numberDSP, extFreq)

    def ZGetEnableExtFreq(self):
        ''' Прочитать статус синхронизации по внешней частоте (устаревшая функция) '''

        enable = c_long()

        if not self._zdev.ZGetEnableExtFreq(self.typeDevice, self.numberDSP, byref(enable)):
            return enable.value

    def ZSetEnableExtFreq(self, enable):
        ''' Вкл./выкл. синхронизации по внешней частоте (устаревшая функция) '''

        enable = c_long(enable)

        return not self._zdev.ZSetEnableExtFreq(self.typeDevice, self.numberDSP, enable)

    def ZGetEnableExtStart(self):
        ''' Прочитать статус внешнего запуска (устаревшая функция) '''

        enable = c_long()

        if not self._zdev.ZGetEnableExtStart(self.typeDevice, self.numberDSP, byref(enable)):
            return enable.value

    def ZSetEnableExtStart(self, enable):
        ''' Вкл./выкл. внешнего запуска (устаревшая функция) '''

        enable = c_long(enable)

        return not self._zdev.ZSetEnableExtStart(self.typeDevice, self.numberDSP, enable)

# Управление каналами ввода (вывода) АЦП/ЦАП

    def ZGetNumberInputADC(self):
        ''' Опрос количества включенных каналов АЦП '''

        channel = c_long()

        if not self._zdev.ZGetNumberInputADC(self.typeDevice, self.numberDSP, byref(channel)):
            return channel.value

    def ZGetNumberOutputDAC(self):
        ''' Опрос количества включенных каналов ЦАП '''

        channel = c_long()

        if not self._zdev.ZGetNumberOutputDAC(self.typeDevice, self.numberDSP, byref(channel)):
            return channel.value

    def ZGetInputADC(self, channel):
        ''' Опрос включен ли заданный канал АЦП '''

        enable = c_long()
        channel = c_long(channel)

        if not self._zdev.ZGetInputADC(self.typeDevice, self.numberDSP, channel, byref(enable)):
            return enable.value

    def ZGetOutputDAC(self, channel):
        ''' Опрос включен ли заданный канал ЦАП '''

        enable = c_long()
        channel = c_long(channel)

        if not self._zdev.ZGetOutputDAC(self.typeDevice, self.numberDSP, channel, byref(enable)):
            return enable.value

    def ZSetInputADC(self, channel, enable):
        ''' Включить/выключить заданный канал АЦП '''

        enable = c_long(enable)
        channel = c_long(channel)

        return not self._zdev.ZSetInputADC(self.typeDevice, self.numberDSP, channel, enable)

    def ZSetOutputDAC(self, channel, enable):
        ''' Включить/выключить заданный канал ЦАП '''

        enable = c_long(enable)
        channel = c_long(channel)

        return not self._zdev.ZSetOutputDAC(self.typeDevice, self.numberDSP, channel, enable)

    def ZGetInputDiffADC(self, channel):
        ''' Опрос дифференциального режима заданного канала для ввода АЦП '''

        enable = c_long()
        channel = c_long(channel)

        if not self._zdev.ZGetInputDiffADC(self.typeDevice, self.numberDSP, channel, byref(enable)):
            return enable.value

    def ZSetInputDiffADC(self, channel, enable):
        ''' Установить-сбросить заданный канал для ввода в дифференциальный режим АЦП '''

        enable = c_long(enable)
        channel = c_long(channel)

        return not self._zdev.ZSetInputDiffADC(self.typeDevice, self.numberDSP, channel, enable)

# Управление коэффициентами усиления АЦП

    def ZGetListAmplifyADC(self):
        ''' Получение списка возможных коэффициентов усиления АЦП '''

        next = c_long(0)
        amplify = c_double()
        amplify_list = []

        i = 0
        while True:
            try:
                self._zdev.ZGetListAmplifyADC(self.typeDevice, self.numberDSP, next, byref(amplify))
                amplify_list.append(amplify.value)
            except Exception as err:
                break
            else:
                i += 1
                next = c_long(i)

        return amplify_list

    def ZSetNextAmplifyADC(self, channel, next):
        ''' Установка большего или меньшего коэффициента усиления из списка выбранного канала АЦП '''

        next = c_long(next)
        channel = c_long(channel)
        amplify = c_double()

        if not self._zdev.ZSetNextAmplifyADC(self.typeDevice, self.numberDSP, channel, next, byref(amplify)):
            return amplify.value

    def ZGetAmplifyADC(self, channel):
        ''' Опрос коэффициента усиления выбранного канала АЦП '''

        amplify = c_double()
        channel = c_long(channel)

        if not self._zdev.ZGetAmplifyADC(self.typeDevice, self.numberDSP, channel, byref(amplify)):
            return amplify.value

    def ZSetAmplifyADC(self, channel, amplifyIn):
        ''' Установка коэффициента усиления выбранного канала АЦП '''

        amplifyIn = c_double(amplifyIn)
        amplifyOut = c_double()
        channel = c_long(channel)

        if not self._zdev.ZSetAmplifyADC(self.typeDevice, self.numberDSP, channel, amplifyIn, byref(amplifyOut)):
            return amplifyOut.value

# Управление коэффициентами усиления ПУ 8/10

    def ZGetListPreAmplifyADC(self):
        ''' Получение списка возможных коэффициентов усиления предварительного усилителя '''

        next = c_long(0)
        amplify = c_double()
        amplify_list = []

        i = 0
        while True:
            try:
                self._zdev.ZGetListPreAmplifyADC(self.typeDevice, self.numberDSP, next, byref(amplify))
                amplify_list.append(amplify.value)
            except Exception as err:
                break
            else:
                i += 1
                next = c_long(i)

        return amplify_list

    def ZSetNextPreAmplifyADC(self, channel, next):
        ''' Установка большего или меньшего коэффициента усиления из списка предварительного усилителя '''

        next = c_long(next)
        channel = c_long(channel)
        amplify = c_double()

        if not self._zdev.ZSetNextPreAmplifyADC(self.typeDevice, self.numberDSP, channel, next, byref(amplify)):
            return amplify.value

    def ZSetPreAmplifyADC(self, channel, amplifyIn):
        ''' Установка коэффициента усиления предварительного усилителя выбранного канала '''

        amplifyIn = c_double(amplifyIn)
        amplifyOut = c_double()
        channel = c_long(channel)

        if not self._zdev.ZSetPreAmplifyADC(self.typeDevice, self.numberDSP, channel, amplifyIn, byref(amplifyOut)):
            return amplifyOut.value

    def ZGetPreAmplifyADC(self, channel):
        ''' Опрос коэффициента усиления предварительного усилителя выбранного канала '''

        amplify = c_double()
        channel = c_long(channel)

        if not self._zdev.ZGetPreAmplifyADC(self.typeDevice, self.numberDSP, channel, byref(amplify)):
            return amplify.value

# Управление коэффициентами ослабления аттенюатора ЦАП

    def ZGetAttenDAC(self, channel):
        ''' Опрос коэффициента ослабления аттенюатора выбранного канала '''

        reduction = c_double()
        channel = c_long(channel)

        if not self._zdev.ZGetAttenDAC(self.typeDevice, self.numberDSP, channel, byref(reduction)):
            return reduction.value

    def ZSetAttenDAC(self, channel, reductionIn):
        ''' Установка коэффициента ослабления аттенюатора выбранного канала '''

        reductionIn = c_double(reductionIn)
        reductionOut = c_double()
        channel = c_long(channel)

        if not self._zdev.ZSetAttenDAC(self.typeDevice, self.numberDSP, channel, reductionIn, byref(reductionOut)):
            return reductionOut.value

# Управление процессом перекачки данных

    def ZSetExtCycleDAC(self, enable):
        ''' Установка режима внешней подкачки данных или внутренней генерации сигналов '''

        enable = c_long(enable)

        return not self._zdev.ZSetExtCycleDAC(self.typeDevice, self.numberDSP, enable)

    def ZGetInterruptADC(self):
        ''' Опрос размера буфера для перекачки данных АЦП '''

        size = c_long()

        if not self._zdev.ZGetInterruptADC(self.typeDevice, self.numberDSP, byref(size)):
            return size.value

    def ZGetInterruptDAC(self):
        ''' Опрос размера буфера для перекачки данных ЦАП '''

        size = c_long()

        if not self._zdev.ZGetInterruptDAC(self.typeDevice, self.numberDSP, byref(size)):
            return size.value

    def ZGetMaxInterruptADC(self):
        ''' Опрос максимального размера буфера для перекачки данных АЦП '''

        size = c_long()

        if not self._zdev.ZGetMaxInterruptADC(self.typeDevice, self.numberDSP, byref(size)):
            return size.value

    def ZGetMaxInterruptDAC(self):
        ''' Опрос максимального размера буфера для перекачки данных ЦАП '''

        size = c_long()

        if not self._zdev.ZGetMaxInterruptDAC(self.typeDevice, self.numberDSP, byref(size)):
            return size.value

    def ZSetInterruptADC(self, size):
        ''' Установка размера буфера для перекачки данных АЦП '''

        size = c_long(size)

        return not self._zdev.ZSetInterruptADC(self.typeDevice, self.numberDSP, size)

    def ZSetInterruptDAC(self, size):
        ''' Установка размера буфера для перекачки данных ЦАП '''

        size = c_long(size)

        return not self._zdev.ZSetInterruptDAC(self.typeDevice, self.numberDSP, size)

    def ZSetBufferSizeADC(self, size):
        ''' Задать размер буфера АЦП в ОЗУ ПК '''

        size = c_long(size)

        return not self._zdev.ZSetBufferSizeADC(self.typeDevice, self.numberDSP, size)

    def ZSetBufferSizeDAC(self, size):
        ''' Задать размер буфера ЦАП в ОЗУ ПК '''

        size = c_long(size)

        return not self._zdev.ZSetBufferSizeDAC(self.typeDevice, self.numberDSP, size)

    def ZGetBufferADC(self):
        ''' Запросить буфер в ОЗУ ПК для АЦП'''

        buff_ptr = pointer(c_long())
        size = c_long()

        if not self._zdev.ZGetBufferADC(self.typeDevice, self.numberDSP, byref(buff_ptr), byref(size)):
            return buff_ptr, size.value

    def ZGetBufferDAC(self):
        ''' Запросить буфер в ОЗУ ПК для ЦАП'''

        buff_ptr = pointer(c_long())
        size = c_long()

        if not self._zdev.ZGetBufferDAC(self.typeDevice, self.numberDSP, byref(buff_ptr), byref(size)):
            return buff_ptr, size.value

    def ZRemBufferADC(self, buff_ptr):
        ''' Освободить буфер в ОЗУ ПК для АЦП '''

        return not self._zdev.ZRemBufferADC(self.typeDevice, self.numberDSP, byref(buff_ptr))

    def ZRemBufferDAC(self, buff_ptr):
        ''' Освободить буфер в ОЗУ ПК для ЦАП '''

        return not self._zdev.ZRemBufferDAC(self.typeDevice, self.numberDSP, byref(buff_ptr))

    def ZSetCycleSampleADC(self, enable):
        ''' Установка циклического или одноразового накопления АЦП '''

        enable = c_long(enable)

        return not self._zdev.ZSetCycleSampleADC(self.typeDevice, self.numberDSP, enable)

    def ZSetCycleSampleDAC(self, enable):
        ''' Установка циклического или одноразового накопления ЦАП '''

        enable = c_long(enable)

        return not self._zdev.ZSetCycleSampleDAC(self.typeDevice, self.numberDSP, enable)

    def ZGetLastDataADC(self, channel, size):
        ''' Пересылка последних накопленных данных АЦП '''

        buff_ptr = c_void_p()
        channel = c_long(channel)
        size = c_long(size)

        return not self._zdev.ZGetLastDataADC(self.typeDevice, self.numberDSP, channel, buff_ptr, size)

    def ZGetPointerADC(self):
        ''' Чтение указателя буфера в ОЗУ ПК для АЦП '''

        ptr = c_long()

        if not self._zdev.ZGetPointerADC(self.typeDevice, self.numberDSP, byref(ptr)):
            return ptr.value

    def ZGetPointerDAC(self):
        ''' Чтение указателя буфера в ОЗУ ПК для ЦАП '''

        ptr = c_long()

        if not self._zdev.ZGetPointerDAC(self.typeDevice, self.numberDSP, byref(ptr)):
            return ptr.value

    def ZGetFlag(self):
        ''' Опрос флага прерываний '''

        flag = c_ulong()

        if not self._zdev.ZGetFlag(self.typeDevice, self.numberDSP, byref(flag)):
            return flag.value

    def ZGetStartADC(self):
        ''' Опрос состояния накопления данных АЦП '''

        status = c_long()

        if not self._zdev.ZGetStartADC(self.typeDevice, self.numberDSP, byref(status)):
            return status.value

    def ZGetStartDAC(self):
        ''' Опрос состояния накопления данных ЦАП '''

        status = c_long()

        if not self._zdev.ZGetStartDAC(self.typeDevice, self.numberDSP, byref(status)):
            return status.value

    def ZStartADC(self):
        ''' Старт накопления данных АЦП '''

        return not self._zdev.ZStartADC(self.typeDevice, self.numberDSP)

    def ZStartDAC(self):
        ''' Старт накопления данных ЦАП '''

        return not self._zdev.ZStartDAC(self.typeDevice, self.numberDSP)

    def ZStopADC(self):
        ''' Останов накопления данных АЦП '''

        return not self._zdev.ZStopADC(self.typeDevice, self.numberDSP)

    def ZStopDAC(self):
        ''' Останов накопления данных ЦАП '''

        return not self._zdev.ZStopDAC(self.typeDevice, self.numberDSP)

# Управление модулем HCP

    def ZFindHCPADC(self):
        ''' Опрос поддержки и подключения модуля HCP '''

        present = c_long()

        if not self._zdev.ZFindHCPADC(self.typeDevice, self.numberDSP, byref(present)):
            return present.value

    def ZGetHCPADC(self, channel):
        ''' Опрос режима работы заданного канала модуля HCP '''

        enable = c_long()
        channel = c_long(channel)

        if not self._zdev.ZGetHCPADC(self.typeDevice, self.numberDSP, channel, byref(enable)):
            return enable.value

    def ZSetHCPADC(self, channel, enable):
        ''' Установка режима работы заданного канала модуля HCP '''

        enable = c_long(enable)
        channel = c_long(channel)

        return not self._zdev.ZSetHCPADC(self.typeDevice, self.numberDSP, channel, enable)

# Управление цифровым портом

    def ZGetDigOutEnable(self):
        ''' Опрос маски выходов цифрового порта '''

        enableMask = c_ulong()

        if not self._zdev.ZGetDigOutEnable(self.typeDevice, self.numberDSP, byref(enableMask)):
            return enableMask.value

    def ZSetDigOutEnable(self, enableMask):
        ''' Установить маску выходов цифрового порта '''

        enableMask = c_ulong(enableMask)

        return not self._zdev.ZSetDigOutEnable(self.typeDevice, self.numberDSP, enableMask)

    def ZGetDigInput(self):
        ''' Прочитать данные с входов цифрового порта '''

        digitalInput = c_ulong()

        if not self._zdev.ZGetDigInput(self.typeDevice, self.numberDSP, byref(digitalInput)):
            return digitalInput.value

    def ZGetDigOutput(self):
        ''' Прочитать данные, выдаваемые на выходы цифрового порта '''

        digitalOutput = c_ulong()

        if not self._zdev.ZGetDigOutput(self.typeDevice, self.numberDSP, byref(digitalOutput)):
            return digitalOutput.value

    def ZSetDigOutput(self, digitalOutput):
        ''' Записать данные в цифровой порт '''

        digitalOutput = c_ulong(digitalOutput)

        return not self._zdev.ZSetDigOutput(self.typeDevice, self.numberDSP, digitalOutput)


__all__ = [ "ZET" ]

#! /usr/bin/env python
# -*- coding: utf-8 -*-

''' Пример записи синусоидального сигнала в 1-ый канал ЦАП '''


from __future__ import print_function
from time import sleep
from math import sin, pi
from zet.zet import ZET, ZET230


if __name__ == "__main__":
    with ZET(device=ZET230, dsp=0) as zdev:     # либо zdev.ZOpen() в начале и zdev.ZClose() в конце
        print("ZGetEnableDAC = {}".format(zdev.ZGetEnableDAC()))
        print("ZSetOutputDAC = {}".format(zdev.ZSetOutputDAC(channel=0, enable=True)))
        print("ZGetNumberOutputDAC = {}".format(zdev.ZGetNumberOutputDAC()))

        resolution = zdev.ZGetDigitalResolutionDAC()
        print("ZGetDigitalResolutionDAC = {}".format(resolution))
        words = zdev.ZGetWordsDAC()
        print("ZGetWordsDAC = {}".format(words))
        freq = zdev.ZGetFreqDAC()
        print("ZGetFreqDAC = {}".format(freq))
        sizeInterruptBufferDAC = zdev.ZGetInterruptDAC()
        print("ZGetInterruptDAC = {}".format(sizeInterruptBufferDAC))
        attenDAC0 = zdev.ZSetAttenDAC(channel=0, reduction_in=0.1)
        print("ZSetAttenDAC = {}".format(attenDAC0))
        buff, sizeBufferDAC = zdev.ZGetBufferDAC()
        print("ZGetBufferDAC = {}, {}".format(buff, sizeBufferDAC))

        amplitude = 1.0         # Амплитуда синусоидального сигнала (Водьты)
        freq_sine = 1.0         # Частота синусоидального сигнала (Гц)

        current_sine_time = 0.0
        response_time = 250.0

        size_packet = int(freq * response_time / 1000.0 * words)
        if size_packet < 2.0*sizeInterruptBufferDAC:
            size_packet = int(2 * sizeInterruptBufferDAC)
        if size_packet > sizeBufferDAC/2.0:
            size_packet = int(sizeBufferDAC / 2.0)

        amplitude = amplitude / (resolution * attenDAC0)
        delta_sine_time = 2.0 * pi * freq_sine / freq

        size = int(2.0 * size_packet / words)
        for i in range(size):
            volt0 = amplitude * sin(current_sine_time)
            buff[i] = int(volt0)
            current_sine_time += delta_sine_time

        pointer_cycle = 2 * size_packet

        print("ZStartDAC = {}".format(zdev.ZStartDAC()))
        print("ZStartADC = {}".format(zdev.ZStartADC()))

        pointer_old = 0
        while True:
            try:
                sleep(0.02)

                pointer = zdev.ZGetPointerDAC()
                print("pointer = {:7d}, pointer_cycle = {:7d}".format(pointer, pointer_cycle), end='\r')

                if pointer_cycle - pointer > size_packet:
                    continue
                if (pointer > pointer_cycle) and (sizeBufferDAC - pointer + pointer_cycle > size_packet):
                    continue

                pointer_old = pointer
                size = size_packet

                if pointer_cycle + size_packet > sizeBufferDAC:
                    size = sizeBufferDAC - pointer_cycle
                size = int(size / words)

                for i in range(size):
                    volt0 = amplitude * sin(current_sine_time)
                    buff[pointer_cycle//words + i] = int(volt0)
                    current_sine_time += delta_sine_time

                pointer_cycle += words * size

                if pointer_cycle >= sizeBufferDAC:
                    pointer_cycle = 0

                if size < size_packet/words:
                    size = int(size_packet/words - size)

                    for i in range(size):
                        volt0 = amplitude * sin(current_sine_time)
                        buff[pointer_cycle//words + i] = int(volt0)
                        current_sine_time += delta_sine_time

                    pointer_cycle += words * size
            except KeyboardInterrupt:
                break
        print()
        print("ZStopDAC = {}".format(zdev.ZStopDAC()))
        print("ZStopADC = {}".format(zdev.ZStopADC()))
        print("ZRemBufferDAC = {}".format(zdev.ZRemBufferDAC(buff)))

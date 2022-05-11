#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from time import sleep
from zet.zet import ZET, ZET230


if __name__ == "__main__":
    ldev = ZET(device=ZET230, dsp=0)
    with ldev:      # либо ldev.ZOpen() в начале и ldev.ZClose() в конце
        print ("ZSetOutputDAC = {}".format(ldev.ZSetOutputDAC(channel=0, enable=True)))
        resolution = ldev.ZGetDigitalResolutionDAC()
        print ("ZGetDigitalResolutionDAC = {}".format(resolution))
        freq = ldev.ZGetFreqDAC()
        print ("ZGetFreqDAC = {}".format(freq))
        channels = ldev.ZGetNumberOutputDAC()
        print ("ZGetNumberOutputDAC = {}".format(channels))
        words = ldev.ZGetWordsDAC()
        print ("ZGetWordsDAC = {}".format(words))
        sizeInterruptBufferDAC = ldev.ZGetInterruptDAC()
        print ("ZGetInterruptDAC = {}".format(sizeInterruptBufferDAC))
        buff, sizeBufferDAC = ldev.ZGetBufferDAC()
        print ("ZGetBufferADC = {}, {}".format(buff, sizeBufferDAC))

        sleepTime = 250.0
        size_packet = int(freq * sleepTime / 1000.0 * words)
        if size_packet < 2.0*sizeInterruptBufferDAC:
            size_packet = int(2 * sizeInterruptBufferDAC)
        if size_packet > sizeBufferDAC/2.0:
            size_packet = int(sizeBufferDAC / 2.0)

        amplitude = 1.0         # Амплитуда сигнала (Водьты)

        size = int(2.0 * size_packet / words)
        for i in range(size):
            buff[i] = int(amplitude)

        pointer_cycle = 2 * size_packet

        print ("ZStartDAC = {}".format(ldev.ZStartDAC()))
        print ("ZStartADC = {}".format(ldev.ZStartADC()))

        pointer_old = 0
        while True:
            try:
                sleep(0.02)

                pointer = ldev.ZGetPointerDAC()
                print ("pointer = {:7d}, pointer_cycle = {:7d}".format(pointer, pointer_cycle), end='\r')

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
                    buff[pointer_cycle//words + i] = int(amplitude)

                pointer_cycle += words * size

                if pointer_cycle >= sizeBufferDAC:
                    pointer_cycle = 0

                if size < size_packet/words:
                    size = int(size_packet/words - size)

                    for i in range(size):
                        buff[pointer_cycle//words + i] = int(amplitude)

                    pointer_cycle += words * size
            except KeyboardInterrupt:
                break
        print ()
        print ("ZStopDAC = {}".format(ldev.ZStopDAC()))
        print ("ZStopADC = {}".format(ldev.ZStopADC()))
        print ("ZRemBufferDAC = {}".format(ldev.ZRemBufferDAC(buffer=buff)))

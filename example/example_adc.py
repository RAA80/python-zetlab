#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from time import sleep
from zet.zet import ZET, ZET230


if __name__ == "__main__":
    with ZET(device=ZET230, dsp=0) as zdev:     # либо zdev.ZOpen() в начале и zdev.ZClose() в конце
        print("ZSetInputADC = {}".format(zdev.ZSetInputADC(channel=0, enable=True)))
        resolution = zdev.ZGetDigitalResolChanADC(channel=0)
        print("ZGetDigitalResolChanADC = {}".format(resolution))
        amplify = zdev.ZGetAmplifyADC(channel=0)
        print("ZGetAmplifyADC = {}".format(amplify))
        channels = zdev.ZGetNumberInputADC()
        print("ZGetNumberInputADC = {}".format(channels))
        words = zdev.ZGetWordsADC()
        print("ZGetWordsADC = {}".format(words))
        buff, size = zdev.ZGetBufferADC()
        print("ZGetBufferADC = {}, {}".format(buff, size))
        print("ZStartADC = {}".format(zdev.ZStartADC()))

        pointer_old = 0
        while True:
            try:
                pointer = zdev.ZGetPointerADC()

                if pointer == pointer_old:
                    continue
                pointer_old = pointer

                if pointer - words*channels < 0:
                    pointer = size + pointer - words*channels
                else:
                    pointer -= words*channels

                volt0 = resolution * buff[pointer // words] / amplify

                print("pointer = {:7d}, volts = {:.05f}".format(pointer, volt0), end='\r')

                sleep(0.02)
            except KeyboardInterrupt:
                break
        print()
        print("ZStopADC = {}".format(zdev.ZStopADC()))
        print("ZRemBufferADC = {}".format(zdev.ZRemBufferADC(buff)))

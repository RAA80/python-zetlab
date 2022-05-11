#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from time import sleep
from zet.zet import ZET, ZET230


if __name__ == "__main__":
    ldev = ZET(device=ZET230, dsp=0)
    with ldev:      # либо ldev.ZOpen() в начале и ldev.ZClose() в конце
        print ("ZSetInputADC = {}".format(ldev.ZSetInputADC(channel=0, enable=True)))
        resolution = ldev.ZGetDigitalResolChanADC(channel=0)
        print ("ZGetDigitalResolChanADC = {}".format(resolution))
        amplify = ldev.ZGetAmplifyADC(channel=0)
        print ("ZGetAmplifyADC = {}".format(amplify))
        channels = ldev.ZGetNumberInputADC()
        print ("ZGetNumberInputADC = {}".format(channels))
        words = ldev.ZGetWordsADC()
        print ("ZGetWordsADC = {}".format(words))
        buff, size = ldev.ZGetBufferADC()
        print ("ZGetBufferADC = {}, {}".format(buff, size))
        print ("ZStartADC = {}".format(ldev.ZStartADC()))

        pointer_old = 0
        while True:
            try:
                pointer = ldev.ZGetPointerADC()

                if pointer == pointer_old:
                    continue
                pointer_old = pointer

                if pointer - words*channels < 0:
                    pointer = size + pointer - words*channels
                else:
                    pointer -= words*channels

                volt0 = resolution * buff[pointer // words] / amplify

                print ("pointer = {:7d}, volts = {:.05f}".format(pointer, volt0), end='\r')

                sleep(0.02)
            except KeyboardInterrupt:
                break
        print ()
        print ("ZStopADC = {}".format(ldev.ZStopADC()))
        print ("ZRemBufferADC = {}".format(ldev.ZRemBufferADC(buff)))

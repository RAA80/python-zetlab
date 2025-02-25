#! /usr/bin/env python3

"""Пример использования библиотеки."""

import contextlib
from time import sleep

from zet.client import Z_DEVICE, ZET

if __name__ == "__main__":
    with ZET(device=Z_DEVICE.ZET230, dsp=0) as zdev:    # либо zdev.ZOpen() в начале и zdev.ZClose() в конце
        print(f"ZSetInputADC = {zdev.ZSetInputADC(channel=0, enable=True)}")
        resolution = zdev.ZGetDigitalResolChanADC(channel=0)
        print(f"ZGetDigitalResolChanADC = {resolution}")
        amplify = zdev.ZGetAmplifyADC(channel=0)
        print(f"ZGetAmplifyADC = {amplify}")
        channels = zdev.ZGetNumberInputADC()
        print(f"ZGetNumberInputADC = {channels}")
        words = zdev.ZGetWordsADC()
        print(f"ZGetWordsADC = {words}")
        buff, size = zdev.ZGetBufferADC()
        print(f"ZGetBufferADC = {buff}, {size}")
        print(f"ZStartADC = {zdev.ZStartADC()}")

        pointer_old = 0
        with contextlib.suppress(KeyboardInterrupt):
            while True:
                pointer = zdev.ZGetPointerADC()

                if pointer == pointer_old:
                    continue
                pointer_old = pointer

                condition = pointer - words * channels
                pointer = size + condition if condition < 0 else condition

                volt0 = resolution * buff[pointer // words] / amplify

                print(f"pointer = {pointer:7d}, volts = {volt0:.05f}", end="\r")
                sleep(0.02)

        print()
        print(f"ZStopADC = {zdev.ZStopADC()}")
        print(f"ZRemBufferADC = {zdev.ZRemBufferADC(buff)}")

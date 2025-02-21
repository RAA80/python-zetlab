#! /usr/bin/env python3

"""Пример записи синусоидального сигнала в 1-ый канал ЦАП."""

import contextlib
from math import pi, sin
from time import sleep

from zet.client import Z_DEVICE, ZET

if __name__ == "__main__":
    with ZET(device=Z_DEVICE.ZET230, dsp=0) as zdev:    # либо zdev.ZOpen() в начале и zdev.ZClose() в конце
        print(f"ZGetEnableDAC = {zdev.ZGetEnableDAC()}")
        print(f"ZSetOutputDAC = {zdev.ZSetOutputDAC(channel=0, enable=True)}")
        print(f"ZGetNumberOutputDAC = {zdev.ZGetNumberOutputDAC()}")

        resolution = zdev.ZGetDigitalResolutionDAC()
        print(f"ZGetDigitalResolutionDAC = {resolution}")
        words = zdev.ZGetWordsDAC()
        print(f"ZGetWordsDAC = {words}")
        freq = zdev.ZGetFreqDAC()
        print(f"ZGetFreqDAC = {freq}")
        size_interrupt_buffer_dac = zdev.ZGetInterruptDAC()
        print(f"ZGetInterruptDAC = {size_interrupt_buffer_dac}")
        atten_dac0 = zdev.ZSetAttenDAC(channel=0, reduction=0.1)
        print(f"ZSetAttenDAC = {atten_dac0}")
        buff, size_buffer_dac = zdev.ZGetBufferDAC()
        print(f"ZGetBufferDAC = {buff}, {size_buffer_dac}")

        amplitude = 1.0         # Амплитуда синусоидального сигнала (Водьты)
        freq_sine = 1.0         # Частота синусоидального сигнала (Гц)

        current_sine_time = 0.0
        response_time = 250.0

        size_packet = int(freq * response_time / 1000.0 * words)
        if size_packet < 2.0 * size_interrupt_buffer_dac:
            size_packet = int(2 * size_interrupt_buffer_dac)
        if size_packet > size_buffer_dac / 2.0:
            size_packet = int(size_buffer_dac / 2.0)

        amplitude /= (resolution * atten_dac0)
        delta_sine_time = 2.0 * pi * freq_sine / freq

        size = int(2.0 * size_packet / words)
        for i in range(size):
            volt0 = amplitude * sin(current_sine_time)
            buff[i] = int(volt0)
            current_sine_time += delta_sine_time

        pointer_cycle = 2 * size_packet

        print(f"ZStartDAC = {zdev.ZStartDAC()}")
        print(f"ZStartADC = {zdev.ZStartADC()}")

        pointer_old = 0
        with contextlib.suppress(KeyboardInterrupt):
            while True:
                sleep(0.02)

                pointer = zdev.ZGetPointerDAC()
                print(f"pointer = {pointer:7d}, pointer_cycle = {pointer_cycle:7d}", end="\r")

                if pointer_cycle - pointer > size_packet:
                    continue
                if (pointer > pointer_cycle) and (size_buffer_dac - pointer + pointer_cycle > size_packet):
                    continue

                pointer_old = pointer
                size = size_packet

                if pointer_cycle + size_packet > size_buffer_dac:
                    size = size_buffer_dac - pointer_cycle
                size = int(size / words)

                for i in range(size):
                    volt0 = amplitude * sin(current_sine_time)
                    buff[pointer_cycle // words + i] = int(volt0)
                    current_sine_time += delta_sine_time

                pointer_cycle += words * size

                if pointer_cycle >= size_buffer_dac:
                    pointer_cycle = 0

                if size < size_packet / words:
                    size = int(size_packet / words - size)

                    for i in range(size):
                        volt0 = amplitude * sin(current_sine_time)
                        buff[pointer_cycle // words + i] = int(volt0)
                        current_sine_time += delta_sine_time

                    pointer_cycle += words * size
        print()
        print(f"ZStopDAC = {zdev.ZStopDAC()}")
        print(f"ZStopADC = {zdev.ZStopADC()}")
        print(f"ZRemBufferDAC = {zdev.ZRemBufferDAC(buff)}")

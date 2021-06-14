from typing import List

def load_fonts(memory: List[int]):
    digit = 0x0
    memory[digit + 0] = 0x11110000
    memory[digit + 1] = 0x10010000
    memory[digit + 2] = 0x10010000
    memory[digit + 3] = 0x10010000
    memory[digit + 4] = 0x11110000

    digit = 0x1
    memory[digit + 0] = 0x00100000
    memory[digit + 1] = 0x01100000
    memory[digit + 2] = 0x00100000
    memory[digit + 3] = 0x00100000
    memory[digit + 4] = 0x01110000

    digit = 0x2
    memory[digit + 0] = 0x11110000
    memory[digit + 1] = 0x00010000
    memory[digit + 2] = 0x11110000
    memory[digit + 3] = 0x10000000
    memory[digit + 4] = 0x11110000

    digit = 0x3
    memory[digit + 0] = 0x11110000
    memory[digit + 1] = 0x00010000
    memory[digit + 2] = 0x11110000
    memory[digit + 3] = 0x00010000
    memory[digit + 4] = 0x11110000

    digit = 0x4
    memory[digit + 0] = 0x10010000
    memory[digit + 1] = 0x10010000
    memory[digit + 2] = 0x11110000
    memory[digit + 3] = 0x00010000
    memory[digit + 4] = 0x00010000

    digit = 0x5
    memory[digit + 0] = 0x11110000
    memory[digit + 1] = 0x10000000
    memory[digit + 2] = 0x11110000
    memory[digit + 3] = 0x00010000
    memory[digit + 4] = 0x11110000

    digit = 0x6
    memory[digit + 0] = 0x11110000
    memory[digit + 1] = 0x10000000
    memory[digit + 2] = 0x11110000
    memory[digit + 3] = 0x10010000
    memory[digit + 4] = 0x11110000

    digit = 0x7
    memory[digit + 0] = 0x11110000
    memory[digit + 1] = 0x00010000
    memory[digit + 2] = 0x00100000
    memory[digit + 3] = 0x01000000
    memory[digit + 4] = 0x01000000
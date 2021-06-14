from typing import List

def load_fonts(memory: List[int]):
    digit = 0x0
    memory[digit + 0] = 0b11110000
    memory[digit + 1] = 0b10010000
    memory[digit + 2] = 0b10010000
    memory[digit + 3] = 0b10010000
    memory[digit + 4] = 0b11110000

    digit = 0x1
    memory[digit + 0] = 0b00100000
    memory[digit + 1] = 0b01100000
    memory[digit + 2] = 0b00100000
    memory[digit + 3] = 0b00100000
    memory[digit + 4] = 0b01110000

    digit = 0x2
    memory[digit + 0] = 0b11110000
    memory[digit + 1] = 0b00010000
    memory[digit + 2] = 0b11110000
    memory[digit + 3] = 0b10000000
    memory[digit + 4] = 0b11110000

    digit = 0x3
    memory[digit + 0] = 0b11110000
    memory[digit + 1] = 0b00010000
    memory[digit + 2] = 0b11110000
    memory[digit + 3] = 0b00010000
    memory[digit + 4] = 0b11110000

    digit = 0x4
    memory[digit + 0] = 0b10010000
    memory[digit + 1] = 0b10010000
    memory[digit + 2] = 0b11110000
    memory[digit + 3] = 0b00010000
    memory[digit + 4] = 0b00010000

    digit = 0x5
    memory[digit + 0] = 0b11110000
    memory[digit + 1] = 0b10000000
    memory[digit + 2] = 0b11110000
    memory[digit + 3] = 0b00010000
    memory[digit + 4] = 0b11110000

    digit = 0x6
    memory[digit + 0] = 0b11110000
    memory[digit + 1] = 0b10000000
    memory[digit + 2] = 0b11110000
    memory[digit + 3] = 0b10010000
    memory[digit + 4] = 0b11110000

    digit = 0x7
    memory[digit + 0] = 0b11110000
    memory[digit + 1] = 0b00010000
    memory[digit + 2] = 0b00100000
    memory[digit + 3] = 0b01000000
    memory[digit + 4] = 0b01000000
 #https://en.wikipedia.org/wiki/CHIP-8
 #http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#font
import sys
from typing import List, NewType
import random
import math
import pygame
from datetime import datetime

from pygame.constants import( K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_a, K_b, K_c, K_d, K_e, K_f,
                              K_KP0, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9)

byte = NewType("byte", int)
address = byte

class Machine:
    program_counter: address = 0
    memory: List[byte] = [0] * 4096
    registers: List[byte] = [0] * 0x10
    I : int = 0         #16 bits
    stack : List[int] = []
    display = [[False]*64 for _ in range(32)]   # array of 32 rows

    def reset_delay_timer(self, duration):
        self.delay_timer_duration = duration
        self.delay_timer_started_at = datetime.now()

    def current_delay_timer_duration(self):
        elapsed = datetime.now() - self.delay_timer_started_at
        one_hertz_in_ms = 1000 / 60
        elapsed_ms = elapsed.microseconds / 1000
        elapsed_hertz = elapsed_ms / one_hertz_in_ms
        if elapsed_hertz > self.delay_timer_duration:
            return 0
        else:
            return elapsed_hertz

    def load_rom(self, filename: str):
        with open(filename, "rb") as f:
            bytes_read = f.read()

        self.memory = [0] * 4096
        for i, b in enumerate(bytes_read):
            self.memory[i+0x200] = b    
        self.program_counter=0x200

    def __str__(self):
        line = f"program_counter = {self.program_counter}\r\n"
        line = line + f"I = {self.I}\r\n"
        line = line + f"registers = {self.registers}\r\n"
        return line

class OpCode():
    """
        Given the memory ABCD:
            + The most significant byte (msb) would be AB
            + This is split into two nibbles n0 = A and n1 = B
            + The least significant byte (lsb) would be CD
            + This is split into two nibbles n2 = C and n3 = D
    """
    def __init__(self, memory: List[byte], program_counter: address):
        self.msb = memory[program_counter]
        self.lsb = memory[program_counter+1]        
        self.n0 =  math.floor(self.msb / 16)
        self.n1 =  self.msb % 16
        self.n2 =  math.floor(self.lsb / 16)
        self.n3 =  self.lsb % 16

    def __str__(self):
        return f"{hex(self.msb)}-{hex(self.lsb)}"

def display_screen(machine: Machine):
    print('=' * 64)
    for row in range(32):
        line = ""
        for column in range(64):
            if machine.display[row][column]:
                line = line + "*"
            else:
                line = line + " "
        print(line)
    print('=' * 64)

def debug_print(msg):
    pass

def load_fonts(machine: Machine):
    #0
    machine.memory[0] = 0x11110000
    machine.memory[1] = 0x10010000
    machine.memory[2] = 0x10010000
    machine.memory[3] = 0x10010000
    machine.memory[4] = 0x11110000

    #1
    machine.memory[5] = 0x00100000
    machine.memory[6] = 0x01100000
    machine.memory[7] = 0x00100000
    machine.memory[8] = 0x00100000
    machine.memory[9] = 0x01110000

    #TODO:

def font_address(character: int) -> int:
    # Each font takes 5 bytes (memory locations)
    return character * 5


def step(machine: Machine, draw_screen_callback, is_key_pressed):
    opCode = OpCode(machine.memory, machine.program_counter)
    debug_print(f"{machine.program_counter}:: Running {opCode}")

    #0nnn

    if opCode.n0 == 0x0 and opCode.lsb == 0xE0:
        machine.display = [[False] * 64] * 32
        debug_print(f"Clear screen")

    elif opCode.n0 == 0x0 and opCode.lsb == 0xEE:
        # 00EE #1002:: Running 0x0-0xee
        machine.program_counter = machine.stack.pop()
        debug_print(f"Return to {machine.program_counter}")

    elif opCode.n0 == 0x1:
        # 1NNN	Flow	goto NNN;	Jumps to address NNN.        
        machine.program_counter = (opCode.n1 * 256) + (opCode.n2 * 16) + opCode.n3
        debug_print(f"Goto {machine.program_counter }")

    elif opCode.n0 == 0x2:
        #2NNN	Flow	*(0xNNN)()	Calls subroutine at NNN.
        machine.stack.append(machine.program_counter + 2)   # Not sure if we should implement PC here on the return.
        machine.program_counter = (opCode.n1 * 256) + (opCode.n2 * 16) + opCode.n3
        debug_print(f"Jumping to {machine.program_counter}")

    elif opCode.n0 == 0x3:
        # 3XNN	Cond	if(Vx==NN)	Skips the next instruction if VX equals NN. (Usually the next instruction is a jump to skip a code block);
        debug_print(f"jump if {machine.registers[opCode.n1]} == {opCode.lsb}")
        if machine.registers[opCode.n1] == opCode.lsb:
            machine.program_counter = machine.program_counter + 4
        else:
            machine.program_counter = machine.program_counter + 2

    elif opCode.n0 == 0x4:
        if machine.registers[opCode.n1] != opCode.lsb:
            machine.program_counter = machine.program_counter + 4
        else:
            machine.program_counter = machine.program_counter + 2

    elif opCode.n0 == 0x5:
        if machine.registers[opCode.n1] == machine.registers[opCode.n2]:
            machine.program_counter = machine.program_counter + 4
        else:
            machine.program_counter = machine.program_counter + 2

    elif opCode.n0 == 0x6:
        # Vx = N
        debug_print(f"Set V[{hex(opCode.n1)}] to {opCode.lsb}")
        machine.registers[opCode.n1] = opCode.lsb
        machine.program_counter = machine.program_counter + 2

    elif opCode.n0 == 0x7:
        # Vx += N
        machine.registers[opCode.n1] = (machine.registers[opCode.n1] + opCode.lsb) % 0x100
        machine.program_counter = machine.program_counter + 2

    elif opCode.n0 == 0x8:
        if opCode.n3 == 0x0:
            # Assignment
            machine.registers[opCode.n1] = machine.registers[opCode.n2]
            machine.program_counter = machine.program_counter + 2

        elif opCode.n3 == 0x1:
            # Bitwise or  (Vx=Vx|Vy)
            machine.registers[opCode.n1] = machine.registers[opCode.n1] | machine.registers[opCode.n2]
            machine.program_counter = machine.program_counter + 2

        elif opCode.n3 == 0x2:
            # Bitwise and  (Vx=Vx&Vy)
            machine.registers[opCode.n1] = machine.registers[opCode.n1] & machine.registers[opCode.n2]
            machine.program_counter = machine.program_counter + 2

        elif opCode.n3 == 0x3:
            # Vx=Vx^Vy	Sets VX to VX xor VY.
            machine.registers[opCode.n1] = machine.registers[opCode.n1] ^ machine.registers[opCode.n2]
            machine.program_counter = machine.program_counter + 2

        elif opCode.n3 == 0x4:
            # Vx += V	Adds VY to VX. VF is set to 1 when there's a carry, and to 0 when there is not.
            machine.registers[opCode.n1] = machine.registers[opCode.n1] + machine.registers[opCode.n2]
            machine.registers[0xF] = 1 if machine.registers[opCode.n1] > 0xFF else 0
            machine.registers[opCode.n1] = machine.registers[opCode.n1] % 0x100
            machine.program_counter = machine.program_counter + 2

        elif opCode.n3 == 0x5:
            # Vx -= V
            machine.registers[opCode.n1] = machine.registers[opCode.n1] - machine.registers[opCode.n2]
            machine.registers[0xF] = 1 if machine.registers[opCode.n1] < 0x0 else 0
            machine.program_counter = machine.program_counter + 2

        #8xy6
        #8xy7
        #8xye

        else:
            raise ValueError(f"Unknown opcode {hex(opCode.msb)}-{hex(opCode.lsb)}")

    elif opCode.n0 == 0x9 and opCode.n3 == 0x0:
        vx = machine.registers[opCode.n1]
        vy = machine.registers[opCode.n2]
        if vx != vy:
            machine.program_counter = machine.program_counter + 4
        else:
            machine.program_counter = machine.program_counter + 2

    elif opCode.n0 == 0xA:
        #ANNN	MEM	I = NN	Sets I to the address NNN.
        machine.I = (opCode.n1 * 256) + (opCode.n2 * 16) + opCode.n3
        machine.program_counter = machine.program_counter + 2

    elif opCode.n0 == 0xB:
        #Jumps to the address NNN plus V0.
        v0 = machine.registers[0x0]
        address = (opCode.n1 * 256) + (opCode.n2 * 16) + opCode.n3
        machine.program_counter = address + v0

    elif opCode.n0 == 0xC:
        machine.registers[opCode.n1] =  random.randint(0,255) & opCode.lsb
        machine.program_counter = machine.program_counter + 2

    elif opCode.n0 == 0xD:
        # DXYN	Disp	draw(Vx,Vy,N)
        # Draws a sprite at coordinate (VX, VY) that has a width of 8 pixels and a height of N+1 pixels.
        # Each row of 8 pixels is read as bit-coded starting from memory location I; I value does not
        # change after the execution of this instruction. As described above, VF is set to 1 if any screen pixels
        #  are flipped from set to unset when the sprite is drawn, and to 0 if that does not happen
        vX = machine.registers[opCode.n1]
        vY = machine.registers[opCode.n2]
        N = opCode.n3

        machine.registers[0xF] = 0
        masks = [0b10000000,0b01000000,0b00100000,0b00010000,
                 0b00001000,0b00000100,0b00000010,0b00000001]
        for row in range(0, N):
            bit_map = machine.memory[machine.I + row]

            for column in range(0,8):
                mask = masks[column]
                bit = (mask & bit_map) == mask
                current = machine.display[(row + vY) % 32][(column + vX) % 64]
                new_value = current ^ bit

                if current and not new_value:
                    # At least one pixel is being flipped from 1 to 0
                    machine.registers[0xF] = 1

                machine.display[(row + vY) % 32][(column + vX) % 64] = new_value
        draw_screen_callback(machine)
        machine.program_counter = machine.program_counter + 2

    elif opCode.n0 == 0xE and opCode.lsb == 0x9E:
        key = machine.registers[opCode.n1]
        if is_key_pressed(key):
            machine.program_counter = machine.program_counter + 4
        else:
            machine.program_counter = machine.program_counter + 2

    elif opCode.n0 == 0xE and opCode.lsb == 0xA1:
        key = machine.registers[opCode.n1]
        if not is_key_pressed(key):
            machine.program_counter = machine.program_counter + 4
        else:
            machine.program_counter = machine.program_counter + 2

    elif opCode.n0 == 0xF and opCode.lsb == 0x07:
        machine.registers[opCode.n1] = machine.current_delay_timer_duration()
        machine.program_counter = machine.program_counter + 2

    elif opCode.n0 == 0xF and opCode.lsb == 0x0A:
        for key in range(0x10):
            if is_key_pressed(key):
                machine.registers[opCode.n1] = key
                machine.program_counter = machine.program_counter + 2
                return
        # This meant to be blocking,  but we don't want to lock
        # up the UI. So instead we just exit without advancing the PC
        # so we get called again and again until we detect a key press                

    elif opCode.n0 == 0xF and opCode.lsb == 0x15:
        duration = machine.registers[opCode.n1]
        machine.reset_delay_timer(duration)
        machine.program_counter = machine.program_counter + 2

    #FX18

    elif opCode.n0 == 0xF and opCode.lsb == 0x1E:
        machine.I = (machine.I + machine.registers[opCode.n1]) % 0x10000
        machine.program_counter = machine.program_counter + 2

    elif opCode.n0 == 0xF and opCode.lsb == 0x29:
        character = machine.registers[opCode.n1]
        machine.I = font_address(character)
        machine.program_counter = machine.program_counter + 2


    elif opCode.n0 == 0xF and opCode.lsb == 0x33:
        vx = machine.registers[opCode.n1]
        machine.memory[machine.I] = math.floor(vx / 100)
        machine.memory[machine.I+1] = math.floor((vx % 100) / 10)
        machine.memory[machine.I+2] = vx % 10
        machine.program_counter = machine.program_counter + 2

    elif opCode.n0 == 0xF and opCode.lsb == 0x55:
        X = opCode.n1
        for i in range(X+1):
            machine.memory[machine.I + i] = machine.registers[i]
        machine.program_counter = machine.program_counter + 2

    elif opCode.n0 == 0xF and opCode.lsb == 0x65:
        X = opCode.n1
        for i in range(X+1):
            machine.registers[i] = machine.memory[machine.I + i]
        machine.program_counter = machine.program_counter + 2

    else:
        raise ValueError(f"Unknown opcode {hex(opCode.msb)}-{hex(opCode.lsb)}")
        




machine = Machine()
machine.load_rom("c8games/TETRIS")
load_fonts(machine)

pygame.init()
CELLSIZE = 10
size = (64 * CELLSIZE), (32 * CELLSIZE)
screen = pygame.display.set_mode(size)

next_move_event = pygame.USEREVENT + 1
pygame.time.set_timer(next_move_event, 1)

def is_key_pressed(key_code: int) -> bool:
    """
        key_code is 0-15  (0x0->0xF)
    """
    key = str(hex(key_code)[2:])

    pressed_keys = pygame.key.get_pressed()
    if key == "0": return pressed_keys[K_0] == 1 or pressed_keys[K_KP0] == 1
    if key == "1": return pressed_keys[K_1] == 1 or pressed_keys[K_KP1] == 1
    if key == "2": return pressed_keys[K_2] == 1 or pressed_keys[K_KP2] == 1
    if key == "3": return pressed_keys[K_3] == 1 or pressed_keys[K_KP3] == 1
    if key == "4": return pressed_keys[K_4] == 1 or pressed_keys[K_KP4] == 1
    if key == "5": return pressed_keys[K_5] == 1 or pressed_keys[K_KP5] == 1
    if key == "6": return pressed_keys[K_6] == 1 or pressed_keys[K_KP6] == 1
    if key == "7": return pressed_keys[K_7] == 1 or pressed_keys[K_KP7] == 1
    if key == "8": return pressed_keys[K_8] == 1 or pressed_keys[K_KP8] == 1
    if key == "9": return pressed_keys[K_9] == 1 or pressed_keys[K_KP9] == 1
    if key == "A": return pressed_keys[K_a] == 1 
    if key == "B": return pressed_keys[K_b] == 1
    if key == "C": return pressed_keys[K_c] == 1
    if key == "D": return pressed_keys[K_d] == 1
    if key == "E": return pressed_keys[K_e] == 1
    if key == "F": return pressed_keys[K_f] == 1
    
    raise ValueError(f"Unexpected key {key}")

def draw_screen(machine: Machine):
    black = pygame.Color(0,0,0)  
    white = pygame.Color(255,255,255)  

    for row in range(32):
        for column in range(64):
            if machine.display[row][column]:
                pygame.draw.rect(screen, white, (column*CELLSIZE,row*CELLSIZE,CELLSIZE,CELLSIZE))
            else:
                pygame.draw.rect(screen, black, (column*CELLSIZE,row*CELLSIZE,CELLSIZE,CELLSIZE))
    pygame.display.update()


while (True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == next_move_event:
            step(machine, draw_screen, is_key_pressed)    

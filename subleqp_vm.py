# Subleq+ Virtual Machine
# Copyright (C) 2022 McChuck
# original Copyright (C) 2013 Chris Lloyd
# Released under GNU General Public License
# See LICENSE for more details.
# https://github.com/cjrl
# This Subleq Virtual Machine was based on the pseudocode from the OSIC Wikipedia article:
# http://en.wikipedia.org/wiki/One_instruction_set_computer

try:
    from getch import getch, getche         # Linux
except ImportError:
    from msvcrt import getch, getche        # Windows

class SubleqpVM:
    @staticmethod 
    def execute(mem):
        pointer = 0
        running = True
        input_buffer = []

        def out_of_bounds(where):
            if mem[abs(where)] <0:
                print("\nIndirect reference out of bounds:", where, " value:", mem[abs(where)])
                raise IndexError

        while running:
            try:
                a = mem[pointer]
                b = mem[pointer+1]
                c = mem[pointer+2]
#                print(pointer, ":", a, b, c, flush=True)
                if a == -1 or a == 0:      # input
                    # if not input_buffer:
                    #    input_buffer.extend(list(input()))
                    # user_in = input_buffer.pop(0)
                    if a == -1:
                        user_in = getche()       # echo
                    if a == 0:
                        user_in = getch()       # no echo
                    if user_in.isdigit():
                        answer = int(user_in)
                    else:
                        answer = ord(user_in)
                    if b < 0:
                        out_of_bounds(b)
                        mem[mem[abs(b)]] = answer
                    else:
                        mem[b] = answer

                elif b == -1:    # output
                    if a < 0:
                        out_of_bounds(a)
                        print(chr(mem[mem[abs(a)]]), end="", flush=True)
                    else:
                        print(chr(mem[a]), end="", flush=True)
                else:
                    if b >= 0:
                        if a >= 0:
                            mem[b] -= mem[a]
                        else:
                            out_of_bounds(a)
                            mem[b] -= mem[mem[abs(a)]]
                    else:
                        if a >= 0:
                            out_of_bounds(a)
                            mem[mem[abs(b)]] -= mem[a]
                        else:
                            out_of_bounds(a)
                            out_of_bounds(b)
                            mem[mem[abs(b)]] -= mem[mem[abs(a)]]
                if b > 0:
                    if mem[b] > 0:
                        pointer += 3
                    else:
                        if c >= -1:
                            pointer = c
                        else:
                            pointer = mem[abs(c)]
                else:
                    if mem[mem[abs(b)]] > 0:
                        out_of_bounds(b)
                        pointer += 3
                    else:
                        if c >= -1:
                            pointer = c
                        else:
                            pointer = mem[abs(c)]
                if pointer < 0:
                    running = False
                    print("\n\nHALT")

            except IndexError:
                print("Memory out of bounds error at instruction", pointer)
                running = False

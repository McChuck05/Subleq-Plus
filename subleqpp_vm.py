# Subleq++ Virtual Machine
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

class VM:
    @staticmethod 
    def execute(mem):
        pointer = int(mem[0])        #   Instruction Pointer initialized to the first number in the file!
        running = True
        maxmem = len(mem)-1
        if pointer <= 0 or pointer > (maxmem - 2):
            print("/nInstruction pointer out of bounds at program init./n")
            running = False
            raise IndexError

        def deref(where):
            index = int(where)
            if out_of_bounds(index):
                print(" at instruction location: ", where, flush=True)
                raise IndexError
            if index < 0:
                index = mem[abs(index)]
                if index < 0:
                    print("Dereferenced location", index, "from", where, "is negative.")
                    raise IndexError
            return index

            #   This iterates to follow negative address pointers to a positive address.
            #   It works, but isn't particularly useful.
            # while index < 0:
            #     if out_of_bounds(index):
            #         print(" at instruction location:", where, flush=True)
            #         raise IndexError
            #     else:
            #         index = mem[abs(index)]
            # if out_of_bounds(index):
            #     print(" at instruction location:", where, flush=True)
            #     raise IndexError
            # else:
            #     return index


        def out_of_bounds(where):
            if abs(where) > maxmem:
                print("\nReference out of bounds:", where, end="")
                return True
            else:
                return False

        while running:
            try:
                a = mem[pointer]
                b = mem[pointer+1]
                c = mem[pointer+2]
                ap = deref(a)
                bp = deref(b)
                cp = deref(c)
                a_val = mem[ap]
                b_val = mem[bp]
                next_ip = pointer + 3

                # print(pointer, "A", a, ap, a_val, "B", b, bp, b_val, "C", c, cp, flush=True)

                if a == 0 and b == 0 and c == 0:
                    print("\nProgram successfully halted @", pointer)
                    running = False
                # elif a == 0 and b == 0 and c != 0:  # JSR
                    # user_in = getche()
                    # return_stack.append(pointer+3)
                    # next_ip = cp
                # elif a != 0 and b == 0 and c == 0:  # Return?
                    # if a_val <= 0:
                    #     if len(return_stack) > 0:
                    #         next_ip = return_stack[-1]
                    #         return_stack.pop(-1)
                    #     else:
                    #         print("Attempted to return from an empty stack @", pointer)
                    #         raise IndexError
                # elif a == 0 and b != 0 and c == 0:  # Return?
                    # if a_val > 0:
                    #     if len(return_stack) > 0:
                    #         next_ip = return_stack[-1]
                    #         return_stack.pop(-1)
                    #     else:
                    #         print("Attempted to return from an empty stack @", pointer)
                    #         raise IndexError


                elif a == 0 and b != 0 and c != 0:  # input
                    mem[bp] = ord(getch())
                elif a != 0 and b == 0 and c != 0:  # print
                    if a_val >= 0:
                        if c == 1:
                            print(a_val, end="", flush=True)
                        else:
                            print(chr(a_val), end="", flush=True)
                    else:
                        print("\nInvalid character:", a_val, " @ memory:", ap, " @ instrtuction:", pointer)
                        running = False
                else:
                    mem[bp] = b_val - a_val
                    if mem[bp] <= 0:
                        if cp <= 0:
                            print("\nHalted @:", pointer)
                            running = False
                        else:
                            next_ip = cp
                pointer = next_ip
                mem[0] = pointer
                if pointer <= 0 or pointer > (maxmem - 2):
                    running = False
                    raise IndexError


            except IndexError:
                print("Memory out of bounds error at instruction", pointer)
                print("A", a, ap, a_val, "B", b, bp, b_val, "C", c, cp)
                running = False
            except ValueError:
                print("Value error at instruction", pointer)
                print("A", a, ap, a_val, "B", b, bp, b_val, "C", c, cp)
                running = False

# Subleq+ master program
# Copyright (C) 2022 McChuck
# Released under GNU General Public License
# See LICENSE for more details.
# Many thanks to Chris Lloyd (github.com/cjrl) and Lawrence Woodman for inspiration and examples.
# Check out         https://techtinkering.com/articles/subleq-a-one-instruction-set-computer/
# And especially    https://techtinkering.com/2009/05/15/improving-the-standard-subleq-oisc-architecture/
# And maybe watch   https://www.youtube.com/watch?v=FvwcRaE9yxc

import sys
import os
from subleqp_parser import SubleqpParser
from subleqp_vm import SubleqpVM
try:
    from getch import getch, getche         # Linux
except ImportError:
    from msvcrt import getch, getche        # Windows


def Write_slc(slc_file, mem):
    pc = 0
    maxpc = len(mem) - 1
    while pc <= maxpc:
        a = mem[pc]
        b = 0
        c = 0
        if pc+1 <= maxpc:
            b = mem[pc+1]
        if pc+2 <= maxpc:
            c = mem[pc+2]
        slc_file.write('{} {} {}\n'.format(a, b, c))
        pc += 3


def Subleqp(args):
    try:
        sla_name = args[0]
        slc_name = None
        if len(args) > 1:
            slc_name = args[1]
        parser = SubleqpParser()
        mem = []
        with open(sla_name, "r") as sla_file:
            raw = sla_file.read()
            mem = parser.parse(raw)
            sla_file.close()
        if  slc_name != None:
            with open(slc_name, "w") as slc_file:
                Write_slc(slc_file, mem)
                slc_file.close()
        SubleqpVM.execute(mem)
    except(ValueError, IndexError):
        print("I just don't know what went wrong!\n")
        sla_file.close()

def main(args):
    try:
        print()
        if len(args) == 1:
            Subleqp(args)
        elif len(args) == 2:
            if os.path.isfile(args[1]):
                print(args[1], "exists.  Overwrite? ", end="", flush=True)
                answer = getche()
                if answer in ["y", "Y"]:
                    print()
                    print(args[1], "replaced \n\n", flush=True)
                    Subleqp(args)
                else:
                    print()
                    print(args[1], "retained \n\n", flush=True)
                    Subleqp([args[0]])
            else:
                print("creating", args[1], "\n\n", flush=True)
                Subleqp(args)
        else:
            print("usage: python subleqp.py infile.sla [outfile.slc]\n")
    except FileNotFoundError:
        print("< *Peter_Lorre* >\nYou eediot!  What were you theenking?\nTry it again, but thees time with a valid file name!\n</ *Peter_Lorre* >\n")
        print("usage: python subleqp.py infile.sla [outfile.slc]\n")


if __name__ == '__main__':
    main(sys.argv[1:])

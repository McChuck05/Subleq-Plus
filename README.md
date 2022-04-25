# Subleq+

Subleq+ is directly inspired by Lawrence Woodman's "Improving the Standard SUBLEQ OISC (One Instruction Set Computer) Architecture"
https://techtinkering.com/2009/05/15/improving-the-standard-subleq-oisc-architecture/

The parser and VM were taken from Chris Loyd https://github.com/cjrl/Python-Subleq and adapted for this project.

Summary:  Subleq, but with negative addresses used as indirect references.

Usage:  python subleqp.py infile.sla [outfile.slc]

If an outfile is named, the parser will create a compiled code file that can be run by the virtual machine.

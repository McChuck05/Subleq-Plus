# Subleq+

Subleq+ is directly inspired by Lawrence Woodman's "Improving the Standard SUBLEQ OISC (One Instruction Set Computer) Architecture"
https://techtinkering.com/2009/05/15/improving-the-standard-subleq-oisc-architecture/

The parser and VM were taken from Chris Loyd https://github.com/cjrl/Python-Subleq and adapted for this project.

**Note:**  There is a new, improved version available in the Subleq++ branch.

**Summary:**  Subleq, but with negative addresses used as indirect references.

**Usage:**  python subleqp.py infile.sla [outfile.slc]

If an outfile is named, the parser will create a compiled code file that can be run by the virtual machine.

 A B C ::=   [B] -= [A]; if [B] <= 0, goto C (standard Subleq)
 
 A B   ::>>   A B ? ::= [B] -= [A]; goto next
 
 A     ::>>   A A ? ::= [A] = 0; goto next
 
 A !   ::=   print [A]; goto next
 
 ! B   ::=   input [B]; goto next
 
 A A ! ::=   halt
 
 A \*B \*C ::>> [[B]] -= [A]; if [[B]] <= 0, goto [C]

 ? ::= next address
 
 @ ::= this address
 
 label: ::= address label, cannot be the only thing on a line
 
 \*label ::=  pointer to address label, represented as a negative address
 
 ! ::= -1 used for input, output, and halting (use 0 for noecho input)
 
 ;  ::=  end of instruction
 
 \#  ::=  comment
 
 . ::=  data indicator
 
 " or ' ::= string delimeters, must be data

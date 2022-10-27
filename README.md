# Subleq++

Subleq++ is directly inspired by Lawrence Woodman's "Improving the Standard SUBLEQ OISC (One Instruction Set Computer) Architecture"
https://techtinkering.com/2009/05/15/improving-the-standard-subleq-oisc-architecture/

The parser and VM were taken from Chris Loyd https://github.com/cjrl/Python-Subleq and adapted for this project.

**Summary:**  Subleq, but with negative addresses used as indirect references, improved.

Note:  There is an improved, improved version available here:  https://github.com/McChuck05/Subleq-Improved

**Usage:**  python subleqpp.py infile.sla [outfile.slc]

If an outfile is named, the parser will create a compiled code file that can be run by the virtual machine.

The first instruction **must** be the address to begin code execution.

 A B C ::=   [B] -= [A]; if [B] <= 0, goto C (standard Subleq)
 
 A B   ::>>   A B ? ::= [B] -= [A]; goto next
 
 A     ::>>   A A ? ::= [A] = 0; goto next
 
 A !  ::=   print [A] as a character; goto next
 
 A ! 1 ::=   print[A] as a number; goto next
 
 ! B C  ::=   input ASCII character [B]; goto next
 
 0 0 0 ::=   halt
 
 A \*B \*C ::>> [[B]] -= [A]; if [[B]] <= 0, goto [C]

 ? ::= next address, equivalent to @+1
 
 @ ::= this address, equivalent to ?-1
 
 label: ::= address label, can be the only thing on a line
 
 \*label ::=  pointer to address label, represented as a negative address
 
 ! ::= 0 used for input, output, and halting
 
 ;  ::=  end of instruction
 
 \#  ::=  comment
 
 . ::=  data indicator
 
 " or ' ::= string delimeters, must be data, can cross over lines

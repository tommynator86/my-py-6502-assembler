JMP test

LBL start
LDX 08
LDA FF

LBL decrement
LDAa 6000
DEX
CPX 03
BNE test
JMP start

LBL test
JMP start

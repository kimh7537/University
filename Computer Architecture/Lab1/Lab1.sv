main:
addiu $s0, $0, 10
addiu $s1, $0, 3
addu $t0, $s0, $0 

loop:
slt $t1, $t0, $s1
bne $t1, $0, remainder
nop
subu $t0, $t0, $s1
j loop
nop

remainder:
addu $s2, $0, $t0
j done
nop

done:
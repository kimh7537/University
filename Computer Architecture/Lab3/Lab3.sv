addiu $sp, $0, 0x1000    # stack pointer
addiu $s0, $0, 5      # input
j main
nop

# multiplication
mult:
  addiu $v0, $0, 0
  addiu $t0, $0, 0
multloop:
  slt $t1, $t0, $a1
  beq $t1, $0, multreturn
  nop
  addu $v0, $v0, $a0
  addiu $t0, $t0, 1
  j multloop
  nop
multreturn:
  jr $ra
  nop

factorial:
  addiu $t2, $0, 1         # result = 1
  addiu $t3, $0, 1         # i = 1
  addiu $s0, $s0, 1
  addiu $t5, $0, 0

  loop:
  slt $t4, $t3, $s0        #i < s0 + 1
  beq $t4, $t5, end
  nop
  
  addiu $sp, $sp, -4
  sw $ra, 0($sp)
  addu $a0, $0, $t2
  addu $a1, $0, $t3
  jal mult
  nop
  addu $t2, $0, $v0
  lw $ra, 0($sp)
  addiu $sp, $sp, 4
  addiu $t3, $t3, 1  

  j loop
  nop
  end:
  jr $ra
  nop


main:
  jal factorial
  nop
  addiu $s1, $t2, 0
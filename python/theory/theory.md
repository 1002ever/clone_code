# \* 이론 간단 정리



### 1. 데이터 타입

- Number  \- 1, 2 , ...

- Float        \- 소수 ( ex> 0.2 )

- Boolean  \-  True / False

- String      \- '123', 'abc'

- NoneType \- None         \<\< `파이썬에만 존재하는 자료형, JS로 따지면 null에 가까움` \>\>



=> <u>**type(데이터)** 로 데이터 타입 확인 가능</u>



> Tip. 파이썬 변수명은 `snake case`로 쓸 것
>
> ex) long_variable



### 2. 시퀀스 타입

​	=> mutable, immutable 로 나뉨

​	=> in , not in, len, min max 연산자, 인덱싱 등이 가능

- Mutable
  - List \- [1,2,3, ...]
  - Dictionary - { key: value, key2: value, ...}
- Immutable
  - Tuple \- (1,2,3, ...)



### 3. 함수

- 내장 함수

- 외장 함수

- 사용자 정의 함수

  > def 함수명(인자):
  >
  > ​	수행사항



\*\* f 스트링

```python
def say_hello(name, age):
    return f"Hello {name} you are {age} years old"

hello = say_hello("kyw", "29")
print(hello) #Hello kyw you are 29 years old
```



### 4. 조건문

> if 조건:
>
> ​	수행1
>
> elif 조건2:
>
> ​	수행2
>
> else:
>
> ​	수행3



### 5. 반복문

for 변수 in 시퀀스타입_데이터:

​	변수

=> 시퀀스 타입 내 데이터를 순차적으로 호출



### 6. 모듈

- import하여 다른 python 파일의 코드를 사용할 수 있음

  ex)

  ```python
  import math
  #필요한 것만 불러오는 것이 효율적 그럴 떈 아래와 같이
  #from math import ceil
  #다른 이름으로 쓰고 싶을 때
  #from math import ceil as my_ceil
  
  print(math.ceil(1.2)) # 2
  ```
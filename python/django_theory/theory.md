## Django 시작 전 기초 개념



### \*\* arguments & keyword arguments

- 개수 제한 없이 인자를 주고 싶을 때 사용하는 개념

  ```python
  # 예시
  
  def plus(a, b, *args, **kwargs):
      print(args)    # (1,1,1,1,1) - 튜플 형태
      print(kwargs)  # {'a': True, 'b': True, 'c': True} - 딕셔너리 형태
      return a+b
  
  # 1은 7개
  plus(1,1,1,1,1,1,1,a=True,b=True,c=True)
  
  ```

  

### \*\* 객체지향 프로그래밍

```python
class Car():
    wheels = 4
    doors = 4
    windows = 4
    seats = 4
    
    #def start():
    #    print("I started")
    
    def start(self):
        print(self.color)
        print("I started")
        
    def __str__(self):
        return "오버라이딩 됨"
    
    # 생성자, 객체 생성 시 자동 호출 됨
    def __init__(self, **kwargs):
                     # color나 price가 주어지지 않으면, black이나 20이 디폴트
        self.color = kwargs.get('color', 'black')
        self.price = kwargs.get('price', '$20')
        
# class의 인자에 다른 클래스 명을 넣어주면 Extends(상속) 함
class Convertible(Car):
    # 재정의하면서 기존 __init__ 기능은 전부 사용하고 싶을 때?
    #    => 부모의 __init__ 도 수행해주면 됨
    # 자신 시점에서 __init__이 덮인거지, 부모의 __init__이 사라진 것은 아니기 때문에
    # super로 접근하면 호출이 가능
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time = kwargs.get("time", 10)
    
    def take_off(self):
        return "taking off"
    
porche = Car()
porche.color = "Red"

# 아래 호출 시 클래스에서 한 인자를 안 주면 에러 듬
# 파이썬이 메소드에는 자기 자신(인스턴스)을 자동으로 인자로 넣어주기 때문
# 메소드 정의 시 반드시 한 인자 이상을 지정해줘야 함
# => 첫 인자는 자기 자신이므로 보통 self 로 이름 지음
porche.start()	# Red
				# I started
    
    
# 출력하고 싶다는 말은 string으로 변환이 필요하다는 말
# 클래스 자체 메소드로 __str__를 가짐(문자열로 바꿔주는)
#   => print(객체) 시 __str__을 자동으로 호출
# 클래스 정의 시 이를 오버라이딩 하여 재정의 된 return이 출력 됨
print(porche)   # 오버라이딩 됨


sonata = Car(color="green", price="$40")
print(sonata.color, sonata.price)  # green $40



```




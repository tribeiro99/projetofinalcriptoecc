class Person:
  def __init__(ponto, name, age):
    ponto.name = name
    ponto.age = age

  def myfunc(abc):
    print("Hello my name is " + abc.name)

  def myputas(ola):
    print("ola tenho " + str(ola.age))

p1 = Person("Tiago", 69)
p1.myfunc()

p1.myputas()
 

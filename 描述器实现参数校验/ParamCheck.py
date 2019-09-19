from functools import partial
#非数据描述器的基础实现
class StaticMethod:
    def __init__(self, fn):
        self._fn = fn

    def __get__(self, instance, owner):
        return self._fn

class ClassMethod:
    def __init__(self, fn):
        self._fn = fn
    def __get__(self, instance, owner):
        ret = partial(self._fn, owner)
        return ret

class A:
    @StaticMethod # stmtd = StaticMerhod(stmtd) -> 经过StaticMethod初始化后调用__get__
    def stmtd(self):
        print('static method')
    @ClassMethod
    def clmtd(cls):
        print('class method')

#参数校验基础
class Person:
    def __init__(self, name:str, age:int):
        params = ((name,str), (age,int))
        if not self.checkdata(params): #初始化前先做类型检查
            raise TypeError('type error')
        self.name = name #检查成功赋值，否则报错
        self.age = age

    def checkdata(self, params):
        for param, type in params:
            if not isinstance(param, type):
                return False
        return True

# p = Person('tom', 18)
# print(p.name,p.age)
# p = Person('tom', '18')
# print(p)

#上面的校验方法耦合度太高，下面用描述器的方式进行修改完善
class TypeCheck:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.data = {}
    def __get__(self, instance, owner):
        if instance is not None:
            #return instance.__dict__[self.name]
            return self.data[self.name]
        return self
    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError('{} is TypeError'.format(value))
        #instance.__dict__[self.name] = value  #把数据存回Person类的实例中
        self.data[self.name] = value  #在TypeCheck类中进行单独存放

class Person:
    name = TypeCheck('name', str)
    age = TypeCheck('age', int)
    def __init__(self, name:str, age:int):
        self.name = name
        self.age = age


#这种方法虽然实现了解耦，但是出现了硬编码，还是不好，继续修改
import inspect
class TypeCheck:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __get__(self, instance, owner):
        if instance is not None:
            return instance.__dict__[self.name]
        return self

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError('{} is TypeError'.format(value))
        instance.__dict__[self.name] = value

def typeassert(cls):
    params = inspect.signature(cls).parameters  #params是一个有序字典
    for name, param in params.items():
        if param.annotation != param.empty:
            setattr(cls, name, TypeCheck(name, param.annotation))
    return cls
@typeassert
class Person:
    def __init__(self, name:str, age:int):
        self.name = name
        self.age = age


# #这样差不多了，但是还可以继续修改，把断言函数封装成类
class TypeCheck:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __get__(self, instance, owner):
        if instance is not None:
            return instance.__dict__[self.name]
        return self

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError('{} is TypeError'.format(value))
        instance.__dict__[self.name] = value

class TypeAssert:
    def __init__(self, cls):
        self.cls = cls
        params = inspect.signature(cls).parameters
        for name, param in params.items():
            if param.annotation != param.empty:
                setattr(cls, name, TypeCheck(name, param.annotation))

    def __call__(self, *args, **kwargs):
        return self.cls(*args, **kwargs)
@TypeAssert
class Person:
    def __init__(self, name:str, age:int, height:float, bol:bool=True):
        self.name = name
        self.age = age
        self.height = height
        self.bol = bol

p = Person('TOM', 40, 18.7, bol=False)
print(p.age, p.height, p.bol)















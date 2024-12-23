from inspect import isclass
from typing import TypeVar

T = TypeVar("T", bound=type)


def block(cls: T) -> T:
    cls.blocked = True
    if isclass(cls):
        print("class!")
    else:
        print("method!")
    return cls


# Example usage
@block
class MyClass:
    @block
    def hello(self):
        print("Hello")


print(MyClass.blocked)  # Output: True
print(MyClass.hello.blocked)  # Output: True

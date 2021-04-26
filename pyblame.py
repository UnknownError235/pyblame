import functools
import inspect
class Author:

    def __repr__(self) -> str:
        return f'{self.name}: {self.email}'

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

def blame(x):
    if isblameable(x):
        return x.__authors__
    else:
        raise Exception('No authors')


def constant(value, auth):
    class newType(value.__class__):
        
        def __init__(self, orig):
            super().__init__()
            self.__authors__ = set()
            # for atr in self.__dir__():
            #     if callable(getattr(self, atr)) and not inspect.isclass(getattr(self, atr)):
            #         setattr(self, atr, author(auth)(getattr(self, atr)))
    for atr in dir(newType):
        if callable(getattr(newType, atr)) and atr not in ['__dir__', '__getattribute__', '__init_subclass__', '__new__', '__setattr__', '__init__', '__class__']:
            setattr(newType, atr, author(auth)(getattr(newType, atr)))  
    result = newType(value)
    result.__authors__.add(auth)
    return result


def isblameable(x):
    return '__authors__' in dir(x)

def author(a: Author):
    def decorator(func):
        @functools.wraps(func)
        def runner(*args, **kwargs):
            prev_authors = set()
            arglist = [*args]
            if len(kwargs) != 0:
                arglist.extend(kwargs.values())
            for arg in arglist:
                if isblameable(arg):
                    prev_authors.update(arg.__authors__)

            result = func(*args, **kwargs)

            if isblameable(result):
                result.__authors__.add(a)
            else:
                result = constant(result, a)
            result.__authors__.update(prev_authors)
            return result
        return runner
    return decorator
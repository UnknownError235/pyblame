import functools
class Author:

    def __repr__(self) -> str:
        return f'{self.name}: {self.email}'

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

def blame(x):
    if '__authors__' in dir(x):
        return x.__authors__
    else:
        raise Exception('No authors')


def author(a: Author):
    def decorator(func):
        @functools.wraps(func)
        def runner(*args, **kwargs):
            prev_authors = set()
            for arg in args:
                if '__authors__' in dir(arg):
                    prev_authors.update(arg.__authors__)

            for arg in kwargs.values():
                if '__authors__' in dir(arg):
                    prev_authors.update(arg.__authors__)

            result = func(*args, **kwargs)

            if '__authors__' in dir(result):
                result.__authors__.add(a)
            else:
                class newType(result.__class__):

                    def __init__(self, orig):
                        super().__init__()
                        self.__authors__ = set()
                    
                    @author(a)
                    def __add__(self, *args, **kwargs):
                        return super().__add__(*args, **kwargs)

                    @author(a)
                    def __mul__(self, *args, **kwargs):
                        return super().__mul__(*args, **kwargs)
                    
                result = newType(result)
                result.__authors__.add(a)
            result.__authors__.update(prev_authors)
            return result
        return runner
    return decorator
from pyblame import author, Author, constant, blame, isblameable

Max = Author('Max', 'm.e.vangent@students.uu.nl')

Jan = Author('Jan', 'jan@gmail.com')

# @author(Max)
def add(x, y):
    return x + y

# @author(Jan)
def mul(x, y):
    return x * y

def addAndSquare(x, y):
    z = add(x, y)
    return mul(z, z)

if __name__ == '__main__':
    x, y = constant(2, Max), constant(3, Jan)
    z = addAndSquare(x, y)
    e = x == y
    print(e, blame(e))
import pyblame

Max = pyblame.Author('Max', 'm.e.vangent@students.uu.nl')

Jan = pyblame.Author('Jan', 'jan@gmail.com')

@pyblame.author(Max)
def add(x, y):
    return x + y

@pyblame.author(Jan)
def mul(x, y):
    return x * y

def addAndSquare(x, y):
    z = add(x, y)
    return mul(z, z) + 0

if __name__ == '__main__':
    x = 1
    y = 1
    z = addAndSquare(x, y)
    print(pyblame.blame(z))
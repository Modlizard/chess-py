class human:
    def __init__(self,name,gender):
        self.nom = name
        self.g = gender

    def greet(self):
        print('Wag wan', self.nom)

    def judge(self):
        if self.g == 'm':
            print('stop man spreading fucking hell')
        else:
            print('you are a neek')

testObj = human(input('name: '),input('gender: '))
testObj.greet()
testObj.judge()

test2 = human(input('name: '),input('gender: '))
test2.greet()
test2.judge()



class Employee:
    
    #emp_x is always passed. This is why the self is necessary. (Instance argument)
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'

    def fullname(self):
        return '{} {}'.format(self.first, self.last)


emp_1 = Employee('Corey', 'Schafer', 50000)
emp_2 = Employee('Test', 'User', 60000)

#print(emp_1)
#print(emp_2)

print(emp_1.email)
print(emp_2.email)

print(emp_1.fullname())
#Employee.fullname(emp_1)=emp_1.fullname()
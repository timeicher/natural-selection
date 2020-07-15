

class Employee:
    num_of_emps = 0   
    raise_amount = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'

        Employee.num_of_emps += 1

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)

emp_1 = Employee('Corey', 'Schafer', 50000)
emp_2 = Employee('Test', 'User', 60000)


print(Employee.num_of_emps)




#A method to see what's going on inside a class.
#print(Employee.__dict__)


#You can edit Class Variables like this:
#Employee.raise_amount = 1.05

#You can edit Class Variables only for one instance like this:
#emp_1.raise_amount = 1.05

#rint(Employee.__dict__)


#Class Variables can be accessed by instances and classes.
"""
print(Employee.raise_amount)
print(emp_1.raise_amount)
print(emp_2.raise_amount)
"""





"""
print(emp_1.pay)
emp_1.apply_raise()
print(emp_1.pay)
"""
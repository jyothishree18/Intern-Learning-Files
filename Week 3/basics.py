name = "Jyothi"
age = 24
marks = 85.5

print(name)
print(age)
print(marks)

#DATA TYPES
x = 10
price = 99.5
name = "Jyothi"
passed = True

print(type(x))
print(type(price))
print(type(name))
print(type(passed))

#ARITHMETIC
a = 10
b = 3

print(a + b)
print(a - b)
print(a * b)
print(a / b)
print(a // b)
print(a % b)
print(a ** b)

#IF,ELIF,ELSE
marks = 75

if marks >= 90:
    print("A")
elif marks >= 60:
    print("B")
else:
    print("C")

#FOR
for i in range(1, 6):
    print(i)

#WHILE
n = 3

while n > 0:
    print(n)
    n -= 1

#FUNCTION
def greet(name):
    return f"Hello, {name}"

print(greet("Jyothi"))

#COLLECTIONS

students = ["Priya", "Rahul", "Jyothi"]

print(students[0])
students.append("Arun")

print(students)

student = {
    "name": "Jyothi",
    "role": "intern"
}

print(student["name"])

#ERROR HANDLING
try:
    age = int(input("Enter age: "))
    print(age)
except ValueError:
    print("Please enter a number")
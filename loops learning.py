Python 3.10.5 (tags/v3.10.5:f377153, Jun  6 2022, 16:14:13) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
student_names = ["amrit", "baya", "katherine"]
"amrit" in
SyntaxError: multiple statements found while compiling a single statement

student_names = ["amrit", "poon", "pooppp"]
student_names
['amrit', 'poon', 'pooppp']
student_names.append("Homer")
student_names
['amrit', 'poon', 'pooppp', 'Homer']
"amrit" in student_names
True
len[student_names]
Traceback (most recent call last):
  File "<pyshell#7>", line 1, in <module>
    len[student_names]
TypeError: 'builtin_function_or_method' object is not subscriptable
len(student_names)
4
del student_names[2]
student_names
['amrit', 'poon', 'Homer']

for name in student_names:
    print("Student name is {0}".format(name))

Student name is amrit
Student name is poon
Student name is Homer


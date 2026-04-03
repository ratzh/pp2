import re
a=input()
x=re.findall(r"\d",a)
print(*x)
s = []

# a = "A corequisite A"
# s.append(a)

a = "2nd 7 weeks. Pre/Co-requisite:PE 261 or consent of instructor."
s.append(a)

b = "B corequisite: B"
s.append(b)

c = "C Corequisite C"
s.append(c)

d = "D Corequisite: D"
s.append(d)

e = "E co-requisite E"
s.append(e)

f = "F co-requisite: F"
s.append(f)

g = "G Co-requisite G"
s.append(g)

h = "H Co-requisite: H"
s.append(h)

i = "I coRequisite I"
s.append(i)

j = "J coRequisite: J"
s.append(j)

k = "K CoRequisite K"
s.append(k)

l = "L CoRequisite: L"
s.append(l)

m = "M co-Requisite M"
s.append(m)

n = "N co-Requisite: N"
s.append(n)

o = "O Co-Requisite O"
s.append(o)

p = "P Co-Requisite: P"
s.append(p)

import re

for string in s:
	letters = re.split(r'[C/c]o-?[R/r]equisite:?', string)
	print(letters)











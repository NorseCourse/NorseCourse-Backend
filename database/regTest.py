s = []

a = "A corequesite A"
s.append(a)

b = "B corequesite: B"
s.append(b)

c = "C Corequesite C"
s.append(c)

d = "D Corequesite: D"
s.append(d)

e = "E co-requesite E"
s.append(e)

f = "F co-requesite: F"
s.append(f)

g = "G Co-requesite G"
s.append(g)

h = "H Co-requesite: H"
s.append(h)

i = "I coRequesite I"
s.append(i)

j = "J coRequesite: J"
s.append(j)

k = "K CoRequesite K"
s.append(k)

l = "L CoRequesite: L"
s.append(l)

m = "M co-Requesite M"
s.append(m)

n = "N co-Requesite: N"
s.append(n)

o = "O Co-Requesite O"
s.append(o)

p = "P Co-Requesite: P"
s.append(p)

import re

for string in s:
	letters = re.split(r'[C/c]o-?[R/r]equesite:?', string)
	print(letters)











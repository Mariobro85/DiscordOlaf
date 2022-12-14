import random as rand

def rand_line():
	f = open("quotes.txt")
	l = next(f)
	for num, line in enumerate(f, 2):
		if rand.randrange(num):
			continue
		l = line
	return l.strip().replace("\\n", '\n')

print(rand_line())

#!/usr/local/bin/python3

'''
Calculator
A simple culator which has externally defined methods.
Also has a settings page which allows modification of this.
Note: requires installation of getch
Author: Zachary Cormack
'''

from sys import platform
from calc_methods import methods
from time import sleep

use_getch = True

if platform == "win32":
	use_ANSI = False
	print("""
ANSI SEQUENCES UNAVAILABLE.
SOME FUNCTIONALITY MAY BE SUB-OPTIMAL.
""")
else:
	use_ANSI = True

try:
	from getch import getch
except ModuleNotFoundError:
	use_getch = False
	print("""
GETCH LIBRARY UNAVAILABLE.
SOME FUNCTIONALITY MAY BE SUB-OPTIMAL.
""")

digits = 2

c = []
num_active = 0

for i, method in enumerate(methods):
	if method[1]:
		c.append(method + (i,))
		num_active += 1


HOME = """\033[u
INTERACTIVE CALCULATOR          
This calculator can perform the following operations:
""" if use_ANSI else """
INTERACTIVE CALCULATOR
This calculator can perform the following operations:
"""

SETTINGS = """\033[u
INTERACITVE CALCULATOR: SETTINGS
enable and disable functions, and change rounding
""" if use_ANSI else """
INTERACITVE CALCULATOR: SETTINGS
enable and disable functions, and change rounding
"""

if use_ANSI:
	print("\033[s")

s = 0

while True:
	if   s  < num_active:
		# a standard option has been selected
		pre = "\033[30;47m" if use_ANSI else "*"
		suf = "\033[0m"     if use_ANSI else "*"
		c[s] = (
			c[s][0],
			c[s][1],
			c[s][2],
			pre + methods[c[s][4]][3] + suf,
			c[s][4]
		)
		s_str = "    SETTINGS            "
		q_str = "    QUIT                "
	elif s == num_active:
		# 'SETTINGS' is selected
		if use_ANSI:
			s_str = "    \033[30;47mSETTINGS          \033[0m"
		else:
			s_str = "    *SETTINGS*"
		q_str = "    QUIT                "
	else:
		# 'QUIT' is is selected
		s_str = "    SETTINGS            "
		if use_ANSI:
			q_str = "    \033[30;47mQUIT              \033[0m"
		else:
			q_str ="    *QUIT*"

	print(HOME)

	for i, j, k, name, n in c:
		print("%2d. %s" %(n+1, name))

	print("\033[K", s_str, q_str,
		("\033[K\n"*25 + "\033[25A") if use_ANSI else "",sep="\n")

	if use_getch:
		key = getch()
		if   key == "\n":
			key = "d"
		elif key == "\x1b":
			key = getch()
			key = getch()
			if key == "A":
				key = "w"
			elif key == "B":
				key = "s"
			elif key == "C":
				key = "d"
			else:
				key = "a"
	else:
		key = input()
	
	if   key == "s":
		# s for move down
		if s < num_active:
			c[s] = list(c[s])
			c[s][3] = methods[c[s][4]][3]
			c[s] = tuple(c[s])
		s += 1
	elif key == "w":
		# w for move up
		if s < num_active:
			c[s] = list(c[s])
			c[s][3] = methods[c[s][4]][3]
			c[s] = tuple(c[s])
		s -= 1
	elif key == "d":
		# d for choose option
		if   s  < num_active:
			# run function
			params = []
			for i in range(1, 1+c[s][2]):
				while True:
					try:
						param = float(input("> "))
					except ValueError:
						print("!!!")
						sleep(0.5)
						print("\033[A\033[K"*2, end="")
						continue
					else:
						break

				params += [param]
			func = c[s]
			try:
				ans = func[0](*params)
			except Exception as e:
				print(e, "\nPlease try again.")
			else:
				if isinstance(ans, float):
				# should print integer on integer result
				# round output otherwise
					if round(ans, digits).is_integer():
						ans_str = str(int(ans))
					else:
						ans_str = "%.*f" %(digits, ans)
				else:
					# don't print 0 component
					# print integer for integer component
					# round component otherwise
					if not round(ans.real, digits):
						r_str = ""
					elif   round(ans.real, digits) % 1:
						r_str = "%.*f" %(
							digits,
							ans.real
						)
					else:
						r_str = str(int(ans.real))
					
					if     round(ans.imag, digits) ==  1:
						i_str = "+i" if r_str else "i"
					elif   round(ans.imag, digits) == -1:
						i_str = "-i"
					elif   round(ans.imag, digits) % 1:
						# include sign
						i_str = (
						"%+.*fi" if r_str else "%.*fi"
						) %(digits, ans.imag)
					else:
						i_str = (
						"%+di" if r_str else "%di"
						) %(int(ans.imag))
					# put real and imaginary parts together
					ans_str = r_str + i_str
				print("Result:", ans_str)
			finally:
				input("Press enter to continue... ")
		elif s == num_active:
			# edit settings
			t = 0
			active = False
			while True:
				print(SETTINGS)

				if t < len(methods):
					r_str = "    ROUND                "
					b_str = "    BACK                 "
					pre = "\033[30;47m" if use_ANSI else "*"
					suf = "\033[0m"     if use_ANSI else "*"
					if methods[t][1]:
						if active and use_ANSI:
							pre = ""
							suf = " \033[30;47mEnabled\033[0m "
						elif active:
							pre = ""
							suf = " *Enabled*"
						else:
							suf += " Enabled "
					else:
						if active and use_ANSI:
							pre = ""
							suf = " \033[30;47mDisabled\033[0m"
						elif active:
							pre = ""
							suf = " *Disabled*"
						else:
							suf += " Disabled"
				elif t == len(methods):
					# 'ROUND' is selected
					if use_ANSI and not active:
						r_str = "    \033[30;47mROUND             \033[0m "
					elif not active:
						r_str = "    *ROUND*          "
					elif use_ANSI and active:
						r_str = "    ROUND              \033[30;47m"
					else:
						r_str = "    ROUND             *"
					
					r_str += "%2d" %(digits)
					
					if use_ANSI and active:
						r_str += "\033[0m"
					elif active:
						r_str += "*"
						
					b_str = "    BACK                 "
				else:
					# 'BACK' is is selected
					r_str = "    ROUND                "
					if use_ANSI:
						b_str = "    \033[30;47mBACK              \033[0m"
					else:
						b_str ="    *BACK              *"
				
				for i, method in enumerate(methods):
					print("%2d." %(i+1), end=" ")
					if i == t:
						print(pre + method[3] + suf)
					else:
						print(method[3] + " "*9)
				
				print("", r_str, b_str, sep="\n")
				
				if use_getch:
					skey = getch()
					if   skey == "\n":
						skey = "d"
					elif skey == "\x1b":
						skey = getch()
						skey = getch()
						if skey == "A":
							skey = "w"
						elif skey == "B":
							skey = "s"
						elif skey == "C":
							skey = "d"
						else:
							skey = "a"
				else:
					skey = input()
				
				if   skey == "s":
					# s for move down
					if active and t < len(methods):
						methods[t] = list(methods[t])
						methods[t][1] = False
						methods[t] = tuple(methods[t])
					elif active:
						digits -= 1
						if digits == 0:
							digits = 1
					else:
						t += 1
				elif skey == "w":
					# w for move up
					if active and t < len(methods):
						methods[t] = list(methods[t])
						methods[t][1] = True
						methods[t] = tuple(methods[t])
					elif active:
						digits += 1
					else:
						t -= 1
				elif skey == "d":
					# d for modify setting
					if t > len(methods):
						# quit
						break
					active = True
				elif skey == "a":
					# a for save setting
					active = False

				if t < 0:
					# there is no option -1, loop around
					t = len(methods) + 1
				elif t > len(methods) + 1:
					# cannot go past end, loop around
					t = 0
                                        
			s = 0
			c = []
			num_active = 0
			for i, method in enumerate(methods):
				if method[1]:
					c.append(method+(i,))
					num_active += 1
			sleep(1)
			if use_ANSI:
				print("\033[A\033[K")
			
		else:
			# quit
			print("GOODBYE!")
			sleep(3.5)
			break

	if s < 0:
		# there is no option -1, loop around
		s = num_active + 1
	elif s > num_active + 1:
		# cannot go past end, loop around
		s = 0

if use_ANSI:
	print(end="\033[u")

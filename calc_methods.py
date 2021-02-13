import math

ROUND = 2

def fib(n):
	if n:
		if n == 1:
			print("1", end=", ")
			return 1, 1
		prev = fib(n-1)
		print(prev[0], end=", ")
		return sum(prev), prev[0]
	return 1, 0

def A_hide(m, n):
	if   m == 0:
		return n+1
	elif m == 1:
		return n+2
	elif m == 2:
		return n*2+3
	elif m == 3:
		return (8<<n)-3
	else:
		if not n:
			return A_hide(m-1, 1)
		else:
			return A_hide(m-1, A_hide(m, n-1))


def A(m, n, i):
	if i == 3 and m:
		ans = A_hide(m, n)
		print((i+1)*"  " + "A(%d, %d): ... = %d" %(m, n, ans))
		return ans

	print((i+1)*"  " + "A(%d, %d):" %(m, n), end=" ")
	
	if not m:
		print("%d+1 = %d" % (n, n+1))
		return n+1
	
	if not n:
		print("A(%d, 1)" %(m-1))
		ans = A(m-1, 1, i+1)
		print((i+1)*"  " + "A(%d, 0) = %d" %(m, ans))
		return ans

	print("A(%d, A(%d, %d))" %(m-1, m, n-1))
	next_n = A(m, n-1, i+1)
	print((i+1)*"  " + "A(%d, %d): A(%d, %d)" %(m, n, m-1, next_n))
	ans = A(m-1, next_n, i+1)
	print((i+1)*"  " + "A(%d, %d) = %d" %(m, n, ans))

	return ans

methods = [
	# enabled by default
	(lambda x, y: x+y,  True, 2, "addition       (+)"),
	(lambda x, y: x-y,  True, 2, "subtaction     (-)"),
	(lambda x, y: x*y,  True, 2, "multiplication (*)"),
	(lambda x, y: x/y,  True, 2, "division       (/)"),
	(lambda x, y: x**y, True, 2, "exponent       (^)"),
	
	(lambda x, y: x if x>y else y, True, 2, "maximum           "),
	(lambda x, y: x if x<y else y, True, 2, "minimum           "),
	
	# optionally enabled in settings
	(lambda m,n: float(A(m, n, 0)),  False, 2, "Ackermann         "),
	(lambda   n: float(fib(n-1)[0]), False, 1, "Fibbonacci        "),
	
	# imported math functions
	(math.exp,   False, 1, "e^n               "),
	(math.sqrt,  False, 1, "sqrt              "),
	(math.sin,   False, 1, "sin               "),
	(math.cos,   False, 1, "cos               "),
	(math.tan,   False, 1, "tan               "),
	(math.asin,  False, 1, "asin              "),
	(math.acos,  False, 1, "acos              "),
	(math.atan,  False, 1, "atan              "),
	(math.sinh,  False, 1, "sinh              "),
	(math.cosh,  False, 1, "cosh              "),
	(math.tanh,  False, 1, "tanh              "),
	(math.asinh, False, 1, "asinh             "),
	(math.acosh, False, 1, "acosh             "),
	(math.atanh, False, 1, "atanh             "),
]

# Decorators
#1
def make_pretty(func):
	def wrapper(*args, **kwargs):
		print("I am Decorated.")
		func()
	return wrapper

@make_pretty
def ordinary():
	print("I am ordinary")

#2
def smart_divide(func):
	def wrapper(a, b):
		if b == 0:
			print(f"{a} cannoy be divided by {b}.")
			return
		func(a, b)
	return wrapper

@smart_divide
def divide(a, b):
	print(a/b)

# Chaining Decorator

def percent(func):
	def wrapper(*args, **kwargs):
		print("%"*15)
		func(*args, **kwargs)
		print("%" * 15)
	return wrapper

def star(func):
	def wrapper(*args, **kwargs):
		print("*" * 15)
		func(*args, **kwargs)
		print("*" * 15)
	return wrapper


@start
@percent
def printer(msg):
	print(msg)


class PowTwo:
	def __init__(self, maximum=0):
		self.maximum = maximum

	def __iter__(self):
		self.n = 0
		return self

	def __next__(self):
		if self.n <= self.maximum:
			result = 2 ** self.n
			self.n += 1
			return result
		else:
			raise(StopIteration("No more Element"))


r = PowTwo(3)
print(iter(r))


callback_registers = {}

def one_func(a, b):
	print 'this is callback function 1.'
	print a+b

def another_func(a, b):
	print 'this is calback function 2.'
	print a*b

def run():
	print 'do somethings.'

	# finally, run callback.
	for func, args in callback_registers['run']:
		func(*args)

def add_callback(func_name, callback, args):
	if func_name not in callback_registers:
		callback_registers[func_name] = []
	callback_registers[func_name].append((callback, args))

add_callback('run', one_func, (3,5))
add_callback('run', another_func, (3,5))
run()
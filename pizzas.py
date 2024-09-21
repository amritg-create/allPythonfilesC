def make_pizza(size, *toppings):
	print('Making a ', size, '-inch pizza with the following topics: ')
	for topping in toppings:
		print(f"-{topping}")
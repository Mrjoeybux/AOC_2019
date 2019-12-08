
class intcode(object):
	
	def __init__(self):
		self.code = None
		self.current_index = None
		self.path = None

	def run(self, verbose=False):
		self.current_index = 0
		while self.code[self.current_index] != 99:
			if self.code[self.current_index] == 1:
				self._add()
			elif self.code[self.current_index] == 2:
				self._multiply()
			else:
				self.current_index += 4
		if verbose:
			print(self.code[0])
		return self.code[0]
			
	def read(self, path_input=None):
		if path_input is None:
			path = self.path
		else:
			self.path = path_input
			path = path_input
		self.code = []
		with open(path, "r") as f:
			for number in f.readline().split(","):
				self.code.append(int(number))

	def update_noun(self, value):
		self.code[1] = value

	def update_verb(self, value):
		self.code[2] = value

	def _add(self):
		self.code[self.code[self.current_index + 3]] = \
		self.code[self.code[self.current_index + 1]] + \
		self.code[self.code[self.current_index + 2]]
		self.current_index += 4

	def _multiply(self):
		self.code[self.code[self.current_index + 3]] = \
		self.code[self.code[self.current_index + 1]] * \
		self.code[self.code[self.current_index + 2]]
		self.current_index += 4

	def reset(self):
		self.code = None
		self.read()

def find_input(path, target):
	ic = intcode()
	ic.read(path)
	for noun in range(99):
		for verb in range(99):
			ic.update_noun(noun)
			ic.update_verb(verb)
			if ic.run(verbose=True) == target:
				return noun, verb
			ic.reset()

if __name__ == "__main__":
	noun, verb = find_input("data.dat", 19690720)
	print(100*noun + verb)

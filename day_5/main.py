
class intcode(object):
	
	def __init__(self):
		self.code = None
		self.current_index = None
		self.path = None
		self.stop = None
		self.output = None

	def run(self, test_input=None):
		self.current_index = 0
		self.stop = False
		self._parameter_mode(test_input)
		while not self.stop:
			self._parameter_mode()
		return self.output
			
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

	def _add(self, C, B, A):
		par_1 = self._interpret_parameter(C, 1)
		par_2 = self._interpret_parameter(B, 2)
		if A == 0:
			self.code[self.code[self.current_index + 3]] = par_1 + par_2
		else:
			self.code[self.current_index + 3] = par_1 + par_2
		
	def _multiply(self, C, B, A):
		par_1 = self._interpret_parameter(C, 1)
		par_2 = self._interpret_parameter(B, 2)
		if A == 0:
			self.code[self.code[self.current_index + 3]] = par_1 * par_2
		else:
			self.code[self.current_index + 3] = par_1 * par_2

	def _save_input(self, input_val):
		self.code[self.code[self.current_index + 1]] = input_val

	def _output(self):
		self.output = self.code[self.code[self.current_index + 1]]

	def _parameter_mode(self, input_val=None):
		str_val = str(self.code[self.current_index])
		n = len(str_val)
		if input_val is not None:
			self._save_input(input_val)
		opcode = int(str_val[-2:])
		n = len(str_val)
		if len(str_val) < 5:
			i = 0
			while i < 5 - n:
				str_val = "0" + str_val
				i+= 1
		C = int(str_val[-3])
		B = int(str_val[-4])
		A = int(str_val[-5])
		#print(opcode, C, B, A)
		if opcode == 1:
			self._add(C, B, A)
		elif opcode == 2:
			self._multiply(C, B, A)
		elif opcode == 3:
			self._save_input(input_val)
		elif opcode == 4:
			self._output()
			self.stop = True
		elif opcode == 99:
			self.output = self.code[0]
			self.stop = True
		self.current_index += n
	
	def _interpret_parameter(self, parameter, parameter_num):
		if parameter == 0:
			return self.code[self.code[self.current_index + parameter_num]]
		elif parameter == 1:
			return self.code[self.current_index + parameter_num]

	def reset(self):
		self.code = None
		self.read()


if __name__ == "__main__":
	ic = intcode()
	ic.read("data.dat")
	output = ic.run(1)
	print("output: {}".format(output))

	#noun, verb = find_input("data.dat", 19690720)
	#print(100*noun + verb)

from string import ascii_lowercase
import random
from collections import Counter

class StreamGenerator:
	"""
	Stream Generator
	"""

	probabilities = None

	def __init__(self, from_sequence=None, stream_size=100, probability=None, delimiter=None, save_to_file=False):
		"""
		Generator Initialization

		Parameters
		----------
		from_sequence : str, optional (default=None)
			Base sequence on which the stream is generated

		stream_size: int, optional (default=100)
			Set stream size

		probability: list, optional (default=None)
			Probability of appearence of each item in stream

		delimiter: str, optional (default=None)
			in-stream item delimiter
		
		save_to_file: bool, optional (default=False)
			Save stream to a file

		"""

		assert isinstance(stream_size, int), print_assertion_error("stream_size", "int")
		assert isinstance(save_to_file, bool), print_assertion_error("save_to_file", "bool")

		if from_sequence == None:
			from_sequence = ascii_lowercase
		else:
			assert isinstance(from_sequence, str), print_assertion_error("from_sequence", "str")

		if delimiter == None:
			delimiter = ""
		else:
			assert isinstance(delimiter, str), print_assertion_error("delimiter", "str")

		self.from_sequence = from_sequence
		self.stream_size = stream_size
		self.delimiter = delimiter
		self.save_to_file = save_to_file
		self.probability = probability

	def assign_probabilities(self, letters_probability, verbose=False):
		"""
		Assign custom probabilities to chars in the sequence from which characters are chosen from to build stream

		Parameters
		----------
		letters_probability: dict
			Custom appearence probability of character in stream

		verbose: bool, optional (default=False)
			Print result of method
		"""

		probabilities = list()
		if sum(letters_probability.values()) >= 1:
			return "Given probabilities sum must be <= 1 (100%)."

		for c in ascii_lowercase:
			if c in letters_probability.keys():
				prob = letters_probability[c]
			else:
				prob = (1-sum(letters_probability.values()))/(len(ascii_lowercase)-len(letters_probability.keys()))

			probabilities.append(prob)

		if verbose:
			print("Probabilities:", probabilities)

		self.probabilities = probabilities

		return probabilities

	def generate_stream(self, letters_probability=None, verbose=False):
		"""
		Generate stream

		Parameters
		----------
		letters_probability: list, optional (default=None)
			Custom appearence probability of character in stream

		verbose: bool, optional (default=False)
			Print result of method
		"""

		assert isinstance(verbose, bool), print_assertion_error("verbose", "bool")

		sequence = ""
		if letters_probability == None:
			for _ in range(self.stream_size):
				sequence += random.choice(self.from_sequence)+self.delimiter
		else:
			self.assign_probabilities(letters_probability)

			for _ in range(self.stream_size):
				sequence += random.choices(self.from_sequence, weights=self.probabilities)[0]+self.delimiter

		if verbose:
			print("Sequence:", sequence[:-1])

		self.stream = sequence[:-1]

		if self.save_to_file:
			self.stream_to_file()

		return sequence

	def stream_statistics(self, verbose=False):
		"""
		Stream statistics

		Parameters
		----------
		verbose: bool, optional (default=False)
			Print result of method
		"""

		stream = sorted(self.stream.replace(" ", ""))
		counts = Counter(stream)

		if self.save_to_file:
			f = open("stats_stream_"+str(self.stream_size)+".txt", 'w')
			f.write("Stream Size: %s\nOriginal Chain: %s\n\n" % (self.stream_size, self.from_sequence))

		for item in counts:
			out = "Item: %s\tProbability: %s" % (item, counts[item]/self.stream_size)
			if verbose:
				print(out)
			if self.save_to_file:
				f.write(out+"\n")

		if self.save_to_file:
			f.close()

	def stream_to_file(self,filename="stream_"):
		"""
		Save stream to file

		Parameters
		----------
		filename: str, optional (default="stream_")
			Output file name
		"""

		assert isinstance(filename, str), print_assertion_error("filename", "str")

		filename = filename+"%s.strm" % self.stream_size
		f = open(filename, 'w')
		f.write(self.stream)
		f.close()
		

	def print_assertion_error(self, obj, type):
		"""
		Return Assertion Error Message
		"""

		return "Parameter %s type must be %s" % (obj, type)


letter_probabilities = {
	'r': 0.3,
	'u': 0.2,
	'i': 0.1
}


stream_length = [100, 1000, 10000, 100000, 1000000, 10000000]
for sl in stream_length:
	gen = StreamGenerator(stream_size=sl, delimiter=" ", save_to_file=True)
	gen.generate_stream(verbose=False, letters_probability=letter_probabilities)
	gen.stream_statistics(verbose=False)
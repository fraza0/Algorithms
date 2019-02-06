from collections import Counter

class MisraGries():
	"""
	Misra & Gries Implementation for Item Frequency Counting in Data Streams
	"""

	stream_size = 0

	def __init__(self, k):
		"""
		Initialization. Validation of parameter k

		Parameters
		----------
		k : int
			Total number of counters used equals k-1
		"""

		assert isinstance(k, int), print_assertion_error("k", "int")
		
		if k > 0:
			self.k = k
			self.counter = dict()
		else:
			return

	def misra_gries(self, item):
		"""
		Misra & Gries Algorithm

		Parameters
		----------
		item : str
			Stream item for counting
		"""

		assert isinstance(item, str), print_assertion_error("item", "str")

		if item==" ":
			return
		self.stream_size+=1
		if item in self.counter.keys():
			self.counter[item] += 1
		elif len(self.counter) < self.k-1:
			self.counter[item] = 1
		else:
			for key in list(self.counter.keys()):
				self.counter[key] -= 1
				if self.counter[key] == 0:
					del self.counter[key]

	def frequency_estimate(self, verbose=False):
		"""
		Print value of frequency in counter.

		Parameters
		----------
		verbose: bool, optional (default=False)
			Print result of method
		"""

		assert isinstance(verbose, bool), print_assertion_error("verbose", "bool")

		counter = dict(sorted(self.counter.items(), key=lambda counts: counts[1], reverse=True))
		estimate = dict()

		for key in counter:
			if key in counter.keys():
				freq_est = counter[key]
			else:
				freq_est = 0
			
			estimate[key] = freq_est
			if verbose:
				print("Character: {:<3}\tFrequency: {:<5}".format(key, freq_est))

		return estimate

	def get_counters_len(self):
		"""
		Return number of counters used
		"""
		
		return len(self.counter)

	def get_stream_size(self):
		"""
		Return Stream Size
		"""

		return self.stream_size



def print_assertion_error(obj, type):
	"""
	Return Assertion Error Message
	"""

	return "Parameter %s type must be %s" % (obj, type)
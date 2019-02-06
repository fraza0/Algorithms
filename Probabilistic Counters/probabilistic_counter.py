import random, time
from collections import Counter
from math import sqrt, pow, floor
import prob_counter_analysis as ca

test_chain = "ruifilipenunesfrazao"
test_chain_chars_size = len(set(test_chain))

seq_size = [100, 1000, 10000, 1000000]
n_repetitions = [10, 100, 1000, 10000]

log_prob_table = dict()

def print_list_of_dict(_dict, keys_only=False):
	"""
	Auxiliary Method for printing counters for each repetition

	Parameters
    ----------
    _dict : dict
        Dictionary containing a counter list per repetition  

    keys_only: bool, optional (default=False)
    	Print only the counter keys (characters)
	"""
	assert isinstance(_dict, dict),     printAssertionError("_dict", "dict")
	assert isinstance(keys_only, bool), printAssertionError("keys_only", "bool")

	for _list in _dict:
		if keys_only:
			print(list(_list.keys()))
		else:
			print(_list)


def estimate(probability, counter_value):
	"""
	Returns estimate for logarithmic decreasing probability counter

	Parameters
    ----------
    probability : float
        Decreasing counter probability

    counter_value: int
    	Counter value
	"""
	assert isinstance(probability, float), printAssertionError("probability", "float")
	assert isinstance(counter_value, int), printAssertionError("counter_value", "int")

	return floor((pow(probability, counter_value)-probability+1)/(probability-1))


def get_log_prob(prob, counter):
	"""
	Returns logarithmic decreasing probability value based on counter value
	If value is already calculated, returns it
	Else calculate and store it

	Parameters
    ----------
    prob : float
        Decreasing counter probability

    counter: int
    	Counter value
	"""
	assert isinstance(prob, float),  printAssertionError("prob", "float")
	assert isinstance(counter, int), printAssertionError("counter", "int")

	if counter in log_prob_table.keys():
		return log_prob_table[counter]
	
	log_prob_table[counter] = pow(prob, counter)
	return log_prob_table[counter]


def printAssertionError(obj, type):
	return "Parameter %s type must be %s" % (obj, type)


def generateSequence(size, chain=test_chain, verbose=False):
	"""
	Generate string sequence by picking random characters from a test chain.

	Parameters
    ----------
    size : int
        Size of sequence

    chain: str, optional (default=test_chain)
    	String from where the characters for the sequence are chosen from
	
	verbose: bool, optional (default=False)
		Print result of method
	"""
	assert isinstance(size, int), 	  printAssertionError("size", "int")
	assert isinstance(chain, str), 	  printAssertionError("chain", "str")
	assert isinstance(verbose, bool), printAssertionError("verbose", "bool")

	sequence = ""
	for _ in range(size):
		sequence += random.choice(chain)

	if verbose:
		print("Sequence:", sequence)
	return sequence

def exact_counting(sequence, verbose=False):
	"""
	Count exact number of ocurrences of unique characters in a string
	This method uses Collections.Counter()

	Parameters
    ----------
    sequence : str
        Sequence of characters to count

	verbose: bool, optional (default=False)
		Print result of method
	"""
	assert isinstance(sequence, str), printAssertionError("sequence", "str")
	assert isinstance(verbose, bool), printAssertionError("verbose", "bool")

	counter = Counter(sequence)
	sorted_counter = dict(sorted(counter.items(), key=lambda counts: counts[1], reverse=True))

	if verbose:
		print("Exact character counting:\n%s" % (sorted_counter))

	return sorted_counter

def approximate_counting_fixed_prob(sequence, n_repetitions, prob=(1/2), verbose=False):
	"""
	Count approximate number of ocurrences of unique characters in a string, using a fixed probability

	Parameters
    ----------
    sequence : str
        Sequence of characters to count

	n_repetitions: int
		Number of repetitions of the approximate counting process

	prob: float, optional (default=(1/2))
		Probability of counting an ocurrence

	verbose: bool, optional (default=False)
		Print result of method
	"""
	assert isinstance(sequence, str), 	   printAssertionError("sequence", "str")
	assert isinstance(n_repetitions, int), printAssertionError("n_repetitions", "int")
	assert isinstance(prob, float), 	   printAssertionError("prob", "float")
	assert isinstance(verbose, bool), 	   printAssertionError("verbose", "bool")

	counters = list()
	for i in range(n_repetitions):
		prob_counter = {char: 0 for char in sequence}
		for char in sequence:
			if random.random() < prob:
				prob_counter[char] += 1
		counters.append(prob_counter)

	for counter in range(len(counters)):
		counters[counter] = {char: counters[counter][char]*2 for char in counters[counter]}
		counters[counter] = dict(sorted(counters[counter].items(), key=lambda counts: counts[1], reverse=True))
	
	if verbose:
		print("Fixed probability character counter for %s repetitions:\t\t\t\t\t" % (n_repetitions))
		print_list_of_dict(counters)

	return counters

def approximate_counting_dec_log_prob(sequence, n_repetitions, dec_prob=(1/sqrt(2)), verbose=False):
	"""
	Count approximate number of ocurrences of unique characters in a string, using a logarithmic decreasing probability based on counter value

	Parameters
    ----------
    sequence : str
        Sequence of characters to count

	n_repetitions: int
		Number of repetitions of the approximate counting process

	dec_prob: float, optional (default=(1/sqrt(2)))
		Probability of counting an ocurrence

	verbose: bool, optional (default=False)
		Print result of method
	"""
	assert isinstance(sequence, str), 	  	printAssertionError("sequence", "str")
	assert isinstance(n_repetitions, int),	printAssertionError("n_repetitions", "int")
	assert isinstance(dec_prob, float), 	printAssertionError("dec_prob", "float")
	assert isinstance(verbose, bool), 		printAssertionError("verbose", "bool")

	counters = list()
	for i in range(n_repetitions):
		prob_counter = {char: 0 for char in sequence}
		for char in sequence:

			if random.random() <= get_log_prob(dec_prob, prob_counter[char]):
				prob_counter[char] += 1
		counters.append(prob_counter)

	for counter in range(len(counters)):
		counters[counter] = {char: estimate(sqrt(2), counters[counter][char]) for char in counters[counter]}
		counters[counter] = dict(sorted(counters[counter].items(), key=lambda counts: counts[1], reverse=True))

	if verbose:
		print("Approximate decreasing logarithmic probability character counter for %s repetitions:\t" % (n_repetitions))
		print_list_of_dict(counters)

	return counters


def print_output_to_file(outfilename, verbose=False):
	open(outfilename, 'w').close()
	with open(outfilename, "w") as outfile:
		if verbose:
			print("Test Chain:",test_chain, "\nNumber of unique characters in test chain:",test_chain_chars_size)
		outfile.write("Test Chain: %s\nNumber of unique characters in test chain: %s\n\n" % (test_chain, test_chain_chars_size))
		for n_rep in n_repetitions:
			start_time = time.time()
			if verbose:
				print("\n{:_^97}\n".format("REPETITIONS %s" % (n_rep)))
			outfile.write("{:_^97}\n".format("REPETITIONS %s" % (n_rep)))
			for size in seq_size:
				if verbose:
					print("\n{:_^97}\n".format("SEQUENCE SIZE %s" % (size)))
				outfile.write("\n{:_^97}\n".format("SEQUENCE SIZE %s" % (size)))
				sequence = generateSequence(size, verbose=False)

				exact = exact_counting(sequence, verbose=False)
				approximate_fixed = approximate_counting_fixed_prob(sequence, n_rep, verbose=False)
				approximate_dec_log = approximate_counting_dec_log_prob(sequence, n_rep, verbose=False)

				char_analysis = ca.print_table(exact, [approximate_fixed, approximate_dec_log])
				char_statistics = ca.statistics(exact, approximate_fixed)
				char_order = ca.order_comparison(list(exact.keys()), list(ca.counter_mean(approximate_fixed).keys()), list(ca.counter_mean(approximate_dec_log).keys()))
				if verbose:
					print(char_analysis, "\n")
					print(char_order)
					print("\n---Statistics---".upper())
					print("\nFixed Probability\n".upper())
					print(char_statistics)
					print("\nDecreasing Probability\n".upper())
					print("\n\nExecution Time: %s secs." % (time.time()-start_time))

				outfile.write("\n\n---COUNTER ANALYSIS---\n\n")
				outfile.write(char_analysis)
				outfile.write("\n\n---COUNTER ORDERING COMPARISON---\n\n")
				outfile.write(char_order)
				outfile.write("\n---STATISTICS---\n")
				outfile.write("\nFIXED PROBABILITY\n")
				outfile.write(ca.statistics(exact, approximate_fixed))
				outfile.write("\nDECREASING PROBABILITY\n")
				outfile.write(ca.statistics(exact, approximate_dec_log))
				outfile.write("EXECUTION TIME: %s secs.\n\n" % round(time.time()-start_time))


outfilename = "counters_output.txt"
print_output_to_file(outfilename)
import os
from collections import Counter
import misra_gries as mg
import frequent_count_analysis as fca

##setup
for file in os.listdir("./Output"):
	os.remove("./Output/"+file)

def exact_counter(stream):
		counter = Counter(stream.readline().replace(" ", ""))
		return dict(sorted(counter.items(), key=lambda counts: counts[1], reverse=True))

stream_length = [100, 1000, 10000, 100000, 1000000, 10000000]
for s in stream_length:
	stream = open("StreamFiles/stream_%s.strm" % s, 'r')
	exact = exact_counter(stream)
	outfilename = "Output/out_l%s.out" % s
	for k in range(2, 27):
		freq_count = mg.MisraGries(k)
		with open(outfilename, "a") as f:
			stream.seek(0)
			counter = dict()
			token = stream.read(1)

			while token != "":
				freq_count.misra_gries(token)
			
				token = stream.read(1)

			f.write("___ k=%s ___\n\n" % (k))
			estimate = freq_count.frequency_estimate()
			f.write(fca.counter_comparison(exact, estimate, freq_count.get_stream_size()))
			f.write("\n\n")
			fac_ord_comp = fca.order_comparison(exact, estimate)
			f.write(fac_ord_comp[0])
			f.write("\nUsed counters: %s of total %s" % (freq_count.get_counters_len(), k-1))
			acc = 0.0
			if freq_count.get_counters_len() != 0:
				acc = round(fac_ord_comp[1]/freq_count.get_counters_len()*100, 2)
			f.write("\nAccuracy: %s%%\n\n" % (acc))

	f.close()
from math import floor
import statistics as stats

def print_table(exact, counters, spacing=30):
    out_str = ""
    out_str += (("|{: ^%s}|{: ^%s}|{: ^%s} |{: ^%s} |\n" % (spacing-15, spacing-15, spacing, spacing)).format("Counter", "Exact", "Fixed Probability", "Decreasing Probability"))
    out_str += (("|{: ^%s}|{: ^%s}|{: ^%s}|{: ^%s}|{: ^%s}|{: ^%s}|{: ^%s}|{: ^%s}|{: ^%s}|{: ^%s}|\n" % (spacing-15, spacing-15, spacing/4, spacing/4, spacing/4, spacing/4, spacing/4, spacing/4, spacing/4, spacing/4)).format(" ", " ", "Min", "Avg", "Max", "Error", "Min", "Avg", "Max", "Error"))
    out_str += ("|{:-^95}|\n".format(""))
    chars = exact.keys()
    output = list()

    for char in chars:
        out_str += (("|{: ^%s}|" % (spacing-15)).format(char))
        out_str += (("{: ^%s}|" % (spacing-15)).format(exact[char]))
        for approximate in counters:
            max_value, min_value, counter_values = 0, float('inf'), list()
            for counter in approximate:
                counter_value = counter[char]
                if max_value < counter_value:
                    max_value = counter_value
                if min_value > counter_value:
                    min_value = counter_value
                
                counter_values.append(counter_value)
                average_counter_value = round(stats.mean(counter_values))
                abs_error = abs(exact[char]-average_counter_value)
                rel_error = round(abs_error/exact[char]*100, 2)
            out_str += (("{: ^%s}|{: ^%s}|{: ^%s}|{: ^%s}%%|" % (spacing-23, spacing-23, spacing-23, spacing-24)).format(min_value, average_counter_value, max_value, rel_error))
        out_str += "\n"
    return out_str

def statistics(exact, counters):
    out_str = ""
    chars = exact.keys()
    n_repetitions = len(counters)
    for char in chars:
        hits = 0
        out_str += ("===Character %s===\n\n" % char)
        char_list = list()
        for approximate in counters:
            char_list.append(approximate[char])

        # print(char_list)

        out_str += ("Exact count: %s\n" % exact[char])

        mean_abs_error = (stats.mean([abs(c-exact[char]) for c in char_list]))
        out_str += ("Mean Absolute Error: %s \n" % mean_abs_error)
        out_str += ("Mean Relative Error: %s %%\n\n" % round(mean_abs_error/exact[char]*100, 2))

        out_str += ("Max Counter Value: %s\n" % max(char_list))
        out_str += ("Min Counter Value: %s\n" % min(char_list))
        mean_counter_value = round(stats.mean(char_list))
        out_str += ("Mean Counter Value: %s\n\n" % mean_counter_value)

        out_str += ("Mean Absolute Deviation: %s \n" % (sum([abs(c-mean_counter_value) for c in char_list])/n_repetitions))
        out_str += ("Standard Deviation: %s \n" % round(stats.stdev(char_list), 2))
        out_str += ("Maximum Deviation: %s \n" % max([abs(c-mean_counter_value) for c in char_list]))
        out_str += ("Variance: %s\n" % round(stats.variance(char_list), 2))
        
        out_str += "\n\n"

    return out_str

def counter_mean(counter):
    if not isinstance(counter, list):
        return counter

    counter_sum = None

    n_repetitions = len(counter)

    for c in counter:
        if counter_sum == None:
            counter_sum = c
        else:
            counter_sum = { k: counter_sum.get(k, 0) + c.get(k, 0) for k in set(counter_sum) & set(c) }

    counters_average = {char: round(counter_sum[char]/n_repetitions) for char in counter_sum}
    counters_average = dict(sorted(counters_average.items(), key=lambda counts: counts[1], reverse=True))

    return counters_average

def order_comparison(exact, appr_fix, appr_dec, spacing=22):
    out_str = ""
    out_str += (("|{: ^%s}|{: ^%s}|{: ^%s}|{: ^%s}|{: ^%s}|\n" % (spacing, spacing, spacing, spacing, spacing)).format("Exact", "Fixed Probability", "Match Exact", "Decreasing Probability", "Match Exact"))
    out_str += (("|{:-^114}|\n".format("")))
    for i in range(len(exact)):
        out_str += (("|{: ^%s}|{: ^%s}|{: ^%s}|{: ^%s}|{: ^%s}|\n" % (spacing, spacing, spacing, spacing, spacing)).format(exact[i], appr_fix[i], str(bool(exact[i]==appr_fix[i])), appr_dec[i], str(bool(exact[i]==appr_dec[i]))))

    return out_str
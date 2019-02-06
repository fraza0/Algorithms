from math import floor
import statistics as stats

def counter_comparison(exact, freq_count, size, spacing=22):
    """
    Print table of values in each counter to compare with the exact counter. Non-used counters are represented by a "-" (dash).

    Parameters
    ----------
    exact : dict
        Dictionary contaning exact counting values

    freq_count: dict
        Dictionary contaning counting values by Misra & Gries Algorithm

    size: int
        Stream Size

    spacing: int, optional (default=22)
        Line spacing in prints
    """

    assert isinstance(exact, dict), print_assertion_error("exact", "dict")
    assert isinstance(freq_count, dict), print_assertion_error("freq_count", "dict")
    assert isinstance(size, int), print_assertion_error("size", "int")
    assert isinstance(spacing, int), print_assertion_error("spacing", "int")

    out_str = ""
    out_str += (("|{: ^%s}|{: ^%s}|{: ^%s}|{: ^%s}|{: ^%s}|{: ^%s}|\n" % (spacing-9, spacing-5, spacing-3, spacing-6, spacing-2, spacing-4)).format("Character", "Exact Counter", "Frequency Counter", "Absolute Error", "Relative Error (%)", "Distribution (%)"))
    out_str += (("|{:-^108}|\n".format("")))
    for c in exact:
        freq_char_count = 0
        if c in freq_count:
            freq_char_count = freq_count[c]

        if c in freq_count.keys():
            abs_error = exact[c]-freq_char_count
            rel_error = round((exact[c]-freq_char_count)/exact[c]*100, 2)
            distribution = round(freq_char_count/size*100, 2)
        else:
            abs_error = "-"
            rel_error = "-"
            distribution = "-"

        out_str += (("|{: ^%s}|{: ^%s}|{: ^%s}|{: ^%s}|{: ^%s}|{: ^%s}|\n" % (spacing-9, spacing-5, spacing-3, spacing-6, spacing-2, spacing-4)).format(c, exact[c], freq_char_count, abs_error, rel_error, distribution))

    return out_str

def order_comparison(exact, freq_count, spacing=22):
    """
    Print table of values of counters ordered by descending order to analyze counter order matches. Non-used counters are represented by a "-" (dash).

    Parameters
    ----------
    exact : dict
        Dictionary contaning exact counting values

    freq_count: dict
        Dictionary contaning counting values by Misra & Gries Algorithm

    spacing: int, optional (default=22)
        Line spacing in prints
    """

    assert isinstance(exact, dict), print_assertion_error("exact", "dict")
    assert isinstance(freq_count, dict), print_assertion_error("freq_count", "dict")
    assert isinstance(spacing, int), print_assertion_error("spacing", "int")

    out_str = ""
    out_str += (("|{: ^%s}|{: ^%s}|{: ^%s}|\n" % (spacing-5, spacing, spacing-11)).format("Exact Counter", "Frequency Counter", "Match"))
    out_str += (("|{:-^52}|\n".format("")))

    exact = list(exact.keys())
    freq_count = list(freq_count.keys())
    n_true = 0

    for i in range(len(exact)):
        freq_char = "-"
        if i < len(freq_count):
            freq_char = freq_count[i]

        result = ""
        if freq_char == "-":
            result = "-"
        else:
            result = bool(exact[i]==freq_char)
            if result:
                n_true+=1
            result = str(result)

        out_str += (("|{: ^%s}|{: ^%s}|{: ^%s}|\n" % (spacing-5, spacing, spacing-11)).format(exact[i], freq_char, result))

    return out_str, n_true


def print_assertion_error(self, obj, type):
    """
    Return Assertion Error Message
    """

    return "Parameter %s type must be %s" % (obj, type)
import math
import random
import time
import string
import re
import matplotlib.pyplot as plt

# ******************** constants: BEGIN ********************
EPSILON = 1e-15
N_ITERATIONS = 100000
N_DAYS_IN_YEAR = 365
N_DEFAULT_CLASS_SIZE = 23
N_SIM_SERIES = 6    # note that for formatting purposes, the number of series should be an even number > 0

S_ADD_SINGLETON_LIST_IDIOM = "t += [x] idiom"
S_LIST_APPEND_METHOD = "List.append() method"

LETTER_FREQ_TEMPLATE = "{}:\t{}\t(/{})\t\t{:0.2f}%"   # expect vals in this order: c, n_c, n_c_all, (n_c/n_c_all)*100

TEXT_FILE_SUMMARY_TEMPLATE = """
***** SUMMARY OF TEXT FILE: {} *****
    WORD COUNT: {}
    LETTER FREQUENCY:
        ALL:
{}
{}
{}
"""

QUIT_MESSAGE = "THAT'S ALL FOLKS!  Thanks for playing.  Bye bye."
# ******************** constants: END ********************




# ******************** functions: BEGIN ********************
def is_sorted(l):
    n = len(l)

    if n == 1:
        return True

    # since we compare indices i and i+1, we range from 0 to len(l)-2
    for i in range(n-1):  # recall that n-1 is not inclusive when using range()
        if l[i] > l[i+1]:
            return False 

    return True

def test_is_sorted(l):
    b_result = is_sorted(l)
    print(f"\tTEST is_sorted(l={l}): {b_result}")


def str_to_list(s):
    """
    This function converts a string to a list of chars (in case we want to modify the list somehow)
    """
    return [s[i] for i in range(len(s))] if type(s) is str else s.copy()


def to_lcase(l):
    """
    This function only convert char elements in the list to lower-case.
    Obviously, non-char elements will not be affected.
    """
    l_lcase = str_to_list(l)

    for i in range(len(l_lcase)):
        if type(l_lcase[i]) is str:
            l_lcase[i] = l_lcase[i].lower()

    return l_lcase


def is_anagram(l1, l2, normalize_char_case=True):
    """
    Normally anagrams are based on words only.
    But this function supports numeric lists as anagrams, as well..
    """

    n1 = len(l1)
    n2 = len(l2)

    # we can short-circuit when the lengths are unequal
    if n1 != n2:
        return False

    # we normally disregard case when considering char anagrams
    if normalize_char_case:
        l1 = to_lcase(l1)   # but remember, the to_lcase() leaves non-char elements alone
        l2 = to_lcase(l2)
    else: # in case strings and we don't want to normalize to lcase
        l1 = str_to_list(l1)
        l2 = str_to_list(l2)

    # here we sort each list
    #   this greatly simplifies the problem compared to not sorting
    if not is_sorted(l1):
        l1 = sorted(l1)
    if not is_sorted(l2):
        l2 = sorted(l2)

    # because the two lists are sorted, we can now short-circuit (exit the loop) when we encounter the first mismatch
    for i in range(n1):
        if l1[i] != l2[i]:
            return False
    
    # if we made it this far then the two lists are necessarily the same length and have the same elements (unless case matters, FOR STRINGS, and case differs for some element)
    return True

def test_is_anagram(l1, l2, normalize_char_case=True):
    b_result = is_anagram(l1, l2, normalize_char_case)
    print(f"\tTEST is_anagram(l1={l1}, l2={l2}, normalize_char_case={normalize_char_case}): {b_result}")



def has_duplicates(l, disregard_char_case=False):
    n = len(l)

    # a 0 or single element list is already implicitly sorted, so we can short-circuit
    if n < 2:
        return False

    if not disregard_char_case:
        l = to_lcase(l)
    else: # in case string and we don't want to normalize to lcase
        l = str_to_list(l)

    # here we sort the list
    #   this greatly simplifies the problem compared to not sorting
    if not is_sorted(l):
        l = sorted(l)

    # because the list is sorted, we can now short-circuit (exit the loop) when we encounter the first matching adjacent pair of elements
    #   range from 0 to len(l)-2
    for i in range(n-1):    # recall that n-1 is not inclusive when using range()
        if l[i] == l[i+1]:
            return True

    return False

def test_has_duplicates(l, disregard_char_case=False):
    b_result = has_duplicates(l, disregard_char_case=disregard_char_case)
    print(f"\tTEST has_duplicates(l={l}, disregard_char_case={disregard_char_case}): {b_result}")


def run_bd_paradox_sim(n_sims, n_class_size=N_DEFAULT_CLASS_SIZE, is_leap_year=False):
    print(f"Running {n_sims} Birthday Paradox simulations on a class size of {n_class_size} students...")
    p = 0
    n_dups = 0
    x = []
    y = []
    for i_sim in range(n_sims):
        l_birthdays = [random.randint(1, N_DAYS_IN_YEAR + (1 if is_leap_year else 0)) for i in range(n_class_size)]
        n_dups += 1 if has_duplicates(l_birthdays) else 0
        x.append(i_sim)
        y.append(n_dups / (i_sim+1))
    p = n_dups / n_sims
    print(f"\tDONE: The probability that at least 2 students from a class size of {n_class_size} have the same birthday converged to {p} after {n_sims} simulations.")

    return p, x, y

def run_bd_paradox_sim_series(n_powers_of_ten, n_class_size=N_DEFAULT_CLASS_SIZE, is_leap_year=False, do_plot=True):
    exponents = list(range(1,n_powers_of_ten+1))

    n_cols = 2
    n_rows = len(exponents) // n_cols
    if do_plot:
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(8,4))

    for i, e in enumerate(exponents):
        n_sims = 10**e
        p, x, y = run_bd_paradox_sim(n_sims=n_sims, n_class_size=N_DEFAULT_CLASS_SIZE, is_leap_year=False)
        if do_plot:
            axis = axes[i//n_cols][i%n_cols]
            axis.set_title(f"# sims = {n_sims}, p = {p}")
            axis.plot(x, y)

    if do_plot:
        fig.tight_layout()
        plt.show()


def remove_duplicates(l):
    l = str_to_list(l)  # in case l is a string

    n = len(l)

    # a 0 or single element list is already implicitly sorted, so we can short-circuit
    if n < 2:
        return l

    # here we sort the list
    #   this greatly simplifies the problem compared to not sorting
    if not is_sorted(l):
        l = sorted(l)

    l_dups_removed = []
    
    # iterate from index 0 to len(l)-2
    #   only add the last non-repeating element, which we can do since the list has been sorted
    for i in range(n-1): # recall that n-1 is not inclusive when using range()
        if l[i] != l[i+1]:
            l_dups_removed.append(l[i])

    # but we still have the very last index to add
    #   this works since if there was a dup at the n-2 index, it will not have been added to l_dups_removed
    l_dups_removed.append(l[n-1])

    return l_dups_removed

def test_remove_duplicates(l):
    b_result = remove_duplicates(l)
    print(f"\tTEST remove_duplicates(l={l}): {b_result}")


def words_file_to_list(fname, use_list_append=True):
    l_words = []

    try:
        with open(fname, 'r') as f_words:
            for words_line in f_words:
                for word in words_line.split():
                    if use_list_append:
                        l_words.append(word.strip()) # dynamically resizes 
                    else:
                        l_words += [word] # adding to separate lists (which exist in two different places in memory)
            f_words.close()
    except Exception as e:
        print(f"words_file_to_list: ***RUNTIME ERROR caught***: {e}")

    return l_words

def benchmark_words_file_to_list(fname, use_list_append, debug=False):
    if debug:
        s_append_list_mechanic = ("t += [x] idiom" if not use_list_append else S_LIST_APPEND_METHOD)
        print(f"Benchmarking '{fname}' file to words list (using {s_append_list_mechanic})")

    # timestamp for start of the execution of words_file_to_list()
    t0 = time.time()

    # execute words_file_to_list()
    l_words = words_file_to_list(fname)

    # timestamp for end of the execution of words_file_to_list()
    t1 = time.time()

    # the delta is just the elapsed time
    t_delta = (t1 - t0) + EPSILON

    if debug:
        print(f"\ttime elapsed (using {s_append_list_mechanic}): {t_delta} seconds") # CPU seconds elapsed (floating point)

    return t_delta, l_words

def run_benchmark_words_file_to_list_series(fname, n_sims, debug=False):
    n_list_append_more_efficient = 0
    n_add_singleton_list_idiom_more_efficient = 0

    print(f"Running {n_sims} words_file_to_list() iterations...")

    for i_sim in range(n_sims):
        # benchmark using List.append()
        tdelta__list_append, l_words = benchmark_words_file_to_list(fname, use_list_append=True, debug=debug)

        if debug:
            print()

        # benchmark using the t += [x] idiom
        tdelta__add_list_idiom, l_words = benchmark_words_file_to_list(fname, use_list_append=False, debug=debug)

        # the rest of this code is just for formatting the summary output when debugging
        s_mech = ""
        eff_factor = 0

        # update summary and count of times the particular mechanic is more efficient
        if tdelta__add_list_idiom < tdelta__list_append:
            s_mech = S_ADD_SINGLETON_LIST_IDIOM
            eff_factor = tdelta__list_append / tdelta__add_list_idiom
            n_add_singleton_list_idiom_more_efficient += 1
        else:
            s_mech = S_LIST_APPEND_METHOD
            eff_factor = tdelta__add_list_idiom / tdelta__list_append
            n_list_append_more_efficient += 1

        s_efficiency = f"{s_mech} is {eff_factor} more efficient!"

        if debug:
            # print(f"\n{s_efficiency}\n\n{l_words}") # uncomment this to see l_words
            print(f"\n{s_efficiency}")

    # always display summary after all simulations are complete
    eff_ratio__list_append = n_list_append_more_efficient/n_sims
    eff_ratio__add_singleton_list = 1 - eff_ratio__list_append
    print(f"\tDONE: Out of {n_sims} iterations, {S_LIST_APPEND_METHOD} was more efficient {round(eff_ratio__list_append,2)*100}% of the time, while {S_ADD_SINGLETON_LIST_IDIOM} was more efficient {round(eff_ratio__add_singleton_list,2)*100}% of the time.")


def bisect(l, i_lb, i_ub, target_value, debug=False):
    """
    This function implements what is also known as 'binary search'.

    This implementation is based on RECURSION and is adapted from https://www.geeksforgeeks.org/python-program-for-binary-search/

    Even though the spec we are given indicates we can assume l is already sorted, we will double-check and do the sorting just in case.

    parameters:
        l:      the list (elements should all be of the same type and comparable)
        i_lb:   the index lower-bound of l to search
        i_ub:   the index upper-bound of l to search

    From our spec:
        'to check whether a <value> is in the list'
        'returns the index of the value in the list, if it’s there, or None if it’s not'
    """

    # short-circuit for 0-length and singleton lists, this is also the "base case" when recursion is used (but we will go the iteration route instead of recursion)
    n = len(l)
    if n == 0:
        return None
    if n == 1:
        return 0 if l[0] == target_value else None

    # is_sorted check: avoid performance hit (checking if sorted only at top level) - i.e. only when i_lb==0 AND i_ub==len(l)-1
    if i_lb==0 and i_ub==len(l)-1:
        if not is_sorted(l):
            if debug:
                print("\tl is not sorted! sorting...")
            l = sorted(l)
            if debug:
                # print(f"\t\tsorted l: {l}")
                print(f"\t\tDONE")
        print(f"\tbisecting l for target value -->{target_value}<-- ...")

    # if we are here, we are guaranteed that l is sorted... now we can implement proper binary search logic
    #   first step is to validate that i_ub >= i_lb
    if i_ub >= i_lb:
        
        # since we are here, we can proceed with "bisecting"
        #   so the first thing we need to do is find the midpoint between i_ub and i_lb: this is the basis of "bisection"
        i_midpoint = (i_ub + i_lb) // 2     # integer division

        val_at_midpoint = l[i_midpoint]

        if debug:
            print(f"\t\tmidpoint (index) of l between index {i_lb} and {i_ub} is: {i_midpoint} and l[{i_midpoint}]=={val_at_midpoint}")
        
        # if target_value is at index i_midpoint, return i_midpoint
        if val_at_midpoint == target_value:
            if debug:
                print(f"\t\ttarget value -->{target_value}<-- found at midpoint index {i_midpoint}")
            return i_midpoint

        else:   # we have already excluded the equality case

            # now we use the fact that elements in l are comparable... this happens recursively
            if target_value < val_at_midpoint:  # then we look in the left half... this is the binary split
                return bisect(l, i_lb, i_midpoint, target_value, debug)

            else:   # otherwise we look in the right half... this happens recursively
                return bisect(l, i_midpoint, i_ub, target_value, debug)

    else: # i_ub < i_lb  (which is illogical, therefore return None)
        return None

def test_bisect(l, i_lb, i_ub, target_value, debug=True):
    result = bisect(l, i_lb, i_ub, target_value, debug=debug)
    print(f"\tTEST bisect(l={l if len(l)<50 else '<l contents SUPRESSED due to length>'}, i_lb={i_lb}, i_ub={i_ub}, target_value={target_value}): {result}")


def process_token_to_word(tkn):
    """
    This function's sole purpose is to "clean" a token and return a word (or None if the token is not actually a word).

    For instance, we want to strip preceding and trailing whitespace if any exists.

    We also want to remove punctuation characters.
    """

    if tkn is None:
        return None

    tkn = tkn.strip()
        
    # strip punctuation
    tkn = re.sub(r"[^\w\s]", "", tkn)
    
    if len(tkn) == 0:
        return None

    return tkn

def tokens_list_to_inverted_index(l_tokens, fn_process_token_to_word=process_token_to_word, debug=False):
    """
    This function converts a list of tokens into two dictionaries:
        1. the first dictionary is keyed by each unqiue word and the corresponding value is the count of that word
        2. the second dictionary is keyed by each unqiue character and the corresponding value is the count of that character

    The above happens AFTER the token is cleaned by the function specified by the fn_process_token_to_word argument
    """

    d_w_index = {}
    d_c_index = {}
    
    for tkn in l_tokens:
        w = fn_process_token_to_word(tkn)

        if w is not None:
            w_lower = w.lower()
            d_w_index[w_lower] = d_w_index.get(w_lower, 0) + 1
            
            for c in w:
                d_c_index[c] = d_c_index.get(c, 0) + 1

    return d_w_index, d_c_index


def summarize_text_file(fname):
    """
    This function opens a text file and summarizes its word count and letter count.

    Note that case matters!

    arguments:
        fname

    returns:
        1. the summary string, which is formatted, containing the summary statistics:
            1. the frequency count that each (case-sensitive) letter occurs (out of the total number of letters), as well as the frequency ratio (as a percentage)
            2. the frequency (count and ratio) of upper-case letters as a group
            3. the frequency (count and ratio) of lower-case letters as a group

        2. a dictionary keyed by words, containing the count of each unique word

        3. a dictionary keyed by letter, containing the count of each unique letter

    """

    l_words = words_file_to_list(fname, use_list_append=False)

    d_w_index, d_c_index = tokens_list_to_inverted_index(l_words)

    n_words = 0
    for k in d_w_index.keys():
        n_words += d_w_index[k]

    # re-arrange d_c_index so that keys are in alphabetical order (based on sorted() order)
    d_c_index = {k:d_c_index[k] for k in sorted(d_c_index.keys())}

    # count all letters (so that we can provide frequency of each letter as a ratio or percentage)
    n_c_all = sum([n_c for _, n_c in d_c_index.items()])

    # now create separate counts of upper and lower case letter (and create formatted individual letter freq summary)
    s_letter_freq__all = ""
    n_c_uc = 0
    n_c_lc = 0
    for c, n_c in d_c_index.items():
        s_letter_freq__all += "\t\t\t" + LETTER_FREQ_TEMPLATE.format(c, n_c, n_c_all, (n_c/n_c_all)*100) + "\n"

        if c.isalpha():
            if c.isupper():
                n_c_uc += n_c
            else:
                n_c_lc += n_c

    # now create summary strings of upper and lower case freqs
    s_letter_freq__ucase = "\t" + LETTER_FREQ_TEMPLATE.format("UPPER-CASE", n_c_uc, n_c_all, (n_c_uc/n_c_all)*100)
    s_letter_freq__lcase = "\t" + LETTER_FREQ_TEMPLATE.format("LOWER-CASE", n_c_lc, n_c_all, (n_c_lc/n_c_all)*100)

    # return entire formatted summary string as well as the dictionaries (in case we want to use them later)
    return TEXT_FILE_SUMMARY_TEMPLATE.format(
        fname,
        n_words,
        s_letter_freq__all,
        s_letter_freq__ucase,
        s_letter_freq__lcase
    ), d_w_index, d_c_index


def words_file_to_toggle_case(fname_in, fname_out):
    try:
        with open(fname_in, 'r') as f_words_in:
            with open(fname_out, 'w') as f_words_out:
                for words_line_in in f_words_in:
                    words_line_out = ""
                    for c_in in words_line_in:
                        if c_in.isalpha():
                            if c_in.isupper():
                                words_line_out += c_in.lower()
                            else:
                                words_line_out += c_in.upper()
                        else:
                            words_line_out += c_in
                    f_words_out.write(words_line_out)
                f_words_out.close()
                print(f"{fname_out} file written")
            f_words_in.close()
    except Exception as e:
        print(f"words_file_to_toggle_case: ***RUNTIME ERROR caught***: {e}")
# ******************** functions: END ********************




# **************************************** main body (simply calls main() when this py file is exec'ed from bash): BEGIN ****************************************
if __name__ == '__main__':
    print("Testing is_sorted()...")
    test_is_sorted([1,2,2])
    test_is_sorted(['b','a'])
    test_is_sorted(['b','a','b'])
    print()


    print("Testing is_anagram()...")
    test_is_anagram("never", "REven")
    test_is_anagram("steve", "STEVEN")
    print()


    print("Testing has_duplicates()...")
    test_has_duplicates([1,2,3])
    test_has_duplicates([1,2,1])
    test_has_duplicates(['a','b','c'])
    test_has_duplicates(['a','b','a'])
    test_has_duplicates(["steven", "steve"])
    test_has_duplicates(["steven", "steven"])
    test_has_duplicates([0])
    test_has_duplicates([])
    print()


    run_bd_paradox_sim_series(N_SIM_SERIES) # note that for formatting purposes, the number of series should be an even number > 0
    print()


    print("Testing remove_duplicates()...")
    test_remove_duplicates("steven")
    test_remove_duplicates([1,2,3,4,2,1])
    test_remove_duplicates(['s','t','e','v','e','n'])
    print()


    fname = "mobysmall.txt"
    run_benchmark_words_file_to_list_series(fname, N_ITERATIONS, debug=False) # set debug to True will produce A LOT of output... use it only if you think something is broken
    print()


    print("Testing bisect()...")
    print(f"\tloading word list from {fname}...")
    l_words = words_file_to_list(fname, use_list_append=False)
    print(f"\t\tDONE")
    test_bisect(l_words, 0, len(l_words)-1, "a", debug=True)    # set debug to False for less output
    print()


    s_text_file_summary, _, d_c_index = summarize_text_file(fname)
    print(s_text_file_summary)
    

    words_file_to_toggle_case("mobysmall.txt", "mobysmall-case-toggled.txt")


    try:
        with open("mobysmall-summary.txt", "w") as f_summary_out:
            f_summary_out.write(s_text_file_summary)
            f_summary_out.close()
            print(f"mobysmall-summary.txt file written")
    except Exception as e:
        print(f"write textfile summary: ***RUNTIME ERROR caught***: {e}")


    # histogram (bar chart) creation
    fig = plt.figure(figsize=(8,4))
    x = d_c_index.keys()
    y = [d_c_index[c] for c in x]
    plt.bar(x, y)
    plt.title(f"Letter frequency for {fname}")
    plt.show()

    
    print(f"\n{QUIT_MESSAGE}\n\n")
# **************************************** main body (simply calls main() when this py file is exec'ed from bash): END ****************************************
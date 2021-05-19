## CSULB

## CECS

```
Project 6
```
```
You are to work in groups of 3 students, self-enrolled group members
```
```
Objectives: Sequence Type, functions and files.
```
```
You are to write multiple functions and then to call them from main using the same order:
```
A- Write a function called **is_sorted** that takes a **list** as a parameter and returns True if the list is **sorted in
ascending** order and False otherwise.
You can assume that the elements of the list can be compared with the relational operators <, >, etc.
For example, is_sorted([1,2,2]) should return True and is_sorted(['b','a']) should return False.

B- Two words are anagrams if you can rearrange the letters from one to spell the other. Write a function
called **is_anagram** that takes two strings and returns True if they are anagrams.

C- The Birthday Paradox:
Write a function called **has_duplicates** that takes a list and returns True if there is any element that
appears more than once. **It should not modify the original list.**
If there are 23 students in your class, what are the chances that two of you have the same birthday? You
can estimate this probability by generating random samples of 23 birthdays and checking for matches.
Hint: you can **generate random birthdays with the randint function in the random module**.

```
You can read about this problem at https://en.wikipedia.org/wiki/Birthday_problem
```
D- Write a function called **remove_duplicates** that takes a list and returns a new list with only the unique
elements from the original. Hint: they don’t have to be in the same order.
E- Write a function that reads the file words.txt (You create your own file) and builds a list with one element
per word. Write two versions of this function, one using the **append method** and the other using the
idiom **t = t + [x]**. Which one takes longer to run? Why?
_use the_ **_time module to measure elapsed time check the following example_**_._
import time
t0= time.time()
print( **"Hello"** )
t1 = time.time() - t
print( **"Time elapsed: "** , t1) _# CPU seconds elapsed (floating point)_

F- To check whether a word is in the word list, you could use the **in** operator, but it would be slow because it
searches through the words in order.
Because the words are in alphabetical order, we can speed things up with a bisection search (also known
as binary search), which is similar to what you do when you look a word up in the dictionary.
You start in the middle and check to see whether the word you are looking for comes before the word in
the middle of the list. If so, then you search the first half of the list the same way. Otherwise you search
the second half. Either way, you cut the remaining search space in half. If the word list has 113,809 words,
it will take about 17 steps to find the word or conclude that it’s not there.
Write a function called **bisect** that takes a sorted list and a target value and returns the index of the value
in the list, if it’s there, or None if it’s not.

G- Write a function that counts the number of times each unique letter (character) occurs in a sentence
entered by the user or in words in a list, and then output the result for each character in the sentence.


```
Hint:
```
- keep the count in a dictionary.
- get the keys from the dictionary and convert them to a list using: list(dictionary_name.keys())
    check the example below.
- Sort the keys, and iterate through them in alphabetical order -don’t forget to associate the key
    with the count when you are sorting the keys.
- Make a histogram bar for each letter (Extra credit)

```
foo = { 'bar': "hello", 'baz': "world" }. # this is a dictionary
ls= list(foo.keys()). #converting a dictionary to a list
print (ls)
```
```
H- Read the Moby Deck text file. Find out the:
```
1. Number of words in the file.
2. The frequency of each letter in the file
3. The frequency of upper case letters file
4. The frequency of lower case letters in the file
5. Convert all uppercase to lower case and vise versa, write in a new file.
6. Towards the end of the file (or in a new file) write the results of 1 - 4 in an output text file
7. Plot the letter frequency.

```
For plotting information please visit
https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html
```
Work as a **group** , however, demonstrate as a group -I want to hear every group member- and **submit as a group**.
Only one of you to submit. Paste a copy of your code, a screenshot of the output, a link to a short video explaining
your code and the output using pdf formatting, a screenshot of your output file(s) and upload as a pdf.

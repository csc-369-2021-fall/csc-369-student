
import sys

def count_words_book(book):
    file = open(book).read()
    book_word_freq = {}
    # YOUR SOLUTION HERE
    return book_word_freq
    
book = sys.argv[1]
count_words_book(book) # I am not printing the output on purpose because we are timing this.

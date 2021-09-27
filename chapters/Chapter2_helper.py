def count_words_book(book):
    file = open(book).read()
    book_word_freq = {}
    # YOUR SOLUTION HERE
    return book_word_freq

def count_words(book_files):
    book_word_freq = {}
    for book in book_files:
        book_word_freq[book] = count_words_book(book)
    return book_word_freq
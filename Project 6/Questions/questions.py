import nltk
import sys

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    import os
    # A dictionary with all files in the directory specified
    corpus = {
        f: "" for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    }

    # Assigning the content of each files to it in the dictionary
    for f in corpus:
        with open(os.path.join(directory, f), encoding="utf8") as document:
            corpus[f] = document.read()

    return corpus


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # for stopwords execute:
    # nltk.download('stopwords')
    # for word tokenize execute:
    # nltk.download('punkt')
    from string import punctuation
    stopwords = nltk.corpus.stopwords.words("english")

    # Removing every punctuation character in the document
    for char in punctuation:
        document = document.replace(char, " ")

    # Return a list of tokenized words with the stopwords filtered out
    return list(filter(
        lambda word: False if word in stopwords else True,
        nltk.word_tokenize(document.lower())
    ))


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    from math import log
    # A method for dividing the number of documents by a number
    def divide_by(x): return 1 if x == 0 else len(documents) / x

    # Return a dictionary of words for all words in documents and assigning idf value for each one
    return {
        w: log(divide_by(sum(1 for d in documents if w in documents[d])))
        for document in documents for w in documents[document]
    }


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # Dictionary that will hold the tf-idf value for all combinations of files and words in query
    tfidfs = {(f, w): 0 for f in files for w in query}

    # Finding tf and idf for each word and storing it in tf-idf dictionary
    for f, w in tfidfs:
        tf = sum(1 for word in files[f] if word == w) if w in files[f] else 0
        idf = idfs[w] if w in idfs else 0
        tfidfs[(f, w)] = tf * idf

    # Return a sorted list of the highest n files according to tf-idf with respect to query
    return sorted(
        [filename for filename in files],
        key=lambda f: sum(tfidfs[(f, w)] for w in query),
        reverse=True
    )[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # A dictionary that contains the idf value for a sentence and the query term density of the sentence
    matching = {
        sentence: {
            "idf": sum(idfs[w] for w in query if w in sentences[sentence] and w in idfs),
            "term_density": sum(1 for w in query if w in sentences[sentence]) / len(sentences[sentence])
        }
        for sentence in sentences
    }

    # Return a sorted list of the highest n sentences according to idf value (or query term density) with respect to query
    return sorted(
        [sentence for sentence in sentences],
        key=lambda s: (matching[s]["idf"], matching[s]["term_density"]),
        reverse=True
    )[:n]


if __name__ == "__main__":
    main()

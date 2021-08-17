#!/usr/bin/env python3
# summarize text.

from sys import stdin
from re import sub
from nltk import tokenize
from math import log
from argparse import ArgumentParser

def sentences(text):
    """Break a text into a list of sentences."""
    return list(tokenize.sent_tokenize(text))

def tokens(text, stopwords=None):
    """Break a text into a list of tokens.

    Parameters
    ----------
    text : str
        A text to tokenize.
    stopwords : list (default:None)
        A list of stopwords to exclude from the resulting tokens. If
        stopwords is None, no tokens are excluded.

    Returns
    -------
    list
        A list of tokens."""
    text = sub("r[^a-zA-Z0-9\-' ]+", '', text.lower())
    tokens = text.split()
    if stopwords is None:
        result = tokens
    else:
        result = [token for token in tokens if token not in stopwords]
    return result

class Sentence:
    """A Sentence class."""
    instance = 0
    def __init__(self, parent, text):
        """
        Parameters
        ----------
        parent : SentenceCollection
            The parent of this object.
        text : str
            A sentence.
        """
        self.text = text
        self.tokens = tokens(text, parent.stopwords)
        for token in self.tokens:
            parent.token_counts.setdefault(token, 0)
            parent.token_counts[token] += 1
        for token in set(self.tokens):
            parent.document_matches.setdefault(token, 0)
            parent.document_matches[token] += 1
        self.instance = Sentence.instance
        Sentence.instance += 1

    def __lt__(self, other):
        return self.instance < other.instance

    def __repr__(self):
        return self.text

class SentenceCollection:
    """A collection of sentences."""
    def __init__(self, stopwords=None):
        self.sentences = []
        self.token_counts = {}
        self.document_matches = {}
        self.stopwords = stopwords

    def add(self, text):
        """Add a sentence to the collection.

        Parameters
        ----------
        text : str
            A sentence.
        """
        sentence = Sentence(self, text)
        self.sentences.append(sentence)

    def compute(self):
        """Compute the top scoring sentences.

        Sentences are scored by summing the TF-IDF value for all its tokens.
        """
        values = dict.fromkeys(self.token_counts.keys(), 0)
        total_tokens = sum([self.token_counts[token] for token in values])
        total_sentences = len(self.sentences)

        #compute TF-IDFs for all tokens
        for token in values:
            tf = self.token_counts[token] / total_tokens
            idf = log(total_sentences / self.document_matches[token])
            values[token] = tf * idf

        #return all sentences sorted by their score (TF-IDF sum term-by-term)
        score = lambda s: sum([values[t] for t in s.tokens])
        return sorted(self.sentences, key=score, reverse=True)

def main(args):
    if args.filename == "-":
        text = stdin.read()
    else:
        with open(args.filename, "r") as f:
            text = f.read()
    if args.stop is None:
        stopwords = None
    else:
        with open(args.stop[0], "r") as f:
            stopwords = f.read().split()
    collection = SentenceCollection(stopwords)
    for sentence in sentences(text):
        collection.add(" ".join(sentence.split()))
    if args.num <= 0:
        args.num = len(collection.sentences)
    for sentence in sorted(collection.compute()[:args.num]):
        print(sentence)

if __name__ == "__main__":
    parser = ArgumentParser(description="Summarize text.")
    parser.add_argument("filename", type=str, nargs="?", default="-",
        help="A file to read text from")
    parser.add_argument("-n", "--num", type=int, default=5,
        help="The number of sentences to print")
    parser.add_argument("-s", "--stop", type=str, nargs=1, default=None,
        help="A file with stopwords to load")
    args = parser.parse_args()
    main(args)


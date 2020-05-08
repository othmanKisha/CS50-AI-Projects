import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Initializing the distribution for each page to zero
    prob_dist = {p: 0 for p in corpus}

    # N is the number of pages in the corpus
    N = len(corpus)

    # Outgoing is the number of links in the page
    outgoing = len(corpus[page])

    if outgoing == 0:
        for p in prob_dist:
            prob_dist[p] = 1 / N
    else:
        for p in prob_dist:
            prob_dist[p] = (1 - damping_factor) / N
            if p != page and p in corpus[page]:
                prob_dist[p] += damping_factor / outgoing

    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initializing the pages' PageRank to zero
    PageRanks = {page: 0 for page in corpus}

    for turn in range(n):

        # If we are in the first turn, pick a random page
        if turn == 0:
            random_sample = random.randint(1, len(corpus))

        # Else pick a weighted random page depending on the previous turn
        else:
            weights = []
            for i in range(len(corpus)):
                weights += [i + 1] * int(trans[f"{i + 1}.html"]*100)
            random_sample = random.choice(weights)

        page = f"{random_sample}.html"
        PageRanks[page] += 1
        trans = transition_model(corpus, page, damping_factor)

    # Making the sum of all pages' PageRank equal to 1
    PageRanks = {page: PageRanks[page] / n for page in corpus}

    return PageRanks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Making every page that has 0 outgoing Links, connected to every page in the corpus including itself
    for page in corpus:
        if len(corpus[page]) == 0:
            corpus[page] = set([p for p in corpus])

    # The number of pages in the corpus
    N = len(corpus)

    # Initializing each page to have a page rank of 1/N
    PageRanks = {page: 1 / N for page in corpus}

    # Variable that indicates if we have a new iteration or not
    new_iteration = True

    while new_iteration:

        # Assigning the previous ranks to prev
        prev = {page: PageRanks[page] for page in PageRanks}

        for p in corpus:
            PageRanks[p] = (1 - damping_factor) / N
            for i in corpus:
                if p in corpus[i] and p != i:

                    # Number of links outgoing from page i
                    NumLinks = len(corpus[i])

                    PageRanks[p] += damping_factor * (prev[i] / NumLinks)

        # Checking if all pages haven't change by more than 0.001, if not go to a new iteration
        if all(PageRanks[p] - prev[p] <= 0.001 for p in corpus):
            new_iteration = False

    return PageRanks


if __name__ == "__main__":
    main()

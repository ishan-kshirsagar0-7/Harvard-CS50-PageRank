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
    dist1 = {}
    length_dict = len(corpus.keys())
    length_pgs = len(corpus[page])

    if len(corpus[page]) < 1:
        for key in corpus.keys():
            dist1[key] = 1 / length_dict
    else:
        fact1 = (1 - damping_factor) / length_dict
        fact2 = damping_factor / length_pgs
        for key in corpus.keys():
            if key not in corpus[page]:
                dist1[key] = fact1
            else:
                dist1[key] = fact2 + fact1

    return dist1


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dict_sample = corpus.copy()
    for i in dict_sample:
        dict_sample[i] = 0
    sample = None

    for _ in range(n):
        if sample:
            model = transition_model(corpus, sample, damping_factor)
            model_list = list(model.keys())
            model_weights = [model[i] for i in model]
            sample = random.choices(model_list, model_weights, k=1)[0]
        else:
            sample = random.choice(list(corpus.keys()))

        dict_sample[sample] += 1

    for item in dict_sample:
        dict_sample[item] /= n

    return dict_sample


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    no_of_pgs = len(corpus)
    dict1 = {}
    dict2 = {}

    for pg in corpus:
        dict1[pg] = 1 / no_of_pgs

    while True:
        for pg in corpus:
            k = 0
            for side_pg in corpus:
                if pg in corpus[side_pg]:
                    k += (dict1[side_pg] / len(corpus[side_pg]))
                if len(corpus[side_pg]) == 0:
                    k += (dict1[side_pg]) / len(corpus)

            k *= damping_factor
            k += (1 - damping_factor) / no_of_pgs
            dict2[pg] = k

        diff = max([abs(dict2[x] - dict1[x]) for x in dict1])
        if diff < 0.001:
            break
        else:
            dict1 = dict2.copy()

    return dict1


if __name__ == "__main__":
    main()

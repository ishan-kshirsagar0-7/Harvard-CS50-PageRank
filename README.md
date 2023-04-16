# Harvard CS50 AI (Week 2) Project 5 : PageRank

This is the fifth project of [Harvard CS50's Introduction to Artificial Intelligence course](https://cs50.harvard.edu/ai/2020/), first project of Week 2.

## My Outputs

![Screenshot of my output on terminal](https://cdn.discordapp.com/attachments/1091358303063396496/1097292289161842750/image.png)

## Objective

Write an AI to rank web pages by importance.

## Background

When search engines like Google display search results, they do so by placing more “important” and higher-quality pages higher in the search results than less important pages. But how does the search engine know which pages are more important than other pages?

One heuristic might be that an “important” page is one that many other pages link to, since it’s reasonable to imagine that more sites will link to a higher-quality webpage than a lower-quality webpage. We could therefore imagine a system where each page is given a rank according to the number of incoming links it has from other pages, and higher ranks would signal higher importance.

But this definition isn’t perfect: if someone wants to make their page seem more important, then under this system, they could simply create many other pages that link to their desired page to artificially inflate its rank.

For that reason, the PageRank algorithm was created by Google’s co-founders (including Larry Page, for whom the algorithm was named). In PageRank’s algorithm, a website is more important if it is linked to by other important websites, and links from less important websites have their links weighted less. This definition seems a bit circular, but it turns out that there are multiple strategies for calculating these rankings.

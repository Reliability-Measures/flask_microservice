"""
Sample code showing how to scrap a site for data
Want to extract from https://www.sanfoundry.com/python-questions-answers-variable-names/
and other links from this site
https://www.sanfoundry.com/1000-python-questions-answers/
and
https://www.geeksforgeeks.org/functions-python-gq/
https://www.tutorialspoint.com/python/python_online_quiz.htm

"""

import requests
from html.parser import HTMLParser

google_news_url = "https://news.google.com/news/rss"

# class MyHTMLParser(HTMLParser):
#     start_tag = None
#     titles = []
#
#     def handle_starttag(self, tag, attrs):
#         if tag == 'title':
#             self.start_tag = tag
#             # print("Encountered a start tag:", tag)
#
#     def handle_endtag(self, tag):
#         if self.start_tag:
#             # print("Encountered an end tag :", tag)
#             self.start_tag = None
#
#     def handle_data(self, data):
#         if self.start_tag:
#             # print("Encountered some data  :", data)
#             self.titles.append(data)


# def get_headlines(rss_url):
#     """
#     @returns a list of titles from the rss feed located at `rss_url`
#     """
#     resp = requests.get(quiz_url)
#     parser = MyHTMLParser()
#     parser.feed(resp.text)
#     # print(len(parser.titles))
#     return parser.titles

class MyHTMLParser(HTMLParser):
    start_tag = None
    data = []

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.start_tag = tag
            #print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        if tag == self.start_tag:
            #print("Encountered an end tag :", tag)
            self.start_tag = None

    def handle_data(self, data):
        if self.start_tag:
            #print("Encountered some data  :", data)
            self.data.append(data)


# WIP
def parse_html(url, file):
    f = open(file, "x")
    r = requests.get(url)
    parser = MyHTMLParser()
    parser.feed(r.text)
    for i in parser.data:
        f.write(i)
    f.close()


quiz_url = "https://www.sanfoundry.com/python-mcqs-core-datatypes/"
parse_html(quiz_url, "scraped texts\sanfoundry2.txt")

# Get info from Wolfram Alpha
# Python 2.7
from bs4 import BeautifulSoup
import requests
import json
appid = "XXX"


class WolframRequest(object):

    def __init__(self, query):
        self.query = query
        self.xml = get_xml(self.query)
        self.status = True
        if not self.xml is None:
            self.extracted = extract_xml(self.xml)
        else:
            self.status = False

    def prettify(self):
        parts = []
        for k, v in self.extracted.items():
            chart = "{} : \n{}"
            if type(v) == unicode:
                row = chart.format(k, v.encode('ascii', 'ignore'))
            elif type(v) == list:
                row = chart.format(k, '\n'.join(map(str, v)))
            else:
                row = chart.format(k, v)
            parts.append(row)
        return '\n\n'.join(parts)


def extract_xml(bs, tag="pod"):
    info = {"links": []}
    for element in bs.find_all(tag):
        if not element.plaintext.text and element.img:
            info["links"].append(
                ([element.attrs['title']], element.img.attrs['src']))
        else:
            info[element.attrs['title']] = element.plaintext.text
    for link in bs.find_all('link'):
        info["links"].append((link.attrs['text'], link.attrs['url']))
    return info


def api_query(appid, format, query):
    if ' ' in query:
        query = '%20'.join(query.split())
    return "http://api.wolframalpha.com/v2/query?appid={}&input={}&format={}".format(
        appid, query, ','.join(format))


def get_xml(query):
    req = requests.get(api_query(appid, ['image', 'plaintext'], query))
    if req.status_code == 200:
        return BeautifulSoup(req.text, "xml")

if __name__ == '__main__':
    w = WolframRequest("integrate e^sqrt(e^x)")

import json

from bs4 import BeautifulSoup


def parse_json(source, selector, hook):
    soup = BeautifulSoup(source, "html.parser")
    script = soup.select(selector)
    data = script[0].text[21:-1]

    return json.loads(data, object_hook=hook)

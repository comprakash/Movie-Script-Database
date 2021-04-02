from bs4 import BeautifulSoup
import urllib
import urllib.request
import requests
import string
import os
import textract
import re
from pdfminer import high_level
from pdfminer.layout import LAParams


def format_filename(s):
    valid_chars = "-() %s%s%s" % (string.ascii_letters, string.digits, "%")
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace('%20', ' ')
    filename = filename.replace('%27', '')
    filename = filename.replace(' ', '-')
    filename = re.sub(r'-+', '-', filename).strip()
    return filename


def get_soup(url):
    page = urllib.request.Request(url)
    result = urllib.request.urlopen(page)
    resulttext = result.read()

    soup = BeautifulSoup(resulttext, 'html.parser')
    return soup


def get_pdf_text(url):
    text = ""
    doc = os.path.join("scripts", "document.pdf")
    response = requests.get(url)

    if response.status_code == requests.codes.ok:
        with open(doc, 'wb') as f:
            f.write(response.content)
        try:
            text = high_level.extract_text(doc, laparams=LAParams(all_texts=True))
        except Exception as ex:
            print(url)
            print(ex)
    else:
        print("Not able to download PDF url {url}: {status}, {content}".format(url=url, status=response.status_code,
                                                                               content=response.content))

    if os.path.isfile(doc):
        os.remove(doc)
    return text


def get_doc_text(url):
    doc = os.path.join("scripts", "document.doc")
    result = urllib.request.urlopen(url)
    f = open(doc, 'wb')
    f.write(result.read())
    f.close()
    try:
        text = textract.process(doc, encoding='utf-8').decode('utf-8')
    except Exception as ex:
        print(url)
        print(ex)
        text = ""
    if os.path.isfile(doc):
        os.remove(doc)
    return text

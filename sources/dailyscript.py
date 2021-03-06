import urllib
import urllib.parse
import os
from tqdm import tqdm
from .utilities import format_filename, get_soup, get_pdf_text


def get_dailyscript():
    ALL_URL_1 = "https://www.dailyscript.com/movie.html"
    ALL_URL_2 = "https://www.dailyscript.com/movie_n-z.html"
    BASE_URL = "https://www.dailyscript.com/"
    DIR = os.path.join("scripts", "unprocessed", "dailyscript")

    if not os.path.exists(DIR):
        os.makedirs(DIR)

    soup_1 = get_soup(ALL_URL_1)
    soup_2 = get_soup(ALL_URL_2)

    movielist = soup_1.find_all('ul')[0].find_all('p')
    movielist_2 = soup_2.find_all('ul')[0].find_all('p')
    movielist += movielist_2

    # print(movielist)

    for movie in tqdm(movielist):
        try:
            script_url = movie.contents
            if len(script_url) < 2:
                continue
            script_url = movie.find('a').get('href')
            # print(script_url)

            text = ""
            name = movie.find('a').text

            if script_url.endswith('.pdf'):
                text = get_pdf_text(BASE_URL + urllib.parse.quote(script_url))
                # name = script_url.split("/")[-1].split('.pdf')[0]

            elif script_url.endswith('.html'):
                script_soup = get_soup(BASE_URL + urllib.parse.quote(script_url))
                doc = script_soup.pre
                if doc:
                    text = script_soup.pre.get_text()
                else:
                    text = script_soup.get_text()
                # name = script_url.split("/")[-1].split('.html')[0]

            elif script_url.endswith('.htm'):
                script_soup = get_soup(BASE_URL + urllib.parse.quote(script_url))
                text = script_soup.pre.get_text()
                # name = script_url.split("/")[-1].split('.htm')[0]

            elif script_url.endswith('.txt'):
                script_soup = get_soup(BASE_URL + urllib.parse.quote(script_url))
                text = script_soup.get_text()
                # name = script_url.split("/")[-1].split('.txt')[0]

            if text == "" or name == "":
                continue

            name = format_filename(name)

            with open(os.path.join(DIR, name + '.txt'), 'w', errors="ignore") as out:
                out.write(text)
        except Exception as ex:
            print(movie)
            print(ex)

import urllib
import urllib.parse
import os
from tqdm import tqdm
from .utilities import format_filename, get_soup


def get_screenplays():
    ALL_URL = "https://www.screenplays-online.de/"
    BASE_URL = "https://www.screenplays-online.de/"
    DIR = os.path.join("scripts", "unprocessed", "screenplays")

    if not os.path.exists(DIR):
        os.makedirs(DIR)
        
    soup = get_soup(ALL_URL)
    mlist = soup.find_all('table', class_="screenplay-listing")[0].find_all("a")
    movielist = [x for x in mlist if x.get('href').startswith("screenplay")]

    for movie in tqdm(movielist):
        try:
            name = format_filename(movie.text)
            script_url = movie.get('href')
            # if script_url.startswith("screenplay"):

            script_soup = get_soup(BASE_URL + urllib.parse.quote(script_url))
            # print(script_soup.pre.get_text())
            if not script_soup.pre:
                continue
            text = script_soup.pre.get_text()

            with open(os.path.join(DIR, name + '.txt'), 'w', errors="ignore") as out:
                out.write(text)
        except Exception as ex:
            print(movie)
            print(ex)

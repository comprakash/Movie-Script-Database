import os
from tqdm import tqdm
from .utilities import format_filename, get_soup, get_pdf_text


def get_scriptsavant():
    ALL_URL_1 = "https://thescriptsavant.com/free-movie-screenplays-am/"
    ALL_URL_2 = "https://thescriptsavant.com/free-movie-screenplays-nz/"
    BASE_URL = "https://thescriptsavant.com"
    DIR = os.path.join("scripts", "unprocessed", "scriptsavant")

    if not os.path.exists(DIR):
        os.makedirs(DIR)

    soup_1 = get_soup(ALL_URL_1)
    soup_2 = get_soup(ALL_URL_2)

    movielist = soup_1.find_all('tbody')[0].find_all('a')
    movielist_2 = soup_2.find_all('div', class_='fusion-text')[0].find_all('a')
    movielist += movielist_2

    for movie in tqdm(movielist):
        try:
            name = format_filename(movie.text.strip())
            print(name)
            script_url = movie.get('href')
            print(script_url)

            if not script_url.endswith('.pdf'):
                soup_1 = get_soup(BASE_URL + script_url)
                script_url = soup_1.find_all(attrs={'class': 'fusion-text'})[0].find_all('a')[0].get('href')

            try:
                text = get_pdf_text(script_url).replace('\x0C', '')

            except Exception as ex:
                print(movie)
                print(ex)
                continue

            if text == "" or name == "":
                continue

            with open(os.path.join(DIR, name + '.txt'), 'w', errors="ignore") as out:
                out.write(text)
        except Exception as ex:
            print(movie)
            print(ex)

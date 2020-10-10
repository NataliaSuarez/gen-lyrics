from bs4 import BeautifulSoup
import requests
import os
import sys

letras_url = "https://www.letras.com"

def descargar_cancion(path):
    url = f"{letras_url}{path}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    letra = ""

    for div in soup.findAll("div", {"class": "cnt-letra p402_premium"}):
        for p in div.findAll("p"):
            text = str(p)
            for space in ["</br>","<br>","<br/>","<p>","</p>"]:
                text = text.replace(space,"\n")
            letra += text

    with open(f"{path[1:-1]}.txt",'w') as f:
        f.write(letra)

def letras(artista):

    url = f"{letras_url}/{artista}/mais_tocadas.html"
    page = requests.get(url)

    if not os.path.exists(artista):
      os.mkdir(artista)

    soup = BeautifulSoup(page.content, 'html.parser')

    for a in soup.findAll("a", {"class": "song-name"}):
        descargar_cancion(a["href"])

artista = sys.argv[1]
letras(artista)

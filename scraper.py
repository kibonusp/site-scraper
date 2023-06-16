# https://pt.wikipedia.org/wiki/Lista_de_Pok%C3%A9mon
# https://www.pokemon.com/br/pokedex/piplup

from bs4 import BeautifulSoup
import requests

class Scraper:
    def __init__(self, search_url, name_selector, dex_selector, picture_selector, paragraph_selector):
        self.search_url = search_url
        self.name_selector = name_selector
        self.dex_selector = dex_selector
        self.picture_selector = picture_selector
        self.paragraph_selector = paragraph_selector
    
    def createBSObject(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')
    
    def safeGet(self, pageObj, selector):
        childObj = pageObj.select(selector)
        if childObj is not None and len(childObj) > 0:
            if (childObj[0].name == 'img'):
                return childObj[0].attrs["src"]
            return childObj[0].get_text()
        return ""
    
    def searchPokemon(self, pokemon_name):
        url = self.search_url + pokemon_name
        bs = self.createBSObject(url)
        return {
            "name": self.safeGet(bs, self.name_selector),
            "dex": self.safeGet(bs, self.dex_selector),
            "picture": self.safeGet(bs, self.picture_selector),
            "paragraph": self.paragraph_selector(bs, self.paragraph_selector)
        }
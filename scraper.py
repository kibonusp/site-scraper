from bs4 import BeautifulSoup
import requests

class Scraper:
    def __init__(self, search_url, dex_selector, picture_selector, paragraph_selector):
        self.search_url = search_url
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
            return childObj[0].get_text().strip()
        return ""
    
    def searchPokemon(self, pokemon_name):
        url = self.search_url + pokemon_name
        bs = self.createBSObject(url)
        return {
            "name": pokemon_name.capitalize(),
            "dex": self.safeGet(bs, self.dex_selector),
            "picture": self.safeGet(bs, self.picture_selector),
            "paragraph": self.safeGet(bs, self.paragraph_selector)
        }
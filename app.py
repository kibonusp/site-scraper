from flask import Flask, render_template
from scraper import Scraper
from db import PostgresAPI

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static',
            template_folder='templates')
db = PostgresAPI()
scraper = Scraper("https://www.pokemon.com/br/pokedex/", ".pokedex-pokemon-pagination-title div span", ".profile-images img", "p.version-x")

@app.route('/pokemon/<name>', methods=['GET'])
def getPokemonPage(name):
    name = name.capitalize()
    pokemon = db.get_pokemon_by_name(name)
    if (pokemon):
        return render_template('pokemon.html', pokemon=pokemon)
    else:
        scraped_pokemon = scraper.searchPokemon(name)
        db.insert_pokemon(scraped_pokemon)
        db.commit()
        return render_template('pokemon.html', pokemon=scraped_pokemon)
    
@app.route('/', methods=['GET'])
def mainpage():
    return render_template('index.html')

if __name__ == '__main__':
    try:      
        app.run(port=80)
                
    except Exception as e:
        print(e)
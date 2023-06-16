import psycopg2

def getkey_values(dictionary, keys):
    return (dictionary[key] for key in keys)

class PostgresAPI:
    def __init__(self):
        self.table = 'pokemon'
        self.con = psycopg2.connect(host='localhost', database='scrap_project', user='postgres')
        self.cur = self.con.cursor()
        self.attr_order = ['name', 'dex', 'picture', 'paragraph']
        self.create_table()
        
    def create_table(self):
        self.cur.execute("select * from information_schema.tables where table_name=%s", (self.table,))
        if (not bool(self.cur.rowcount)):
            self.cur.execute(f'create table {self.table} (name varchar(15), dex varchar(12) primary key, picture varchar(200) not null, paragraph varchar(1000) not null);')
        
    def commit_close(self):
        self.con.commit()
        self.con.close()
        
    '''
    @pokemon {
        name: STRING,
        picture: STRING,
        dex: STRING,
        paragraph: STRING
    }
    '''
    def insert_pokemon(self, pokemon):
        self.cur.execute(f'''insert into {self.table}(name, dex, picture, paragraph)
             values(%s);''', getkey_values(pokemon, self.attr_order))
        
    def get_pokemon_by_name(self, name):
        self.cur.execute(f"select * from {self.table} where name = {name}")
        return dict(zip(self.attr_order, self.cur.fetchone()))
        
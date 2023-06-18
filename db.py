import psycopg2

def getkey_values(dictionary, keys):
    return (dictionary[key] for key in keys)

class PostgresAPI:
    def __init__(self):
        self.table = 'pokemon'
        self.create_table()
        self.con = psycopg2.connect(host='localhost', database='scrap_project', user='postgres')
        self.cur = self.con.cursor()
        self.attr_order = ['name', 'dex', 'picture', 'paragraph']
        
    def create_table(self):
        self.con = psycopg2.connect(host='localhost', database='scrap_project', user='postgres')
        self.cur = self.con.cursor()
        self.cur.execute("select * from information_schema.tables where table_name=%s", (self.table,))
        if (not bool(self.cur.rowcount)):
            self.cur.execute(f'create table {self.table} (name varchar(30), dex varchar(12) primary key, picture varchar(200) not null, paragraph varchar(1000) not null);')
        self.con.commit()
        self.con.close()
        
    def commit(self):
        self.con.commit()
        
    '''
    @pokemon {
        name: STRING,
        picture: STRING,
        dex: STRING,
        paragraph: STRING
    }
    '''
    def insert_pokemon(self, pokemon):
        values = getkey_values(pokemon, self.attr_order)
        query_string = f"insert into {self.table}(name, dex, picture, paragraph) values("
        for value in values:
            query_string += f"'{value}',"
        query_string = query_string[:len(query_string)-1]
        query_string += ");"
        self.cur.execute(query_string)
        
    def get_pokemon_by_name(self, name):
        self.cur.execute(f"select * from {self.table} where name = \'{name}\'")
        pokemon = self.cur.fetchone()
        if (pokemon):
            return dict(zip(self.attr_order, pokemon))
        return None
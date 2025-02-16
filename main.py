import sqlite3


# con = sqlite3.connect("Avto.db")
# query = con.cursor()
# con.execute(''' CREATE TABLE avto (
#                      id INTEGER  PRIMARY KEY AUTOINCREMENT,
#                      name varchar(20),
#                      price integer,
#                      caller varchar(20),
#                      year integer)''')

# con.commit()
# con.close()


class DBcontextmanager:
    def __init__(self, db_name='../Avto.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)

    def __enter__(self):
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()
        if exc_type:
            return exc_val


class Avto1:
    def __init__(self, name, price, caller, year, id=None):
        self.name = name
        self.price = price
        self.caller = caller
        self.year = year
        self.id = id

    def __str__(self):
        return f"id : {self.id} , name : {self.name}"

    def save(self):
        try:
            with DBcontextmanager() as cur:
                id = cur.execute("INSERT INTO avto ('name','price','caller','year')"
                                 "VALUES (?,?,?,?) returning id",
                                 (self.name, self.price, self.caller, self.year)).fetchone()
                self.id = id[0]
                print(self.id)
        except sqlite3.Error as e:
            print(f"xato {e}")

    def update(self, **kwargs):
        with DBcontextmanager() as cur:
            for key, value in kwargs.items():
                print(type(key), type(value))
                print(key, value, self.id)
                sql_query = f"UPDATE avto SET {key} = ? WHERE id = ?"
                cur.execute(sql_query, (value, self.id))

    @classmethod
    def show_list(cls):
        avtolar = []
        with DBcontextmanager() as cure:
            a = cure.execute("SELECT * FROM Avto").fetchall()
            for i in a:
                a = Avto1(id=i[0], name=i[1], price=i[2], caller=i[3], year=i[4])
                avtolar.append(a)

            # for i in avtolar:
            #     for a in i:
            #         print(a)

        # db hamma avtolardi select
        # qilib iolib kelsaila va Avto classida object olasilar va ularni
        # avtolar listiga append qilib return
        return avtolar

    def delete(self):
        pass
    @staticmethod
    def filter(**kwargs):
        new_avtolar = []
        with DBcontextmanager() as cur:
            for key , value in kwargs.items():
                sql_query = f"SELECT * FROM avto WHERE {key} = ?"
                data = cur.execute(sql_query,(value,)).fetchall()
            for i in data :
                a = Avto1(id=i[0], name=i[1], price=i[2], caller=i[3], year=i[4])
                new_avtolar.append(a)
        # db hamma avtolardi select
        # qilib iolib kelsaila va Avto classida object olasilar va ularni
        # avtolar listiga append qilib return
        return new_avtolar


avto = Avto1('Gentra', 5000, 'Qora', 2020, )
# avto.save()
# avto.show_list()
avto1 = Avto1.show_list()
avto1[3].update(name='BMW')
# avto.update(caller='dghfjgf')
avtolar = avto.filter(name = 'Gentra')

for i in avtolar:
    i.update(name="Nexia2")
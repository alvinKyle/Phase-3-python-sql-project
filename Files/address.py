from Files.myDatabase import conn , cursor

class Address:

    all = {}

    def __init__(self,country,city,user_id = None,org_id = None,id = None):
        self.id = id
        self.country = country
        self.city = city
        self.user_id = user_id
        self.org_id = org_id

    def __repr__(self):
        return f"<Address {self.id}: {self.country}, {self.city}, {self.user_id}, {self.org_id}>"
    

    @property
    def country(self):
        return self._country
    
    @country.setter
    def country(self,country):
        if isinstance(country,str) and len(country):
            self._country = country
        else:raise ValueError("Country must be a string")

    @property
    def city(self):
        return self._city
    
    @city.setter
    def city(self,city):
        if isinstance(city,str) and len(city):
            self._city = city
        else:
            raise ValueError("City must be a string")
        
    @classmethod
    def create_table(cls):
        try:
            sql = """
                CREATE TABLE IF NOT EXISTS addresses (
                id INTEGER PRIMARY KEY,
                country TEXT,
                city TEXT,
                user_id INTEGER,
                org_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (org_id) REFERENCES organizations(id)
                )
            """
            cursor.execute(sql)
            conn.commit()
            print("Address table created successfully.")

        except Exception as e:
            print(f"An error occurred while creating the Address table: {e}")

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS addresses
            """
        cursor.execute(sql)
        conn.commit()

    def save(self):
        sql = """
            INSERT INTO addresses (country,city,user_id,org_id)
            VALUES(?,?,?,?)
            """
        cursor.execute(sql,(self.country,self.city,self.user_id,self.org_id))
        conn.commit()

        self.id = cursor.lastrowid
        type(self).all[self.id] = self
        
    @classmethod
    def create(cls,country,city,user_id = None,org_id = None):
        address = cls(country,city,user_id,org_id)
        address.save()
        return address
    
    def update(self):
        sql = """
            UPDATE addresses
            SET country =?, city =?, user_id =?, org_id =?
            WHERE id =?
        """
        cursor.execute(sql,(self.country,self.city,self.user_id,self.org_id,self.id))
        conn.commit()

    def delete(self):
        sql = """
            DELETE FROM addresses
            WHERE id =?
        """
        cursor.execute(sql,(self.id,))
        conn.commit()

        del type(self).all[self.id]
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        address = cls.all.get(row[0])
        if address:
            address.country = row[1]
            address.city = row[2]
            address.user_id = row[3]
            address.org_id = row[4]
        else:
            address = cls(row[1], row[2], row[3], row[4])
            address.id = row[0]
            cls.all[address.id] = address
        return address
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM addresses
        """
        rows = cursor.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls,id):
        sql = """
            SELECT * FROM addresses
            WHERE id =?
        """
        row = cursor.execute(sql,(id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_city(cls,city):
        sql  = """
            SELECT * FROM addresses
            WHERE city =?
        """
        rows = cursor.execute(sql,(city,)).fetchone()
        return [cls.instance_from_db(row) for row in rows] if rows else []
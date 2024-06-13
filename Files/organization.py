from Files.myDatabase import conn ,cursor

class Organization:

    all = {}

    def __init__(self,name,id = None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Organization {self.id}:{self.name}>"
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,name):
        if isinstance(name,str) and len(name):
            self._name = name
        else:raise ValueError("Name must be a non-empty string")

    @classmethod
    def create_table(cls):
        try:
            sql ="""
                CREATE TABLE IF NOT EXISTS organizations(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
                )
            """
            cursor.execute(sql)
            conn.commit()
            print("Organization table created successfully.")

        except Exception as e:
            print(f"An error occurred while creating the Organization table: {e}")


    @classmethod
    def drop_table(cls):
        try:
            sql ="""
                DROP TABLE IF EXISTS organizations
            """ 
            cursor.execute(sql)
            conn.commit()

        except Exception as e:
            print(f"An error occurred while dropping the table: {e}")

    def save(self):
        try:
            sql = """
                INSERT INTO organizations (name)
                VALUES(?)
            """
            cursor.execute(sql,(self.name,))
            conn.commit()
            self.id = cursor.lastrowid
            type(self).all[self.id] = self

        except Exception as e:
            print(f"An error occurred while saving the organization: {e}")

    @classmethod
    def create (cls,name):
        organization = cls(name)
        organization.save()
        return organization

    def update(self):
        sql = """
                UPDATE organizations
                SET name = ?
                WHERE id = ?
            """
        cursor.execute(sql,(self.name,self.id))
        conn.commit()

    def delete(self):
        try:
            sql = """
                    DELETE FROM organizations
                    WHERE id = ?
                    """
            cursor.execute(sql,(self.id,))
            conn.commit()
            del type(self).all[self.id]
            self.id = None

        except Exception as e:
            print(f"An error occurred while deleting the organization: {e}")

    @classmethod
    def instance_from_db(cls,row):
        organization = cls.all.get(row[0])
        if organization :
            organization.name = row[1]
        else:
            organization = cls(row[1])
            organization.id = row[0]
            cls.all[organization.id] = organization
        return organization
    
    @classmethod
    def get_all(cls):
        try:
            sql = """
                SELECT * FROM organizations
            """
            rows = cursor.execute(sql).fetchall()
            return [cls.instance_from_db(row) for row in rows]
        
        except Exception as e:
            print(f"An error occurred while retrieving all organizations: {e}")
            return []

    
    @classmethod
    def find_by_id(cls,id):
        try:
            sql = """
                SELECT * FROM organizations 
                WHERE id = ?
                """
            row = cursor.execute(sql,(id,)).fetchone()
            return cls.instance_from_db(row) if row else None
        
        except Exception as e:
            print(f"An error occurred while finding the organization by ID: {e}")
            return None

    
    @classmethod
    def find_by_name(cls,name):
        try:
            sql = """
                SELECT * FROM organizations
                WHERE name = ?
                """
            row = cursor.execute(sql,(name,)).fetchone()
            return cls.instance_from_db(row) if row else None
        
        except Exception as e:
            print(f"An error occurred while finding the organization by name: {e}")
            return None
from Files.myDatabase import conn, cursor


class User:
     
    all = {}

    def __init__(self, username, phone_no, email, org_id=None, id=None):
        self.id = id
        self.username = username  
        self.phone_no = phone_no  
        self.email = email  
        self.org_id = org_id

    def __repr__(self):
        return f"<User {self.id}: {self.username}, {self.phone_no}, {self.email}, {self.org_id}>"

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        if isinstance(username, str) and len(username):
            self._username = username
        else:
            raise ValueError("Username must be a non-empty string")

    @property
    def phone_no(self):
        return self._phone_no

    @phone_no.setter
    def phone_no(self, phone_no):
        if isinstance(phone_no, int):
            self._phone_no = phone_no
        else:
            raise ValueError("Phone number must be an integer")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if isinstance(email, str) and "@" in email:
            self._email = email
        else:
            raise ValueError("Email must be a valid non-empty string")

    @classmethod
    def create_table(cls):
        try:
            sql = """
                CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                phone_no INTEGER NOT NULL,
                email TEXT NOT NULL,
                org_id INTEGER,
                FOREIGN KEY (org_id) REFERENCES organizations(id)
                )
            """
            cursor.execute(sql)
            conn.commit()
            print("User table created successfully.")

        except Exception as e:
            print(f"An error occurred while creating the User table: {e}")
    @classmethod
    def drop_table(cls):
        try:
            sql = """
                DROP TABLE IF EXISTS users 
                
                """
            cursor.execute(sql)
            conn.commit()

        except Exception as e:
            print(f"An error occurred while dropping the table: {e}")

    def save(self):
        try:
            sql = """
                INSERT INTO users (username, phone_no, email, org_id)
                VALUES(?,?,?,?)
                
                """
            cursor.execute(sql, (self.username, self.phone_no, self.email, self.org_id))
            conn.commit()

            self.id = cursor.lastrowid
            type(self).all[self.id] = self

        except Exception as e:
            print(f"An error occurred while saving the user: {e}")


    @classmethod
    def create (cls,username, phone_no, email, org_id=None):
        user = cls(username, phone_no, email, org_id)
        user.save()
        return user
    
    
    def update(self):
        try:
            sql = """
                UPDATE users
                SET username = ?, phone_no = ?, email = ?, org_id = ?
                WHERE id = ?
                """
            cursor.execute(sql, (self.username, self.phone_no, self.email, self.org_id, self.id))
            conn.commit()

        except Exception as e:
            print(f"An error occurred while updating the user: {e}")

    def delete (self):
        try:
            sql = """
                    DELETE FROM users
                    WHERE id = ?
                """
            cursor.execute(sql ,(self.id,))
            conn.commit()

            del type(self).all[self.id]
            self.id = None

        except Exception as e:
            print(f"An error occurred while deleting the user: {e}")

    @classmethod
    def instance_from_db(cls,row):
        user = cls.all.get (row[0])
        if user :
            user.username = row[1]
            user.phone_no = row[2]
            user.email = row[3]
            user.org_id = row[4]
        else:
            user = cls(row[1], row[2], row[3], row[4])
            user.id = row[0]
            cls.all[user.id] = user
        return user
        
    @classmethod
    
    def get_all(cls):
        sql = """
            SELECT * FROM users
            """
        rows = cursor.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls,id):
        sql = """
            SELECT * FROM users 
            WHERE id = ?
            """
        row = cursor.execute(sql,(id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_username(cls,username):
        sql = """
            SELECT * FROM users
            WHERE username = ?
            """
        row = cursor.execute(sql,(username,)).fetchone()
        return cls.instance_from_db(row) if row else None

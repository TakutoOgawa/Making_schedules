import sqlite3

DB = "database.db"

con = sqlite3.connect(DB)



con.execute("""
            UPDATE students
            SET chemistry = 0
            """
            )

con.commit()
con.close()
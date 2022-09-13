import sqlite3

DB = "database.db"

con = sqlite3.connect(DB)



con.execute("""
            DELETE FROM students
            """
            )

con.commit()
con.close()
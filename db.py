import sqlite3
from date import make_day_id

DB = 'database.db'

def create_table():
    con = sqlite3.connect(DB)
    con.execute("""
                CREATE TABLE IF NOT EXISTS students(
                    id INTEGER PRIMARY KEY, 
                    name STRING UNIQUE, 
                    belonging STRING, 
                    chemistry INT
                    )
                """
                )
    con.execute("""
                CREATE TABLE IF NOT EXISTS teachers(
                    id INTEGER PRIMARY KEY, 
                    name STRING UNIQUE, 
                    subject INT
                    )
                """
                )
    con.execute("""
                CREATE TABLE IF NOT EXISTS all_date(
                    day STRING, 
                    info INT
                    )
                """
                )
    
    flag = con.execute("""
                    SELECT 1 FROM all_date
                    """
                    ).fetchone()
    
    if flag is None:
        for year in range(2020, 2051):
            diff = [1, -2, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]
            if year % 4 == 0:
                diff[1] += 1
            for month in range(1, 13):
                days = 30 + diff[month - 1]
                for day in range(1, days + 1):
                    for class_num in range(4):
                        day_id = make_day_id(year, month, day, class_num)
                        con.execute("""
                                    INSERT INTO all_date(day, info)
                                    SELECT {}, 0
                                    WHERE NOT EXISTS (SELECT 1 FROM all_date WHERE day = {})
                                    """.format(day_id, day_id)
                                    )

    con.commit()
    con.close()
    return

def preserve_date(name, job, date_list, day, class_num, subject_num):
    con = sqlite3.connect(DB)
    year, month = date_list[0], date_list[1]
    day_id = make_day_id(year, month, day, class_num)
    student_id = con.execute("""
                            SELECT id FROM {}
                            WHERE name = "{}"
                            """.format(job + "s", name)
                            ).fetchone()[0]

    info = con.execute("""
                        SELECT info FROM all_date
                        WHERE day = {}
                        """.format(day_id)
                        ).fetchone()[0]

    his_info = info // 10 ** (student_id - 1)
    his_info %= 10
    info += (subject_num - his_info) * 10 ** (student_id - 1)

    con.execute("""
                UPDATE all_date
                SET info = {}
                WHERE day = {}
                """.format(info, day_id)
                )
    con.commit()
    con.close()
    return

def get_subject(name, job, date_list, day, class_num):
    year, month = date_list[0], date_list[1]
    day_id = make_day_id(year, month, day, class_num)
    day_info = get_day_info(day_id)
    student_id = get_ones_info(name, job)[1]

    his_info = day_info // 10 ** (student_id - 1)
    his_info %= 10
    
    return his_info

def get_persons(job):
    flag = 1 if job == "teacher" else 0
    con = sqlite3.connect(DB)
    persons = con.execute("""
                            SELECT * FROM {}
                            """.format(job + "s", flag)
                            ).fetchall()
    con.close() 
    return persons

# Unfinished. 
def delete_from_db(name, job):
    con = sqlite3.connect(DB)

    person_id = con.execute("""
                            SELECT id FROM {}
                            WHERE name = "{}"
                            """.format(job + "s", name)
                            ).fetchone()[0]

    con.execute("""
                DELETE FROM {}
                WHERE name = "{}"
                """.format(job + "s", name)
                )
    
    return

def register_person(name, job):
    con = sqlite3.connect(DB)

    id = con.execute("""
                    SELECT MIN(id + 1)
                    FROM (
                        SELECT students.id FROM students
                        UNION
                        SELECT teachers.id FROM teachers
                        )
                    WHERE id + 1 NOT IN (
                                        SELECT students.id FROM students
                                        UNION
                                        SELECT teachers.id FROM teachers
                                        )
                    """
                    ).fetchone()[0]
    if id is None:
        id = 1

    con.execute("""
                INSERT INTO {}s (id, name)
                SELECT {}, "{}"
                WHERE NOT EXISTS (SELECT 1 FROM {}s WHERE name = "{}")
                """.format(job, id, name, job, name)
                )

    con.commit()
    con.close()
    return

def update(name, job, subject):
    con = sqlite3.connect(DB)

    con.execute("""
                UPDATE {}s
                SET subject = {}
                WHERE name = "{}"
                """.format(job, subject, name)
                )
    
    con.commit()
    con.close()
    return

def get_day_info(day_id):
    con = sqlite3.connect(DB)
    day_info = con.execute("""
                            SELECT info FROM all_date
                            WHERE day = {}
                            """.format(day_id)
                            ).fetchone()[1]
    con.close()
    return day_info

def get_ones_info(name, job):
    con = sqlite3.connect(DB)
    ones_info = con.execute("""
                            SELECT * FROM {}s
                            WHERE name = "{}"
                            """.format(job, name)
                            ).fetchone()
    con.close()
    return ones_info

def search_name(id):
    con = sqlite3.connect(DB)
    name1 = con.execute("""
                        SELECT name
                        FROM students
                        """.format(id)
                        ).fetchone()[0]
    name2 = con.execute("""
                        SELECT name
                        FROM students
                        """.format(id)
                        ).fetchone()[0]
    con.close()
    if name1 is not None:
        return name1, "student"
    else:
        return name2, "teacher"
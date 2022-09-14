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
                    chemistry INT DEFAULT 0
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
                        con.execute(f"""
                                    INSERT INTO all_date(day, info)
                                    SELECT {day_id}, 0
                                    WHERE NOT EXISTS (SELECT 1 FROM all_date WHERE day = {day_id})
                                    """
                                    )

    con.commit()
    con.close()
    return

def preserve_date(name, job, date_list, day, class_num, subject_num):
    con = sqlite3.connect(DB)
    year, month = date_list[0], date_list[1]
    day_id = make_day_id(year, month, day, class_num)
    student_id = con.execute(f"""
                            SELECT id FROM {job}s
                            WHERE name = "{name}"
                            """
                            ).fetchone()[0]

    info = con.execute(f"""
                        SELECT info FROM all_date
                        WHERE day = {day_id}
                        """
                        ).fetchone()[0]

    his_info = info // 10 ** (student_id - 1)
    his_info %= 10
    info += (subject_num - his_info) * 10 ** (student_id - 1)

    con.execute(f"""
                UPDATE all_date
                SET info = {info}
                WHERE day = {day_id}
                """
                )
    con.commit()
    con.close()
    return

def get_subject(name, job, date_list, day, class_num):
    year, month = date_list[0], date_list[1]
    day_id = make_day_id(year, month, day, class_num)
    day_info = get_day_info(day_id)
    student_id = get_ones_info(name, job)[0]

    his_info = day_info // 10 ** (student_id - 1)
    his_info %= 10
    
    return his_info

def get_persons(job):
    flag = 1 if job == "teacher" else 0
    con = sqlite3.connect(DB)
    persons = con.execute(f"""
                            SELECT * FROM {job}s
                            """
                            ).fetchall()
    con.close() 
    return persons

# Unfinished. 
def delete_from_db(name, job):
    con = sqlite3.connect(DB)

    person_id = con.execute(f"""
                            SELECT id FROM {job}s
                            WHERE name = "{name}"
                            """
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

    con.execute(f"""
                INSERT INTO {job}s (id, name)
                SELECT {id}, "{name}"
                WHERE NOT EXISTS (SELECT 1 FROM {job}s WHERE name = "{name}")
                """
                )

    con.commit()
    con.close()
    return

def update(name, job, subject):
    con = sqlite3.connect(DB)

    con.execute(f"""
                UPDATE {job}s
                SET subject = {subject}
                WHERE name = "{name}"
                """
                )
    
    con.commit()
    con.close()
    return

def get_day_info(day_id):
    con = sqlite3.connect(DB)
    day_info = con.execute(f"""
                            SELECT info FROM all_date
                            WHERE day = {day_id}
                            """
                            ).fetchone()[0]
    con.close()
    return day_info

def get_ones_info(name, job):
    con = sqlite3.connect(DB)
    ones_info = con.execute(f"""
                            SELECT * FROM {job}s
                            WHERE name = "{name}"
                            """
                            ).fetchone()
    con.close()
    return ones_info

def search_name(id):
    con = sqlite3.connect(DB)
    name1 = con.execute(f"""
                        SELECT name
                        FROM students
                        WHERE id = {id}
                        """
                        ).fetchone()
    name2 = con.execute(f"""
                        SELECT name
                        FROM teachers
                        WHERE id = {id}
                        """
                        ).fetchone()
    con.close()
    if name1 is not None:
        return name1[0], "student"
    else:
        return name2[0], "teacher"

def get_persons_info(id_or_name):
    if type(id_or_name) is int:
        type_name = "id"
    else:
        type_name = "name"
    
    con = sqlite3.connect(DB)
    info = con.execute(f"""
                        SELECT {type_name}
                        FROM students UNION teachers
                        WHERE {type_name} == {id_or_name}
                        """)
    con.close()
    return info
import sqlite3
import heapq
from db import get_day_info, get_ones_info, search_name
from date import make_day_id

DB = 'database.db'

def making_schedule(year, month, day, class_num):
    day_id = make_day_id(year, month, day, class_num)
    info = get_day_info(day_id)
    teacher_ids = []
    student_ids = []
    N = len(str(info))

    for id in range(1, N + 1):
        subject = info % 10
        if subject == 0:
            continue
        name, job = search_name(id)
        if job == "teacher":
            teacher_ids.append(id)
        else:
            student_ids.append(id)
        
        info //= 10
    
    que = []
    heapq.heapify(que)
    g = [[] for _ in range(N + 1)]
    for u in teacher_ids:
        for v in student_ids:
            g[u].append(v)
            g[v].append(u)
            c = chemistry(u, v, subject)
            heapq.heappush((-c, u, v))


    return


def chemistry(teacher, student, subject):
    return
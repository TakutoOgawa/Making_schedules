import sqlite3
import heapq
from db import get_day_info, search_name
from date import make_day_id

DB = 'database.db'

def make_schedule(year, month, day, class_num):
    day_id = make_day_id(year, month, day, class_num)
    info = get_day_info(day_id)
    S = []
    T = []
    S_name = []
    T_name = []
    Subject = []
    N = len(str(info))

    for id in range(1, N + 1):
        subject = info % 10
        if subject == 0:
            info //= 10
            continue
        name, job = search_name(id)
        if job == "student":
            S.append(id)
            S_name.append(name)
            Subject.append(subject)
        else:
            T.append(id)
            T_name.append(name)

        info //= 10
    
    ls, lt = len(S), len(T)
    inv_S = {}
    inv_T = {}
    for i, s in enumerate(S):
        inv_S[s] = i
    for i, t in enumerate(T):
        inv_T[t] = i

    que = []
    heapq.heapify(que)
    for s in range(ls):
        for t in range(lt):
            c = chemistry(S[s], T[t], Subject[s])
            heapq.heappush(que, (-c, s, t))
    
    cnt_S = [0] * ls
    cnt_T = [0] * lt
    sm = 0

    A = ["----", "English", "Math", "Japanese", "Science", "Society"]

    g = {}

    while que:
        c, s, t = heapq.heappop(que)
        c *= -1
        if cnt_S[s] == 1 or cnt_T[t] == 4:
            continue
        sm += c
        cnt_S[s] += 1
        cnt_T[t] += 1
        if T_name[t] not in g:
            g[T_name[t]] = []
        g[T_name[t]].append((S_name[s], A[Subject[s]]))

    return g


def make_schedule_table(year, month, day):
    g = [make_schedule(year, month, day, class_num) for class_num in range(4)]
    A = {}

    for i in range(4):
        for t_name in g[i]:
            if t_name not in A:
                A[t_name] = [[("----", "----")] * 4 for _ in range(4)]
            for j, (student, subject) in enumerate(g[i][t_name]):
                A[t_name][i][j] = (student, subject)

    return A



def chemistry(student, teacher, subject):
    con = sqlite3.connect(DB)
    x = con.execute(f"""
                    SELECT subject
                    FROM teachers
                    WHERE id == {teacher}
                    """
                    ).fetchone()[0]
    x //= 10 ** subject
    x %= 10
    y = con.execute(f"""
                    SELECT chemistry
                    FROM students
                    WHERE id == {student}
                    """
                    ).fetchone()[0]
    con.close()
    y //= 10 ** (teacher - 1)
    y %= 10

    return x + y
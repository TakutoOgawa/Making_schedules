from flask import Flask, render_template, request, redirect, url_for
from db import create_table, preserve_date, get_subject, delete_from_db, get_persons, register_person, update, get_ones_info
from date import today_date, weekday_of_the_first_day
from main import make_schedule_table

app = Flask(__name__)
DB = 'database.db'


@app.route('/')
def index():
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    return render_template(
        'index.html'
    )


@app.route('/students/')
def students():
    """students
    Keyword arguments:
    argument -- description
    Return: return_description
    """

    job = "student"
    persons = get_persons(job)
    today = today_date()
    return render_template(
        'students.html',
        job=job,
        persons=persons,
        year=today[0],
        month=today[1]
    )


@app.route('/teachers/')
def teachers():
    job = "teacher"
    persons = get_persons(job)
    today = today_date()
    return render_template(
        'teachers.html',
        job=job,
        persons=persons,
        year=today[0],
        month=today[1]
    )


@app.route('/register', methods=['POST'])
def register():
    job = request.form["job"]
    name = request.form['name']
    register_person(name, job)
    return redirect(url_for(job + "s"))


@app.route('/form/students/<name>/', methods=["GET", "POST"])
def student_form(name):
    job = "student"
    today = today_date()
    if request.form.get("year") is None:
        year, month = today[0], today[1]
    else:
        year = int(request.form["year"])
        month = int(request.form["month"])

    weekday, days = weekday_of_the_first_day(year, month)
    date_list = [year, month, weekday, days]

    subject = ["----", "English", "Math", "Japanese", "Science", "Society"]
    weekdays = ["Mon.", "Tue.", "Wed.", "Thu.", "Fri.", "Sat.", "Sun."]

    ones_subject = [[0] * 4 for _ in range(days)]
    if request.form.get("ones_subject") is not None:
        for i in range(1, days + 1):
            for j in range(4):
                ones_subject[i -
                             1][j] = int(request.form['subject_' + str(i) + '_' + str(j)])
                preserve_date(name, job, date_list, i,
                              j, ones_subject[i - 1][j])
    else:
        for i in range(1, days + 1):
            for j in range(4):
                ones_subject[i -
                             1][j] = get_subject(name, job, date_list, i, j)

    return render_template(
        'student_form.html',
        name=name,
        job=job,
        date_list=date_list,
        subject=subject,
        weekdays=weekdays,
        ones_subject=ones_subject
    )


@app.route('/form/teachers/<name>/', methods=["GET", "POST"])
def teacher_form(name):
    job = "teacher"
    today = today_date()
    if request.form.get("year") is None:
        year, month = today[0], today[1]
    else:
        year = int(request.form["year"])
        month = int(request.form["month"])

    weekday, days = weekday_of_the_first_day(year, month)
    date_list = [year, month, weekday, days]

    subject = ["----", "Attending"]
    weekdays = ["Mon.", "Tue.", "Wed.", "Thu.", "Fri.", "Sat.", "Sun."]

    ones_subject = [[0] * 4 for _ in range(days)]
    if request.form.get("ones_subject") is not None:
        for i in range(1, days + 1):
            for j in range(4):
                ones_subject[i -
                             1][j] = int(request.form['subject_' + str(i) + '_' + str(j)])
                preserve_date(name, job, date_list, i,
                              j, ones_subject[i - 1][j])
    else:
        for i in range(1, days + 1):
            for j in range(4):
                ones_subject[i -
                             1][j] = get_subject(name, job, date_list, i, j)

    return render_template(
        'teacher_form.html',
        name=name,
        job=job,
        date_list=date_list,
        subject=subject,
        weekdays=weekdays,
        ones_subject=ones_subject
    )


@app.route('/delete', methods=["POST"])
def delete():
    name = request.form['name']
    delete_from_db(name)
    return redirect("sections")


@app.route("/teachers/<name>/info", methods=["GET", "POST"])
def teacher_info(name):
    info = get_ones_info(name, "teacher")[2]
    ability = [0] * 5
    if info is not None:
        for i in range(5):
            x = info % 10
            ability[i] = x
            info //= 10

    subject = ["----", "English", "Math", "Japanese", "Science", "Society"]
    return render_template(
        "teacher_info.html",
        name=name,
        subject=subject,
        ability=ability
    )


@app.route("/update_info/<name>", methods=["POST"])
def update_info(name):
    job = "teacher"
    sm = 0
    for i in range(1, 6):
        x = int(request.form[str(i)])
        sm += x * 10 ** (i - 1)

    update(name=name, job=job, subject=sm)
    return redirect(url_for("teacher_info", name=name))


@app.route('/management', methods=["GET", "POST"])
def management():
    if request.form.get("year") is None:
        today = today_date()
        year, month, day = today[0], today[1], today[2]
    else:
        year = int(request.form["year"])
        month = int(request.form["month"])
        day = int(request.form["day"])
    days = weekday_of_the_first_day(year, month)[1]
    date_list = [year, month, day, days]
    g = make_schedule_table(year, month, day)
    return render_template(
        "scheduling.html",
        date_list=date_list,
        g=g
    )


if __name__ == '__main__':
    create_table()
    app.run(debug=False, host='0.0.0.0', port="5050")

# app.run(debug=True, host='localhost', port=5000)

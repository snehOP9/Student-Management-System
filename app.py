from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "secret"

users = {
    "admin1": {"password": "adminpass", "role": "admin"},
    "teacher1": {"password": "teach1", "role": "teacher"},
    "teacher2": {"password": "teach2", "role": "teacher"},
    "Sneh": {"password": "sneh123", "role": "student"},
    "Vansh": {"password": "vansh123", "role": "student"},
    "Deepika": {"password": "deepika123", "role": "student"},
    "Nidhi": {"password": "nidhi123", "role": "student"},
    "Devesh": {"password": "devesh123", "role": "student"},
    "Abhishek": {"password": "abhishek123", "role": "student"},
    "Aishwarya": {"password": "aish123", "role": "student"}
}

students = [
    {"id": 1, "name": "Sneh", "roll": "101", "branch": "CSE", "email": "sneh@xyz.com", "attendance": 85, "fees_paid": True, "subjects": {"Math": 78, "Physics": 80, "Chemistry": 82}},
    {"id": 2, "name": "Vansh", "roll": "102", "branch": "ECE", "email": "vansh@xyz.com", "attendance": 90, "fees_paid": False, "subjects": {"Math": 88, "Physics": 67, "Chemistry": 70}},
    {"id": 3, "name": "Deepika", "roll": "103", "branch": "CSE", "email": "deepika@xyz.com", "attendance": 92, "fees_paid": True, "subjects": {"Math": 92, "Physics": 90, "Chemistry": 91}},
    {"id": 4, "name": "Nidhi", "roll": "104", "branch": "ME", "email": "nidhi@xyz.com", "attendance": 78, "fees_paid": False, "subjects": {"Math": 65, "Physics": 72, "Chemistry": 60}},
    {"id": 5, "name": "Devesh", "roll": "105", "branch": "CSE", "email": "devesh@xyz.com", "attendance": 88, "fees_paid": True, "subjects": {"Math": 93, "Physics": 85, "Chemistry": 89}},
    {"id": 6, "name": "Abhishek", "roll": "106", "branch": "IT", "email": "abhishek@xyz.com", "attendance": 80, "fees_paid": True, "subjects": {"Math": 70, "Physics": 75, "Chemistry": 68}},
    {"id": 7, "name": "Aishwarya", "roll": "107", "branch": "EE", "email": "aishwarya@xyz.com", "attendance": 84, "fees_paid": False, "subjects": {"Math": 64, "Physics": 77, "Chemistry": 69}}
]

@app.route("/")
def index():
    return render_template("role_select.html")

@app.route("/login", methods=["POST"])
def login():
    role = request.form.get("role")
    username = request.form.get("username")
    password = request.form.get("password")
    if username in users and users[username]["password"] == password and users[username]["role"] == role:
        session["user"] = username
        session["role"] = role
        if role == "admin":
            return redirect(url_for("admin_dashboard"))
        elif role == "teacher":
            return redirect(url_for("teacher_dashboard"))
        else:
            return redirect(url_for("student_dashboard"))
    flash("Invalid credentials", "danger")
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/admin_dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("index"))
    return render_template("admin_dashboard.html", students=students)

@app.route("/teacher_dashboard")
def teacher_dashboard():
    if session.get("role") != "teacher":
        return redirect(url_for("index"))
    return render_template("teacher_dashboard.html", students=students)

@app.route("/student_dashboard")
def student_dashboard():
    if session.get("role") != "student":
        return redirect(url_for("index"))
    user = session.get("user")
    d = next((s for s in students if s["name"].lower() == user.lower()), None)
    return render_template("student_dashboard.html", student=d)

@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if session.get("role") != "admin":
        return redirect(url_for("index"))
    if request.method == "POST":
        n = request.form.get("name")
        r = request.form.get("roll_number")
        b = request.form.get("branch")
        e = request.form.get("email")
        m = request.form.get("marks")
        i = max(s["id"] for s in students) + 1 if students else 1
        students.append({"id": i, "name": n, "roll": r, "branch": b, "email": e, "attendance": 0, "fees_paid": False, "subjects": {"Math": int(m), "Physics": 0, "Chemistry": 0}})
        return redirect(url_for("admin_dashboard"))
    return render_template("add_student.html")

@app.route("/delete_student/<int:sid>", methods=["POST"])
def delete_student(sid):
    if session.get("role") != "admin":
        return redirect(url_for("index"))
    global students
    students = [s for s in students if s["id"] != sid]
    return redirect(url_for("admin_dashboard"))

@app.route("/update_student/<int:id>", methods=["GET","POST"])
def update_student(id):
    if session.get("role") != "admin":
        return redirect(url_for("index"))
    st = next((s for s in students if s["id"] == id), None)
    if not st:
        return redirect(url_for("admin_dashboard"))
    if request.method == "POST":
        st["name"] = request.form.get("name")
        st["roll"] = request.form.get("roll_number")
        st["branch"] = request.form.get("branch")
        st["email"] = request.form.get("email")
        st["subjects"]["Math"] = int(request.form.get("marks"))
        return redirect(url_for("admin_dashboard"))
    return render_template("update_student.html", student=st)

@app.route("/update_record/<int:sid>", methods=["GET","POST"])
def update_record(sid):
    if session.get("role") not in ["admin","teacher"]:
        return redirect(url_for("index"))
    st = next((s for s in students if s["id"] == sid), None)
    if not st:
        return redirect(url_for("teacher_dashboard"))
    if request.method == "POST":
        st["subjects"]["Math"] = int(request.form.get("math"))
        st["subjects"]["Physics"] = int(request.form.get("physics"))
        st["subjects"]["Chemistry"] = int(request.form.get("chem"))
        st["attendance"] = int(request.form.get("attendance"))
        st["fees_paid"] = request.form.get("fees_paid") == "on"
        return redirect(url_for("teacher_dashboard") if session["role"]=="teacher" else url_for("admin_dashboard"))
    return render_template("update_record.html", student=st)

if __name__ == "__main__":
    app.run(debug=True)

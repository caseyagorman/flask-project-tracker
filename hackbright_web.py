"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect, flash

import hackbright

app = Flask(__name__)
app.secret_key = b'shhhhhhhhh'


@app.route("/student")
def get_student():
	"""Show information about a student."""

	github = request.args.get("github")

	first, last, github = hackbright.get_student_by_github(github)
	grades = hackbright.get_grades_by_github(github)

	
	html = render_template("student_info.html",
							first=first,
							last=last,
							github=github,
							grades= grades)
	return html

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/add-student")
def get_new_student():

	return render_template("add_student.html")

@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""
    first = request.form.get("first")
    last = request.form.get("last")
    github = request.form.get("github")
    hackbright.make_new_student(first, last, github)
    flash(github + ' has been added')
    return redirect("/")	

@app.route("/student-delete")
def get_student_to_delete():
	"""display form to delete student"""
	return render_template("student_delete.html")


@app.route("/delete-student", methods=['POST'])
def student_delete():
	 """Check if student in database, delete a student."""
	 github = request.form.get("github")
	 student = hackbright.get_student_by_github(github)
	 if student:
	 	hackbright.delete_student_by_github(github)
	 	hackbright.delete_grades_by_github(github)
	 	flash(github + ' has been deleted')
	 	return redirect("/")
	 else: 
 	 	flash('There is no student with that name in our records')
 	 	return redirect("/student-delete")							


@app.route("/project")
def get_project():
	"""get projects from database"""
	title = request.args.get("title")
	projects = hackbright.get_project_by_title(title)
	grades = hackbright.get_grades_by_title(title)
	return render_template("projects.html",
							projects=projects,
							grades=grades)

@app.route("/")
def list_students_and_projects():
	"""get and list all students and projects from database"""
	students = hackbright.get_all_students()
	projects = hackbright.get_all_projects()
	return render_template("homepage.html",
							students=students,
							projects=projects)

@app.route("/assign-grade")
def get_grades():
	"""get form to assign grades"""
	return render_template("assign_grades.html")

@app.route("/assign-grades", methods=['POST'])
def assign_grade():
	"""assign project and grade to student"""
	github = request.form.get("github")
	title = request.form.get("title")
	grade = request.form.get("grade")
	student = hackbright.get_student_by_github(github)
	if student:
		hackbright.assign_grade(github, title, grade)
		flash('Grades have been added for ' + github)
		return redirect("/")
	else: 
		flash('There is no student with that name in our records')
		return redirect("/assign-grade")							

@app.route("/add-project")
def add_project():
	"""get form to add project"""
	return render_template("add_project.html")

@app.route("/project-add", methods=['POST'])
def add_projects():
	"""add project to database"""
	title = request.form.get("title")
	description = request.form.get("description")
	max_grade = request.form.get("max_grade")
	hackbright.add_student_project(title, description, max_grade)
	flash(title + ' has been added')
	return redirect("/")

@app.route("/delete-project")
def get_project_to_delete():
	"""get form to delete project"""
	return render_template("project_delete.html")


@app.route("/project-delete", methods=['POST'])
def project_delete():
	 """Check if project exists, delete a project."""
	 title = request.form.get("title")
	 check_title = hackbright.get_project_by_title(title)
	 if check_title:
	 	hackbright.delete_project_by_title(title)
	 	hackbright.delete_grades_by_title(title)
	 	flash(title + ' has been deleted')
	 	return redirect("/")
	 else: 
	 	flash('There is no project with that name in our records')
	 	return redirect("/delete-project")

if __name__ == "__main__":
	hackbright.connect_to_db(app)
	app.run(debug=True)

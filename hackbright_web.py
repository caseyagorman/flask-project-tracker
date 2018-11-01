"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)


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

@app.route("/new-student")
def get_new_student():

	return render_template("new_student.html")

@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""
    first = request.form.get("first")
    last = request.form.get("last")
    github = request.form.get("github")
    hackbright.make_new_student(first, last, github)

    return render_template("student_add.html", 
    						first=first,
    						last=last,
    						github=github)
							
@app.route("/student-delete")
def get_student_to_delete():
	return render_template("student_delete.html")


@app.route("/delete-student", methods=['POST'])
def student_delete():
	 """Delete a student."""
	 github = request.form.get("github")
	 hackbright.delete_student_by_github(github)
	 hackbright.delete_grades_by_github(github)
	 return redirect("/")

@app.route("/project")
def get_project():
	title = request.args.get("title")
	projects = hackbright.get_project_by_title(title)
	grades = hackbright.get_grades_by_title(title)
	return render_template("projects.html",
							projects=projects,
							grades=grades)

@app.route("/")
def list_students_and_projects():
	students = hackbright.get_all_students()
	projects = hackbright.get_all_projects()
	return render_template("homepage.html",
							students=students,
							projects=projects)

# @app.route("/assign-grade")
# def get_grades():
# 	return render_template("assign_grades.html")

# @app.route("/assign-grades", methods=['POST'])
# def assign_grade():
# 	github = request.args.get("github")
# 	title = request.args.get("title")
# 	grade = request.args.get("grade")

@app.route("/add-project")
def add_project():
	return render_template("add_project.html")

@app.route("/project-add", methods=['POST'])
def add_projects():
	title = request.form.get("title")
	description = request.form.get("description")
	max_grade = request.form.get("max_grade")
	hackbright.add_student_project(title, description, max_grade)
	return render_template("project_add.html",
							title=title,
							description=description,
							max_grade=max_grade)

@app.route("/delete-project")
def get_project_to_delete():
	return render_template("project_delete.html")


@app.route("/project-delete", methods=['POST'])
def project_delete():
	 """Delete a student."""
	 title = request.form.get("title")
	 hackbright.delete_project_by_title(title)
	 hackbright.delete_grades_by_title(title)
	 return redirect("/")

if __name__ == "__main__":
	hackbright.connect_to_db(app)
	app.run(debug=True)

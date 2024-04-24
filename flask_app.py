from datetime import datetime
import os

from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

from forms import RegistrationForm, LoginForm, SearchForm, NewEmployerForm, EditEmployerForm, \
    RelationForm, DeleteEmployerForm, AddAdminForm, RecordNewJobForm, AddEmployeeForm, EditEmployeeForm, \
    DeleteEmployeeForm, AddInstitutionForm, EditInstitutionForm, DeleteInstitutionForm, AddCertificationForm, \
    DeleteCertificationForm, EditCertificationForm

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from cryptography.fernet import Fernet


app = Flask(__name__)


app.config["SECRET_KEY"] = "c6d2f9789a32a64e8d12d42d2c955505"
app.config['MAIL_SERVER'] = "smtp.gmail.com."
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "organizationalodyssey@gmail.com"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_PASSWORD'] = "pgjdzozsuadatvzw"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config["FERNET_KEY"] = "VvPY8Yqf8U42_CyPWJwaDuHu4r-8LKcVwGgTJT3j_NQ="
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://" + "Brmiller2" + ":" + "8GH3#L!J&#Wpub^v" + "@" + "Brmiller2.mysql.pythonanywhere-services.com" + ":3306/" + "Brmiller2$default"#database URI

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
fernet = Fernet(app.config["FERNET_KEY"])
login_manager = LoginManager(app)


employer_relation = db.Table("employer_relation",
                             db.Column('parent_id', db.Integer, db.ForeignKey('employer.id')),
                             db.Column('child_id', db.Integer, db.ForeignKey('employer.id'))
                             )


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    email_confirmed = db.Column(db.Boolean, nullable=False, default=False)


class Employer(db.Model):
    __tablename__ = "employer"

    id = db.Column(db.Integer, primary_key=True)
    employer_name = db.Column(db.String(60), nullable=False, unique=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    headquarters_address = db.Column(db.String(60), nullable=False)
    industry_type = db.Column(db.String(60))
    description = db.Column(db.String(60))
    hasEmployed = db.relationship('EmployeeEmploymentRecord')
    child_employers = db.relationship("Employer",
                                      secondary=employer_relation,
                                      primaryjoin=(employer_relation.c.parent_id == id),
                                      secondaryjoin=(employer_relation.c.child_id == id),
                                      backref='parent_employers'
                                      )

class EmployeeEmploymentRecord(db.Model):
    __tablename__ = "employeeEmploymentRecord"

    id = db.Column(db.Integer, primary_key=True)
    theEmployee = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    theEmployer = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
    jobTitle = db.Column(db.String(60), nullable=False)
    startDate = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)

class Employee(db.Model):
    __tablename__ = "employee"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    employee_address = db.Column(db.String(60), nullable=False)
    email_address = db.Column(db.String(60), nullable=False)
    employers = db.relationship('EmployeeEmploymentRecord')

class Certification(db.Model):
    __tablename__ = "certification"

    id = db.Column(db.Integer, primary_key=True)
    CertificationName = db.Column(db.String(60), nullable=False)

class EmployeeCertificationForm(db.Model):
    __tablename__="employeeCertificationForm"

    id = db.Column(db.Integer, primary_key=True)
    certAwardedTo = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)    ##may need to be changed to just "employee" and remove '.id' same goes for as follows
    grantingInstitution = db.Column(db.Integer, db.ForeignKey('institution.id'), nullable=False)
    grantedCertification = db.Column(db.Integer, db.ForeignKey('certification.id'), nullable=False)
    awardDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Institution(db.Model):
    __tablename__ = "institution"

    id = db.Column(db.Integer, primary_key=True)
    institution_name = db.Column(db.String(60), nullable=False, unique=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash(f"No account exists with that email", "danger")
            return redirect(url_for("login"))
        if not user.email_confirmed:
            flash(f"Please activate your account before loging in", "danger")
            return redirect(url_for("login"))
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash(f"invalid credentials", "danger")
            return redirect(url_for("login"))
    return render_template("login.html", title="Log in", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if request.method == "POST" and form.validate():
        email = User.query.filter_by(email=form.email.data).first()
        if email:
            flash(f"An account with that email already exists", "danger")
            return redirect(url_for("register"))
        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=encrypted_password)
        db.session.add(user)
        db.session.commit()

        token = fernet.encrypt(user.email.encode())
        confirm_url = url_for("confirm_account", token=token, _external=True)
        html = render_template("email.html", confirm_url=confirm_url)
        msg = Message(
            "Confirm your email with Organizational Odyssey!",
            recipients=[user.email],
            html=html,
            sender="organizationalodyssey@gmail.com"
        )
        mail.send(msg)

        flash(f"Thank you for signing up! Please check your email to confirm your account", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Registration", form=form)


@app.route("/home")
@login_required
def home():  # put application's code here
    form = SearchForm()
    return render_template("home.html", form=form, current_user=current_user)


@app.route("/confirm/<token>")
def confirm_account(token):
    email = fernet.decrypt(token).decode()
    user = User.query.filter_by(email=email).first()
    user.email_confirmed = True
    db.session.commit()
    flash(f"Your account has been successfully registered!", "success")
    return redirect(url_for("login"))


@app.route("/visualization/<root_node>", methods=["GET", "POST"])
@app.route("/visualization", methods=["GET", "POST"])
@login_required
def visualization(root_node=None):
    form = SearchForm()
    data = {"nodes": [], "edges": []}
    visited_nodes = set()

    if root_node:
        start_point = fetch_start_point(root_node)
    else:
        start_point = fetch_start_point(form.search.data)

    if not start_point:
        flash("Start point not found", "danger")
        return redirect(url_for("home"))

    traverse_tree(start_point, data, visited_nodes)
    return render_template("visualization.html", data=data)


def fetch_start_point(identifier):
    employer = Employer.query.filter_by(employer_name=identifier).first()
    if employer:
        return employer
    employee = Employee.query.filter_by(first_name=identifier.split()[0], last_name=identifier.split()[-1]).first()
    if employee:
        return employee
    institution = Institution.query.filter_by(institution_name=identifier).first()
    return institution


def traverse_tree(node, data, visited_nodes):
    if node.id in visited_nodes:
        return
    visited_nodes.add(node.id)

    # Add node to data
    if isinstance(node, Employer):
        add_employer_node(node, data)
    elif isinstance(node, Employee):
        add_employee_node(node, data)
    elif isinstance(node, Institution):
        add_institution_node(node, data)

    # Recurse for connected nodes
    if isinstance(node, Employer):
        for child in node.child_employers:
            data['edges'].append({"from": node.id, "to": child.id, "type": "employer_relation"})
            traverse_tree(child, data, visited_nodes)
        for record in node.hasEmployed:
            employee = Employee.query.get(record.theEmployee)
            employer = Employer.query.get(record.theEmployer)
            data['edges'].append({"from": node.id, "to": employee.id, "type": "employed", "jobTitle": record.jobTitle,
                                  "startDate": record.startDate, "endDate": record.endDate})
            traverse_tree(employee, data, visited_nodes)
            if employer not in visited_nodes:
                traverse_tree(employer, data, visited_nodes)
    elif isinstance(node, Employee):
        for record in node.employers:
            employer = Employer.query.get(record.theEmployer)
            if employer.id not in visited_nodes:
                data['edges'].append(
                    {"from": node.id, "to": employer.id, "type": "employed_by", "jobTitle": record.jobTitle,
                     "startDate": record.startDate, "endDate": record.endDate})
                traverse_tree(employer, data, visited_nodes)
    elif isinstance(node, Institution):
        certifications = EmployeeCertificationForm.query.filter_by(grantingInstitution=node.id).all()
        for cert in certifications:
            employee = Employee.query.get(cert.certAwardedTo)
            data['edges'].append({"from": node.id, "to": employee.id, "type": "certified",
                                  "certificationName": Certification.query.get(
                                      cert.grantedCertification).CertificationName, "awardDate": cert.awardDate})
            traverse_tree(employee, data, visited_nodes)


def add_employer_node(employer, data):
    data['nodes'].append({
        "id": employer.id,
        "type": "Employer",
        "name": employer.employer_name,
        "start_date": employer.start_date.strftime("%Y-%m-%d"),
        "end_date": employer.end_date.strftime("%Y-%m-%d") if employer.end_date else "Active",
        "headquarters_address": employer.headquarters_address,
        "description": employer.description[:100] + "..." if len(employer.description) > 100 else employer.description
    })


def add_employee_node(employee, data):
    data['nodes'].append({
        "id": employee.id,
        "type": "Employee",
        "name": f"{employee.first_name} {employee.last_name}",
        "phone_number": employee.phone_number,
        "email_address": employee.email_address,
        "employee_address": employee.employee_address,
        "employers": [{"employer": Employer.query.get(record.theEmployer).employer_name,
                       "jobTitle": record.jobTitle,
                       "startDate": record.startDate,
                       "endDate": record.endDate} for record in employee.employers],
        "address": employee.employee_address})


def add_institution_node(institution, data):
    data['nodes'].append({
        "id": institution.id,
        "certifications": [{"certificationName": Certification.query.get(cert.grantedCertification).CertificationName,
                            "awardedTo": f"{Employee.query.get(cert.certAwardedTo).first_name} {Employee.query.get(cert.certAwardedTo).last_name}",
                            "awardDate": cert.awardDate} for cert in
                           EmployeeCertificationForm.query.filter_by(grantingInstitution=institution.id).all()],
        "name": institution.institution_name})


@app.route("/admin")
@login_required
def admin():
    if not current_user.admin:
        flash("Unauthorized Access", "danger")
        return redirect(url_for("home"))
    employer_form = NewEmployerForm()
    edit_employer_form = EditEmployerForm()
    delete_employer_form = DeleteEmployerForm()
    add_employee_form = AddEmployeeForm()
    edit_employee_form = EditEmployeeForm()
    delete_employee_form = DeleteEmployeeForm()
    relation_form = RelationForm()
    add_admin_form = AddAdminForm()
    record_new_job_form = RecordNewJobForm()
    add_institution_form = AddInstitutionForm()
    edit_institution_form = EditInstitutionForm()
    delete_institution_form = DeleteInstitutionForm()
    add_Certification_form = AddCertificationForm()
    edit_certification_form = EditCertificationForm()
    delete_certification_form = DeleteCertificationForm()

    return render_template("admin.html", new_employer_form=employer_form,
                           relation_form=relation_form,
                           edit_employer_form=edit_employer_form,
                           delete_employer_form=delete_employer_form, add_admin_form=add_admin_form,
                           add_employee_form=add_employee_form, edit_employee_form=edit_employee_form,
                           delete_employee_form=delete_employee_form, form=record_new_job_form,
                           add_institution_form=add_institution_form, edit_institution_form=edit_institution_form,
                           delete_institution_form=delete_institution_form,
                           add_Certification_form=add_Certification_form,
                           edit_certification_form=edit_certification_form,
                           delete_certification_form=delete_certification_form
                           )


@app.route("/employers")
@login_required
def employers():
    all_employers = Employer.query.all()
    employer_descriptions = []
    for employer in all_employers:
        employer_description = employer.description if employer.description != "" else "No Description"
        employer_description = (employer.description[:50] + "...") if len(employer.description) > 50 else employer.description
        employer_descriptions.append(employer_description)
    return render_template("employers.html", all_employers=all_employers, employer_descriptions=employer_descriptions)


@app.route("/add_employer", methods=["POST"])
@login_required
def add_employer():
    if not current_user.admin:
        return

    form = NewEmployerForm()
    if form.validate_on_submit():
        valid_employer = Employer.query.filter_by(employer_name=form.employer_name.data).first()
        if valid_employer:
            flash(f"Employer with name {valid_employer.employer_name} already exists", "danger")
            return redirect(url_for("admin"))

        new_employer = Employer(
            employer_name=form.employer_name.data,
            headquarters_address=form.headquarters_address.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data
        )
        db.session.add(new_employer)
        db.session.commit()
        flash("Employer added successfully!", "success")
    return redirect(url_for("admin"))


@app.route("/edit_employer", methods=["POST"])
@login_required
def edit_employer():
    if not current_user.admin:
        return

    form = EditEmployerForm()
    if form.validate_on_submit():
        employer = Employer.query.filter_by(employer_name=form.employer_name.data).first()
        if not employer:
            flash(f"{form.employer_name.data} does not exist", "danger")
            return redirect(url_for("admin"))

        edited = False
        if form.headquarters_address.data:
            employer.headquarters_address = form.headquarters_address.data
            edited = True
        if form.description.data:
            employer.description = form.description.data
            edited = True
        if form.start_date.data:
            employer.start_date = form.start_date.data
            edited = True
        if form.end_date.data:
            employer.end_date = form.end_date.data
            edited = True
        db.session.commit()

        if edited:
            flash("Employer has been successfully updated!", "success")
    return redirect(url_for("admin"))


@app.route("/delete_employer", methods=["POST"])
@login_required
def delete_employer():
    if not current_user.admin:
        return

    form = DeleteEmployerForm()
    if form.validate_on_submit():
        employer = Employer.query.filter_by(employer_name=form.employer_name.data).first()

        if not employer:
            flash(f"{form.employer_name.data} does not exist", "danger")
            return redirect(url_for("admin"))

        if employer.child_employers:
            flash(f"Cannot delete employer with child relationships", "danger")
            return redirect(url_for("admin"))

        db.session.delete(employer)
        db.session.commit()
        flash(f"Employer deleted", "success")
    return redirect(url_for("admin"))


@app.route("/add_relation", methods=["POST"])
@login_required
def add_relation():
    if not current_user.admin:
        return

    form = RelationForm()
    if form.validate_on_submit():
        parent_employer = Employer.query.filter_by(employer_name=form.parent_name.data).first()
        child_employer = Employer.query.filter_by(employer_name=form.child_name.data).first()
        if not parent_employer or not child_employer:
            flash("Child or Parent's name is incorrect", "danger")
            return redirect(url_for("home"))

        if child_employer in parent_employer.child_employers:
            flash("Relation already exits", "danger")
            return redirect(url_for("admin"))

        parent_employer.child_employers.append(child_employer)
        db.session.commit()
        flash("Relation added successfully!", "success")

    return redirect(url_for("admin"))


@app.route("/add_admin", methods=["POST"])
@login_required
def add_admin():
    if not current_user.admin:
        return

    form = AddAdminForm()
    if form.validate_on_submit():
        new_admin = User.query.filter_by(email=form.email_address.data).first()
        if not new_admin:
            flash("User does not exits", "danger")
            return redirect(url_for("admin"))

        new_admin.admin = True
        db.session.commit()
        flash("New admin successfully added", "success")

    return redirect(url_for("admin"))


# /////////////////// ADDING ALL PHASE 2 UCs BELOW HERE \\\\\\\\\\\\\\\\\\\\\\\\\\

@app.route("/add_employee", methods=["GET", "POST"])
@login_required
def add_employee():
    if not current_user.admin:
        flash("Unauthorized Access", "danger")
        return redirect(url_for("home"))
    form = AddEmployeeForm()
    if form.validate_on_submit():
        new_employee = Employee(first_name=form.first_name.data, last_name=form.last_name.data,
                                phone_number=form.phone_number.data, employee_address=form.employee_address.data,
                                email_address=form.email_address.data)
        db.session.add(new_employee)
        db.session.commit()
        flash("Employee added successfully!", "success")
        return redirect(url_for("admin"))
    return render_template("add_employee.html", form=form)


@app.route("/edit_employee", methods=["POST"])
@login_required
def edit_employee():
    if not current_user.admin:
        return

    form = EditEmployeeForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(first_name=form.first_name.data, last_name=form.last_name.data).first()
        if not employee:
            flash(f"{form.first_name.data} {form.last_name.data} does not exist", "danger")
            return redirect(url_for("admin"))

        edited = False
        if form.phone_number.data:
            employee.phone_number = form.phone_number.data
            edited = True
        if form.employee_address.data:
            employee.employee_address = form.employee_address.data
            edited = True
        if form.email_address.data:
            employee.email_address = form.email_address.data
            edited = True
        db.session.commit()

        if edited:
            flash("Employee has been successfully updated!", "success")
    return redirect(url_for("admin"))


@app.route("/delete_employee", methods=["POST"])
@login_required
def delete_employee():
    if not current_user.admin:
        return

    form = DeleteEmployeeForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(first_name=form.first_name.data, last_name=form.last_name.data).first()

        if not employee:
            flash(f"{form.first_name.data} {form.last_name.data} does not exist", "danger")
            return redirect(url_for("admin"))

        EmployeeEmploymentRecord.query.filter_by(theEmployee=employee.id).delete()

        db.session.delete(employee)
        db.session.commit()
        flash(f"Employee deleted", "success")
    return redirect(url_for("admin"))


from sqlalchemy import or_, and_


@app.route("/record_new_job", methods=["GET", "POST"])
@login_required
def record_new_job():
    form = RecordNewJobForm()  # Initializing the form to record new job

    if form.validate_on_submit():  # Checks if the form is submitted and validated
        # Fetching employee and employer from the database based on form input
        employee = Employee.query.filter_by(first_name=form.employee_first_name.data, last_name=form.employee_last_name.data).first()
        employer = Employer.query.filter_by(employer_name=form.employer_name.data).first()

        # If employee or employer is not found, flash this message and redirect
        if not employee:
            flash(f"Employee {form.employee_first_name.data} {form.employee_last_name.data} not found.", "danger")
            return redirect(url_for("record_new_job"))

        if not employer:
            flash(f"Employer {form.employer_name.data} not found.", "danger")
            return redirect(url_for("record_new_job"))

        # Start building the query to check for existing employment record
        query = EmployeeEmploymentRecord.query.filter(
            EmployeeEmploymentRecord.theEmployee == employee.id,
            EmployeeEmploymentRecord.theEmployer == employer.id,
            EmployeeEmploymentRecord.jobTitle == form.jobTitle.data
        )

        # Adjust query based on whether endDate is provided
        if form.endDate.data:
            query = query.filter(
                or_(
                    EmployeeEmploymentRecord.startDate <= form.endDate.data,
                    EmployeeEmploymentRecord.endDate >= form.startDate.data
                )
            )
        else:  # If no end date, ensure records start date is on or before forms start date
            query = query.filter(
                EmployeeEmploymentRecord.startDate <= form.startDate.data
            )

        existing_record = query.first()  # If a matching record exists flash this message

        if existing_record:
            flash("An employment record with similar details already exists.", "danger")
        else:
            # Create a new job record with form data
            new_job_record = EmployeeEmploymentRecord(
                theEmployee=employee.id,
                theEmployer=employer.id,
                jobTitle=form.jobTitle.data,
                startDate=form.startDate.data,
                endDate=form.endDate.data if form.endDate.data else None
            )
            db.session.add(new_job_record)  # Add a new record to session
            db.session.commit()  # Committing to save the record
            flash("New job record added successfully!", "success")

        return redirect(url_for("admin"))

    else:
        flash("Error in form, please correct and retry submission.", "danger")

    return render_template("record_new_job.html", form=form)


@app.route("/employees")
@login_required
def employees():
    all_employees = Employee.query.all()
    return render_template("employees.html", all_employees=all_employees)

# Still Needed
# def institutions, def addInstitution, def removeInstitution, def editInstitution, and def addDegreeOrCertification #Jenn
# add institution page #Gavin
# update admin page to add forms #Gavin
# update forms.py to include a addInstitution removeInstitution editInstitution and addDegreeOrCertification #Jenn
# def addEmployeeCertificationForm, update admin page to add form for EmployeeCertificationForm, update forms.py #Jenn

if __name__ == "__main__":
    app.run()


@app.route("/add_institution", methods=["GET", "POST"])
@login_required
def add_institution():
    if not current_user.admin:
        flash("Unauthorized Access", "danger")
        return redirect(url_for("home"))
    form = AddInstitutionForm()
    if form.validate_on_submit():
        new_institution = Institution(
            institution_name=form.institution_name.data
        )
        db.session.add(new_institution)
        db.session.commit()
        flash("Institution added successfully!", "success")
        return redirect(url_for("admin"))

    else:
        flash("Error in form, please correct and try resubmitting.", "danger")

    return render_template("add_institution.html", form=form)


@app.route("/edit_institution", methods=["POST"])
@login_required
def edit_institution():
    if not current_user.admin:
        return

    form = EditInstitutionForm()
    if form.validate_on_submit():
        institution = Institution.query.filter_by(institution_name=form.institution_name.data).first()
        if not institution:
            flash(f"{form.institution_name.data} does not exist", "danger")
            return redirect(url_for("admin"))

        edited = False
        if form.institution_name.data:
            institution.institution_name = form.institution_name.data
            edited = True
        db.session.commit()

        if edited:
            flash("Institution has been successfully updated!", "success")
    return redirect(url_for("admin"))


@app.route("/delete_institution", methods=["POST"])
@login_required
def delete_institution():
    if not current_user.admin:
        return

    form = DeleteInstitutionForm()
    if form.validate_on_submit():
        institution = Institution.query.filter_by(institution_name=form.institution_name.data).first()

        if not institution:
            flash(f"{form.institution_name.data}  does not exist", "danger")
            return redirect(url_for("admin"))

        db.session.delete(institution)
        db.session.commit()
        flash("Institution deleted", "success")
    return redirect(url_for("admin"))


from sqlalchemy import or_, and_


@app.route("/add_Certification", methods=["GET", "POST"])
@login_required
def add_Certification():
    if not current_user.admin:
        flash("Unauthorized Access", "danger")
        return redirect(url_for("home"))
    form = AddCertificationForm()
    if form.validate_on_submit():
        new_Certification = Institution(certificationName:=form.new_certification.data,)

        db.session.add(new_Certification)
        db.session.commit()
        flash("Certification added successfully!", "success")
        return redirect(url_for("admin"))
    return render_template("add_Certification.html", form=form)


@app.route("/edit_certification", methods=["POST"])
@login_required
def edit_certification():
    if not current_user.admin:
        return

    form = EditCertificationForm()
    if form.validate_on_submit():
        certification = Certification.query.filter_by(certificationName=form.new_certification.data).first()
        if not certification:
            flash(f"{form.new_certification.data} does not exist", "danger")
            return redirect(url_for("admin"))

        edited = False
        if form.new_certification.data:
            certification.new_certification = form.new_certification.data
            edited = True
        db.session.commit()

        if edited:
            flash("Certification has been successfully updated!", "success")
    return redirect(url_for("admin"))


@app.route("/delete_certification", methods=["POST"])
@login_required
def delete_certification():
    if not current_user.admin:
        return

    form = DeleteCertificationForm()
    if form.validate_on_submit():
        certification = Certification.query.filter_by(certificationName=form.new_certification.data).first()

        if not certification:
            flash(f"{form.new_certification.data} does not exist", "danger")
            return redirect(url_for("admin"))

        db.session.delete(certification)
        db.session.commit()
        flash("Certification deleted", "success")
    return redirect(url_for("admin"))


@app.route("/institutions")
@login_required
def institutions():
    all_institutions = Institution.query.all()
    return render_template("institutions.html", all_institutions=all_institutions)

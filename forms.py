from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Log in")


class SearchForm(FlaskForm):
    search = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Search")


class NewEmployerForm(FlaskForm):
    employer_name = StringField("Employer Name", validators=[DataRequired()])
    #new_employer_name = StringField("Employer Name", validators=[DataRequired()])
    headquarters_address = StringField('Headquarters Address', validators=[DataRequired()])
    description = StringField('Description', validators=[Optional()])
    start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Add Employer')


class EditEmployerForm(FlaskForm):
    employer_name = StringField("Current Employer Name", validators=[DataRequired()])
    new_employer_name = StringField("New Employer Name", validators=[DataRequired()])
    headquarters_address = StringField('Headquarters Address', validators=[Optional()])
    description = StringField('Description', validators=[Optional()])
    start_date = DateField('Start Date', validators=[Optional()], format='%Y-%m-%d')
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Edit Employer')


class DeleteEmployerForm(FlaskForm):
    employer_name = StringField("Employer Name", validators=[DataRequired()])
    #new_employer_name = StringField("Employer Name", validators=[DataRequired()])
    submit = SubmitField('Delete Employer')


class RelationForm(FlaskForm):
    parent_name = StringField("Parent Name", validators=[DataRequired()])
    child_name = StringField('Child Name', validators=[DataRequired()])
    submit = SubmitField('Add Relation')


class AddAdminForm(FlaskForm):
    email_address = StringField("Email Address", validators=[DataRequired()])
    submit = SubmitField("Create Admin")


class AddEmployeeForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[DataRequired(), Length(min=10, max=15)])
    employee_address = StringField("Address", validators=[DataRequired()])
    email_address = StringField("Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField("Add Employee")


class EditEmployeeForm(FlaskForm):
    current_first_name = StringField("Current First Name", validators=[DataRequired()])
    current_last_name = StringField("Current Last Name", validators=[DataRequired()])
    new_first_name = StringField("New First Name", validators=[DataRequired()])
    new_last_name = StringField("New Last Name", validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[DataRequired(), Length(min=10, max=15)])
    employee_address = StringField("Address", validators=[DataRequired()])
    email_address = StringField("Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField("Edit Employee")


class EmployeeCertificationForm(FlaskForm):
    employee_first_name = StringField("Employee First Name", validators=[DataRequired()])
    employee_last_name = StringField("Employee Last Name", validators=[DataRequired()])
    granting_institution = StringField("Granting Institution", validators=[DataRequired()])
    granted_certification = StringField("Granting Certification", validators=[DataRequired()])
    award_date = DateField('Award Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField("Add Employee Certification Form")

# Need to adjust this for employee. Has to be Employee First and Last name since that is what we query by.
# Change the function, HTML, and this flask form

class DeleteEmployeeForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    submit = SubmitField("Delete Employee")


class RecordNewJobForm(FlaskForm):
    employee_first_name = StringField("Employee First Name", validators=[DataRequired()])
    employee_last_name = StringField("Employee Last Name", validators=[DataRequired()])
    employer_name = StringField("Employer Name", validators=[DataRequired()])
    jobTitle = StringField("Job Title", validators=[DataRequired()])
    startDate = DateField("Start Date", validators=[DataRequired()], format='%Y-%m-%d')
    endDate = DateField("End Date", validators=[Optional()], format='%Y-%m-%d')
    submit = SubmitField("Record Job")


#              NEED TO ADD THE FOLLOWING FORMS
# 1. AddDegreeOrCertification
# 2. RemoveEmployeeForm (I am not sure if you really need this or not. I would think you would need this form
# to select which employee to remove.)
# 3.


class AddInstitutionForm(FlaskForm):
    institution_name = StringField("Institution Name", validators=[DataRequired()])
   # auth_cert = StringField("Authorized Certifications", validators=[DataRequired()])
   # phone_number = StringField("Phone Number", validators=[DataRequired(), Length(min=10, max=15)])
   # institution_address = StringField("Address", validators=[DataRequired()])
    # email_address = StringField("Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField("Add Institution")


class EditInstitutionForm(FlaskForm):
    institution_name = StringField("Current Institution Name", validators=[DataRequired()])
    new_institution_name = StringField("New Institution Name", validators=[DataRequired()])
    submit = SubmitField("Edit Institution")


class DeleteInstitutionForm(FlaskForm):
    institution_name = StringField("Institution Name", validators=[DataRequired()])
    # auth_cert = StringField("Authorized Certification", validators=[DataRequired()])
    submit = SubmitField("Delete Institution")


class AddCertificationForm(FlaskForm):
    new_certification = StringField("Certification", validators=[DataRequired()])
    submit = SubmitField('Add')


class EditCertificationForm(FlaskForm):
    current_certification = StringField("Current Certification", validators=[DataRequired()])
    new_certification = StringField("New Certification", validators=[DataRequired()])
    submit = SubmitField('Add')


class DeleteCertificationForm(FlaskForm):
    new_certification = StringField("Certification", validators=[DataRequired()])
    submit = SubmitField('Add')


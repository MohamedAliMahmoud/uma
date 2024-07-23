from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from email.mime.application import MIMEApplication
import random
import math
from flask import Flask, abort, render_template, redirect, url_for, flash, request, send_from_directory
from flask_paginate import Pagination, get_page_parameter
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Float
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.orm import relationship
from wtforms.fields.choices import SelectField

# Import your forms from the forms.py
from forms import RegisterForm, LoginForm, AddProject, AddProjectDetails, AddDataSubcontractors, DisplaySubcontractorsAccount, AddCustodySettlement, EmployeeDetails, SalaryCashOut, AddCustodyCashOut, EditCustodyName, AddInventoryItem, ImportInventoryMovement, ExportInventoryMovement, CashIn, UploadFile, Permissions, WorksTrack, InputWorksTracking, AddExpense, ExpenseCashOut, AddFinancialRequirement, AddSubcontractorRequirement, AddPurchaseRequirement, AddPurchaseRequirementItem, OperationExpensesCashOut
import datetime
import os


'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''
year = datetime.datetime.now().year
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
app.config['UPLOAD_FOLDER'] = os.environ.get("UPLOAD_FOLDER")
ckeditor = CKEditor(app)
Bootstrap5(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


def admin_check(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.is_authenticated:
            if current_user.id != 1:
                return abort(403)
        elif db.session.execute(db.select(User).where(User.id == 1)).scalar():
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function


# For adding profile images to the comment section
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)
# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'sqlite:///uma.db')
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Create a User table for all your registered users


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    custodes = relationship("CustodySettlement", back_populates="user_custody")
    cash: Mapped[int] = mapped_column(Integer, nullable=True)
    add_cash: Mapped[int] = mapped_column(Integer, nullable=True)
    display_cash_account: Mapped[int] = mapped_column(Integer, nullable=True)
    edit_cash_in: Mapped[int] = mapped_column(Integer, nullable=True)
    delete_cash_in: Mapped[int] = mapped_column(Integer, nullable=True)
    projects: Mapped[int] = mapped_column(Integer, nullable=True)
    add_project: Mapped[int] = mapped_column(Integer, nullable=True)
    edit_project: Mapped[int] = mapped_column(Integer, nullable=True)
    display_all_projects: Mapped[int] = mapped_column(Integer, nullable=True)
    display_project: Mapped[int] = mapped_column(Integer, nullable=True)
    add_project_details: Mapped[int] = mapped_column(Integer, nullable=True)
    edit_project_details: Mapped[int] = mapped_column(Integer, nullable=True)
    delete_project_details: Mapped[int] = mapped_column(Integer, nullable=True)
    add_works_tracking: Mapped[int] = mapped_column(Integer, nullable=True)
    delete_works_tracking: Mapped[int] = mapped_column(Integer, nullable=True)
    add_subcontractor_opening_account: Mapped[int] = mapped_column(Integer, nullable=True)
    add_subcontractor_cash_out: Mapped[int] = mapped_column(Integer, nullable=True)
    display_subcontractor_account: Mapped[int] = mapped_column(Integer, nullable=True)
    edit_subcontractor_account: Mapped[int] = mapped_column(Integer, nullable=True)
    delete_subcontractor_account: Mapped[int] = mapped_column(Integer, nullable=True)
    display_project_cost: Mapped[int] = mapped_column(Integer, nullable=True)
    custody: Mapped[int] = mapped_column(Integer, nullable=True)
    display_my_custody: Mapped[int] = mapped_column(Integer, nullable=True)
    display_all_custodes: Mapped[int] = mapped_column(Integer, nullable=True)
    display_employee_custody: Mapped[int] = mapped_column(Integer, nullable=True)
    edit_employee_name: Mapped[int] = mapped_column(Integer, nullable=True)
    add_custody_settlement: Mapped[int] = mapped_column(Integer, nullable=True)
    edit_custody_settlement: Mapped[int] = mapped_column(Integer, nullable=True)
    delete_custody_settlement: Mapped[int] = mapped_column(Integer, nullable=True)
    add_custody_cash_out: Mapped[int] = mapped_column(Integer, nullable=True)
    edit_custody_cash_out: Mapped[int] = mapped_column(Integer, nullable=True)
    delete_custody_cash_out: Mapped[int] = mapped_column(Integer, nullable=True)
    payroll: Mapped[int] = mapped_column(Integer, nullable=True)
    add_employee: Mapped[int] = mapped_column(Integer, nullable=True)
    display_all_employees: Mapped[int] = mapped_column(Integer, nullable=True)
    salary_cash_out: Mapped[int] = mapped_column(Integer, nullable=True)
    display_employee_salary: Mapped[int] = mapped_column(Integer, nullable=True)
    edit_employee_details: Mapped[int] = mapped_column(Integer, nullable=True)
    edit_salary: Mapped[int] = mapped_column(Integer, nullable=True)
    delete_salary: Mapped[int] = mapped_column(Integer, nullable=True)
    inventory: Mapped[int] = mapped_column(Integer, nullable=True)
    add_item: Mapped[int] = mapped_column(Integer, nullable=True)
    display_all_items: Mapped[int] = mapped_column(Integer, nullable=True)
    edit_item: Mapped[int] = mapped_column(Integer, nullable=True)
    import_item: Mapped[int] = mapped_column(Integer, nullable=True)
    export_item: Mapped[int] = mapped_column(Integer, nullable=True)
    display_item_movements: Mapped[int] = mapped_column(Integer, nullable=True)
    edit_item_movement: Mapped[int] = mapped_column(Integer, nullable=True)
    delete_item_movement: Mapped[int] = mapped_column(Integer, nullable=True)
    expenses: Mapped[int] = mapped_column(Integer, nullable=True)
    add_expense: Mapped[int] = mapped_column(Integer, nullable=True)
    display_all_expenses: Mapped[int] = mapped_column(Integer, nullable=True)
    expense_cash_out: Mapped[int] = mapped_column(Integer, nullable=True)
    display_expense_details: Mapped[int] = mapped_column(Integer, nullable=True)
    edit_expense: Mapped[int] = mapped_column(Integer, nullable=True)
    edit_expense_cash_out: Mapped[int] = mapped_column(Integer, nullable=True)
    delete_expense_cash_out: Mapped[int] = mapped_column(Integer, nullable=True)
    operating_expense_cash_out: Mapped[int] = mapped_column(Integer, nullable=True)
    display_all_operating_expenses: Mapped[int] = mapped_column(Integer, nullable=True)
    edit_operating_expense: Mapped[int] = mapped_column(Integer, nullable=True)
    delete_operating_expense: Mapped[int] = mapped_column(Integer, nullable=True)
    notifications: Mapped[int] = mapped_column(Integer, nullable=True)
    add_financial_requirement: Mapped[int] = mapped_column(Integer, nullable=True)
    display_all_financial_requirements: Mapped[int] = mapped_column(Integer, nullable=True)
    delete_financial_requirement: Mapped[int] = mapped_column(Integer, nullable=True)
    add_subcontractor_requirement: Mapped[int] = mapped_column(Integer, nullable=True)
    display_subcontractor_requirements: Mapped[int] = mapped_column(Integer, nullable=True)
    edit_subcontractor_requirement: Mapped[int] = mapped_column(Integer, nullable=True)
    delete_subcontractor_requirement: Mapped[int] = mapped_column(Integer, nullable=True)
    add_purchase_requirement: Mapped[int] = mapped_column(Integer, nullable=True)
    display_purchase_requirements: Mapped[int] = mapped_column(Integer, nullable=True)
    upload_file: Mapped[int] = mapped_column(Integer, nullable=True)
    download_file: Mapped[int] = mapped_column(Integer, nullable=True)
    delete_file: Mapped[int] = mapped_column(Integer, nullable=True)




class Project(db.Model):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    customer_name: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    total: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    date: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    details = relationship("ProjectDetail", back_populates="details_project")
    subcontractors = relationship("SubContractor", back_populates="subcontractors_project")
    costs = relationship("ProjectCost", back_populates="project_cost")
    file_path: Mapped[str] = mapped_column(String(100), unique=False, nullable=True)
    track_number: Mapped[str] = mapped_column(String(100), unique=False, nullable=True)


class ProjectDetail(db.Model):
    __tablename__ = "project_details"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_name: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    description: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    total: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("projects.id"))
    details_project = relationship("Project", back_populates="details")
    works_track = relationship("WorkTrack", back_populates="works_detail_track")


class WorkTrack(db.Model):
    __tablename__ = "works_tracks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_path: Mapped[str] = mapped_column(String(100), unique=False, nullable=True)
    percentage: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    project_details_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("project_details.id"))
    works_detail_track = relationship("ProjectDetail", back_populates="works_track")


class ProjectCost(db.Model):
    __tablename__ = "project_costs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    total: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
    date: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("projects.id"))
    project_cost = relationship("Project", back_populates="costs")
    cost_name: Mapped[str] = mapped_column(String(100), unique=False, nullable=True)
    subcontractor_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    file_path: Mapped[str] = mapped_column(String(100), unique=False, nullable=True)


class SubContractor(db.Model):
    __tablename__ = "subcontractors"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    description: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    opening_balance: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    cash_out: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    date: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("projects.id"))
    subcontractors_project = relationship("Project", back_populates="subcontractors")
    cash_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    file_path: Mapped[str] = mapped_column(String(100), unique=False, nullable=True)


class Custody(db.Model):
    __tablename__ = "custodes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    debit: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    credit: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    balance: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    custody_settlements = relationship("CustodySettlement", back_populates="custody")


class CustodySettlement(db.Model):
    __tablename__ = "Custody_settlements"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    debit: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    credit: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    date: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    user_custody = relationship("User", back_populates="custodes")
    project_cost_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    custody_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("custodes.id"))
    custody = relationship("Custody", back_populates="custody_settlements")
    cash_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    file_path: Mapped[str] = mapped_column(String(100), unique=False, nullable=True)


class InventoryItem(db.Model):
    __tablename__ = "inventory_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    quantity_in: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    unit_price_average: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    total_in: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    quantity_out: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    total_out: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    quantity_balance: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    total_balance: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    item_movements = relationship("InventoryMovement", back_populates="inventory_item")


class InventoryMovement(db.Model):
    __tablename__ = "inventory_movements"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(100), unique=False, nullable=True)
    quantity_in: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    unit_price_in: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    total_in: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    quantity_out: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    unit_price_out: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    total_out: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    date: Mapped[str] = mapped_column(String(100), unique=False, nullable=True)
    project_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    project_cost_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    inventory_item_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("inventory_items.id"))
    inventory_item = relationship("InventoryItem", back_populates="item_movements")
    cash_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    file_path: Mapped[str] = mapped_column(String(100), unique=False, nullable=True)


class Employee(db.Model):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    contact_number: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    total_salary: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    salaries = relationship("EmployeesSalary", back_populates="employee")


class EmployeesSalary(db.Model):
    __tablename__ = "employees_salary"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    salary: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
    date: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    employee_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("employees.id"))
    employee = relationship("Employee", back_populates="salaries")
    cash_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    file_path: Mapped[str] = mapped_column(String(100), unique=False, nullable=True)


class Cash(db.Model):
    __tablename__ = "cashes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    debit: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
    credit: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
    balance: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
    date: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    contra_account: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    file_path: Mapped[str] = mapped_column(String(100), unique=False, nullable=True)


class Expense(db.Model):
    __tablename__ = "expenses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    total: Mapped[float] = mapped_column(Float, unique=False, nullable=True)
    expense_details = relationship("ExpenseDetail", back_populates="expense")


class ExpenseDetail(db.Model):
    __tablename__ = "expense_details"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    total: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
    date: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    expense_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("expenses.id"))
    expense = relationship("Expense", back_populates="expense_details")
    cash_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    file_path: Mapped[str] = mapped_column(String(100), unique=False, nullable=True)


class OperationExpense(db.Model):
    __tablename__ = "operation_expenses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    total: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
    date: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    cash_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    project_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    project_cost_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    file_path: Mapped[str] = mapped_column(String(100), unique=False, nullable=True)


class FinancialRequirement(db.Model):
    __tablename__ = "financial_requirements"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    total: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
    date: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    file_path: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)


class SubcontractorRequirement(db.Model):
    __tablename__ = "subcontractor_requirements"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    project_name: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    subcontractor_name: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    percentage: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
    status: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    date: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)



class PurchaseRequirement(db.Model):
    __tablename__ = "purchase_requirements"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=True)
    project_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    date: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    status: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    purchase_requirement_items = relationship("PurchaseRequirementItem", back_populates="purchase_requirement")


class PurchaseRequirementItem(db.Model):
    __tablename__ = "purchase_requirement_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    status: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    purchase_requirement_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("purchase_requirements.id"))
    purchase_requirement = relationship("PurchaseRequirement", back_populates="purchase_requirement_items")


with app.app_context():
    db.create_all()

def add_cash(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.add_cash != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def display_cash_account(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.display_cash_account != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def edit_cash_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.edit_cash_in != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def delete_cash_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.delete_cash_in != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function



def add_project(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.add_project != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def edit_project(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.edit_project != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def display_all_projects(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.display_all_projects != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def display_project(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.display_project != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def add_project_details(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.add_project_details != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def edit_project_details(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.edit_project_details != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def delete_project_details(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.delete_project_details != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def add_works_tracking(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.add_works_tracking != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def delete_works_tracking(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.delete_works_tracking != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def add_subcontractor_opening_account(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.add_subcontractor_opening_account != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def add_subcontractor_cash_out(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.add_subcontractor_cash_out != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def display_subcontractor_account(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.display_subcontractor_account != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def edit_subcontractor_account(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.edit_subcontractor_account != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def delete_subcontractor_account(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.delete_subcontractor_account != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def display_project_cost(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.display_project_cost != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def display_my_custody(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.display_my_custody != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def display_all_custodes(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.display_all_custodes != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def display_employee_custody(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.display_employee_custody != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def edit_employee_name(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.edit_employee_name != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def add_custody_settlement(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.add_custody_settlement != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def edit_custody_settlement(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.edit_custody_settlement != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def delete_custody_settlement(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.delete_custody_settlement != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def add_custody_cash_out(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.add_custody_cash_out != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def edit_custody_cash_out(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.edit_custody_cash_out != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def delete_custody_cash_out(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.delete_custody_cash_out != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def add_employee(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.add_employee != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def display_all_employees(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.display_all_employees != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def salary_cash_out(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.salary_cash_out != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def display_employee_salary(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.display_employee_salary != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def edit_employee_details(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.edit_employee_details != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def edit_salary(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.edit_salary != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def delete_salary(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.delete_salary != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def add_item(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.add_item != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def display_all_items(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.display_all_items != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def edit_item(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.edit_item != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def import_item(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.import_item != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def export_item(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.export_item != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def display_item_movements(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.display_item_movements != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def edit_item_movement(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.edit_item_movement != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def delete_item_movement(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.delete_item_movement != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def add_expense(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.add_expense != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def display_all_expenses(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.display_all_expenses != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def expense_cash_out(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.expense_cash_out != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def display_expense_details(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.display_expense_details != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def edit_expense(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.edit_expense != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def edit_expense_cash_out(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.edit_expense_cash_out != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def delete_expense_cash_out(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.delete_expense_cash_out != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def operating_expense_cash_out(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.operating_expense_cash_out != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def display_all_operating_expenses(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.display_all_operating_expenses != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def edit_operating_expense(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.edit_operating_expense != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def delete_operating_expense(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.delete_operating_expense != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def add_financial_requirement(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.add_financial_requirement != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def display_all_financial_requirements(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.display_all_financial_requirements != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def delete_financial_requirement(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.delete_financial_requirement != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def add_subcontractor_requirement(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.add_subcontractor_requirement != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def display_subcontractor_requirements(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.display_subcontractor_requirements != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def edit_subcontractor_requirement(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.edit_subcontractor_requirement != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def delete_subcontractor_requirement(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.delete_subcontractor_requirement != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def add_purchase_requirement(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.add_purchase_requirement != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def display_purchase_requirements(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.display_purchase_requirements != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def upload_file(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.upload_file != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def download_file(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.download_file != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


def delete_file(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.delete_file != 2:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function



# Create an admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function


# Register new users into the User database
@app.route('/register', methods=["GET", "POST"])
@admin_check
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user email is already present in the database.
        if form.password.data == form.confirm_password.data:
            result = db.session.execute(db.select(User).where(User.email == form.email.data))
            user = result.scalar()
            if user:
                # User already exists
                flash("You've already signed up with that email, log in instead!")
                return redirect(url_for('login'))

            hash_and_salted_password = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_user = User(
                email=form.email.data,
                name=form.name.data.title(),
                password=hash_and_salted_password,
            )

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            new_custody = Custody(name=form.name.data, debit=0, credit=0, balance=0, user_id=current_user.id)
            db.session.add(new_custody)
            db.session.commit()

            if new_user.id == 1:
                new_user.cash = 2
                new_user.add_cash = 2
                new_user.display_cash_account = 2
                new_user.edit_cash_in = 2
                new_user.delete_cash_in = 2
                new_user.projects = 2
                new_user.add_project = 2
                new_user.edit_project = 2
                new_user.display_all_projects = 2
                new_user.display_project = 2
                new_user.add_project_details = 2
                new_user.edit_project_details = 2
                new_user.delete_project_details = 2
                new_user.add_works_tracking = 2
                new_user.delete_works_tracking = 2
                new_user.add_subcontractor_opening_account = 2
                new_user.add_subcontractor_cash_out = 2
                new_user.display_subcontractor_account = 2
                new_user.edit_subcontractor_account = 2
                new_user.delete_subcontractor_account = 2
                new_user.display_project_cost = 2
                new_user.custody = 2
                new_user.display_my_custody = 2
                new_user.display_all_custodes = 2
                new_user.display_employee_custody = 2
                new_user.edit_employee_name = 2
                new_user.add_custody_settlement = 2
                new_user.edit_custody_settlement = 2
                new_user.delete_custody_settlement = 2
                new_user.add_custody_cash_out = 2
                new_user.edit_custody_cash_out = 2
                new_user.delete_custody_cash_out = 2
                new_user.payroll = 2
                new_user.add_employee = 2
                new_user.display_all_employees = 2
                new_user.salary_cash_out = 2
                new_user.display_employee_salary = 2
                new_user.edit_employee_details = 2
                new_user.edit_salary = 2
                new_user.delete_salary = 2
                new_user.inventory = 2
                new_user.add_item = 2
                new_user.edit_item = 2
                new_user.display_all_items = 2
                new_user.display_item_movements = 2
                new_user.edit_item_movement = 2
                new_user.delete_item_movement = 2
                new_user.import_item = 2
                new_user.export_item = 2
                new_user.expenses = 2
                new_user.add_expense = 2
                new_user.display_all_expenses = 2
                new_user.expense_cash_out = 2
                new_user.display_expense_details = 2
                new_user.edit_expense = 2
                new_user.edit_expense_cash_out = 2
                new_user.delete_expense_cash_out = 2
                new_user.operating_expense_cash_out = 2
                new_user.display_all_operating_expenses = 2
                new_user.edit_operating_expense = 2
                new_user.delete_operating_expense = 2
                new_user.notifications = 2
                new_user.add_financial_requirement = 2
                new_user.display_all_financial_requirements = 2
                new_user.delete_financial_requirement = 2
                new_user.add_subcontractor_requirement = 2
                new_user.display_subcontractor_requirements = 2
                new_user.edit_subcontractor_requirement = 2
                new_user.delete_subcontractor_requirement = 2
                new_user.add_purchase_requirement = 2
                new_user.display_purchase_requirements = 2
                new_user.upload_file = 2
                new_user.download_file = 2
                new_user.delete_file = 2
                db.session.commit()

            # This line will authenticate the user with Flask-Login
            return render_template("dashboard.html", logged_in=current_user.is_authenticated, year=year)
        else:
            flash("Those passwords didn’t match. Try again.")
            return redirect(url_for('register'))
    return render_template("register.html", form=form, current_user=current_user, logged_in=current_user.is_authenticated, year=year)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return render_template("dashboard.html", logged_in=current_user.is_authenticated, year=year)
    return render_template("login.html", form=form, current_user=current_user, logged_in=current_user.is_authenticated, year=year)


@app.route("/interior_finishing")
def interior_finishing():
    return render_template("interior-finishing.html", year=year)


@app.route("/exterior_finishing")
def exterior_finishing():
    return render_template("exterior-finishing.html", year=year)


@app.route("/swimming_pool_construction")
def swimming_pool_construction():
    return render_template("swimming-pool-construction.html", year=year)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/home_decor")
def home_decor():
    return render_template("home-decor.html", year=year)


@app.route('/')
def get_all_posts():
    return render_template("index.html", current_user=current_user, year=year)


# Add a POST method to be able to post comments


@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user, year=year)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        user_email = request.form["email"]
        phone = request.form["phone"]
        body = request.form["message"]
        password = os.environ.get("PASSWORD")
        msg = MIMEMultipart()
        msg["From"] = os.environ.get("EMAIL")
        msg["To"] = 'sekam85@gmail.com'
        msg["Subject"] = "Contact us"
        all_message = f"Name is: {name}\nEmail is: {user_email}\nPhone is: {phone}\nMessage is: {body}"
        msg.attach(MIMEText(all_message, 'plain'))
        with SMTP("Smtp.gmail.com:587") as connection:
            connection.starttls()
            connection.login(user=msg["From"], password=password)
            connection.sendmail(from_addr=msg["From"], to_addrs=msg["To"], msg=msg.as_string())
            return render_template("contact.html", msg_sent=True, year=year)
    return render_template("contact.html", year=year)


@app.route("/all_users")
@login_required
@admin_only
def all_users():
    result = db.session.execute(db.select(User))
    users = result.scalars().all()
    return render_template("all-users.html", users=users)


@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
@login_required
@admin_only
def edit_user(user_id):
    requested_user = db.get_or_404(User, user_id)
    form = RegisterForm(email=requested_user.email, name=requested_user.name)
    if form.validate_on_submit():
        if form.password.data == form.confirm_password.data:
            requested_user.email = form.email.data
            requested_user.name = form.name.data
            hash_and_salted_password = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            requested_user.password = hash_and_salted_password
            db.session.commit()
            return redirect(url_for('all_users'))
        else:
            flash("Those passwords didn’t match. Try again.")
            return redirect(url_for('edit_user'))
    return render_template('edit_user.html', form=form, logged_in=current_user.is_authenticated)


@app.route("/add_project", methods=["GET", "POST"])
@login_required
@add_project
def add_project():
    form = AddProject()
    if form.validate_on_submit():
        result = db.session.execute(
            db.select(Project).where(Project.project_name == form.project_name.data.title())).scalar()
        if result:
            flash("You've already Added this Project, add instead!")
            return redirect(url_for('add_project'))
        new_project = Project(project_name=form.project_name.data.title(), customer_name=form.customer_name.data.title(), description=form.description.data, date=datetime.datetime.now().strftime("%d/%m/%Y"))
        db.session.add(new_project)
        db.session.commit()
        track_number(project_id=new_project.id)
        flash("Project  added Successfully")
        return redirect(url_for('add_project'))
    return render_template("add-project.html", form=form, year=year)


@app.route("/display_project/<int:project_id>")
@login_required
@display_project
def display_project(project_id):
    requested_project = db.get_or_404(Project, project_id)
    project_details = db.session.execute(db.select(ProjectDetail).where(ProjectDetail.project_id == project_id)).scalars().all()
    project_total = 0
    for project_detail in project_details:
        project_total += project_detail.total
    requested_project.total = project_total
    db.session.commit()
    return render_template("display_project.html", project=requested_project, year=year)


@app.route("/all_projects")
@login_required
@display_all_projects
def all_projects():
    result = db.session.execute(db.select(Project))
    projects = result.scalars().all()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(projects, page=page, css_framework='bootstrap5', total=len(projects), search=search,
                            record_name='All Projects')
    all_projects_paginate = db.paginate(db.select(Project), page=page, per_page=10, error_out=False)
    return render_template("all-projects.html", projects=all_projects_paginate, year=year,pagination=pagination )


@app.route("/search", methods=["GET", "POST"])
@login_required
@display_all_projects
def search_projects():
    if request.method == "POST":
        search_text = request.form["input_name"]
        search_format = "%{}%".format(search_text)
        if db.session.execute(db.select(Project).where(Project.project_name.like(search_format.title()))).scalars().all():
            result = db.session.execute(db.select(Project).where(Project.project_name.like(search_format.title()))).scalars()
            return render_template("all-projects.html", projects=result, year=year, search=True)

        elif db.session.execute(db.select(Project).where(Project.description.like(search_format.title()))).scalars().all():
            result = db.session.execute(db.select(Project).where(Project.description.like(search_format.title()))).scalars()
            return render_template("all-projects.html", projects=result, year=year, search=True)
        elif db.session.execute(db.select(Project).where(Project.date.like(search_format.title()))).scalars().all():
            result = db.session.execute(db.select(Project).where(Project.date.like(search_format.title()))).scalars()
            return render_template("all-projects.html", projects=result, year=year, search=True)
        elif db.session.execute(db.select(Project).where(Project.track_number.like(search_format))).scalars().all():
            result = db.session.execute(db.select(Project).where(Project.track_number.like(search_format))).scalars()
            return render_template("all-projects.html", projects=result, year=year, search=True)
        else:
            flash("this Project not exist")
            return redirect(url_for('all_projects'))


@app.route("/edit_project/<int:project_id>" ,methods=["GET", "POST"])
@login_required
@edit_project
def edit_project(project_id):
    requested_project = db.get_or_404(Project, project_id)
    form = AddProject(project_name=requested_project.project_name, description=requested_project.description, customer_name=requested_project.customer_name)
    if form.validate_on_submit():
        requested_project.project_name = form.project_name.data
        requested_project.description = form.description.data
        requested_project.customer_name = form.customer_name.data.title()
        db.session.commit()
        return redirect(url_for('all_projects'))
    return render_template("add-project.html", form=form, edit_project=True)


@app.route("/add_project_details/<int:project_id>", methods=["GET", "POST"])
@login_required
@add_project_details
def add_project_details(project_id):
    form = AddProjectDetails()
    requested_project = db.get_or_404(Project, project_id)
    form.item_name.choices = ["سيراميك", "حدادة", "نقاشة", "رخام", "سباكة","كهرباء", "محارة", "حمام سباحة", "نجارة","تكييفات"]
    if form.validate_on_submit():
        new_project_details = ProjectDetail(item_name=form.item_name.data, description=form.description.data,
                                            total=form.total.data, project_id=project_id)
        db.session.add(new_project_details)
        project_details = db.session.execute(
            db.select(ProjectDetail).where(ProjectDetail.project_id == project_id)).scalars().all()
        db.session.commit()
        project_total = 0
        for project_detail in project_details:
            project_total += project_detail.total
        requested_project.total = project_total
        db.session.commit()
        flash("Project Details  added Successfully")
        return redirect(url_for('add_project_details',project_id=project_id))
    return render_template("add_project_details.html", form=form)


@app.route("/edit_project_details/<int:project_detail_id>", methods=["GET", "POST"])
@login_required
@edit_project_details
def edit_project_details(project_detail_id):
    requested_project_detail = db.get_or_404(ProjectDetail, project_detail_id)
    project_details = db.session.execute(
        db.select(ProjectDetail).where(ProjectDetail.project_id == requested_project_detail.project_id)).scalars().all()

    form = AddProjectDetails(item_name=requested_project_detail.item_name,
                             description=requested_project_detail.description, total=requested_project_detail.total)
    form.item_name.choices = ["سيراميك", "حدادة", "نقاشة", "رخام", "سباكة", "كهرباء", "محارة", "نجارة", "حمام سباحة", "تكييفات"]
    if form.validate_on_submit():
        requested_project_detail.item_name = form.item_name.data
        requested_project_detail.description = form.description.data
        requested_project_detail.total = form.total.data
        db.session.commit()
        requested_project = db.session.execute(db.select(Project).where(Project.id == requested_project_detail.project_id)).scalar()
        project_total = 0
        for project_detail in project_details:
            project_total += project_detail.total
        requested_project.total = project_total
        db.session.commit()
        return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
    return render_template("add_project_details.html", form=form, edit_project_details=True)


@app.route("/delete_project_details/<int:project_detail_id>", methods=["GET", "POST"])
@login_required
@delete_project_details
def delete_project_details(project_detail_id):
    requested_project_detail = db.get_or_404(ProjectDetail, project_detail_id)
    requested_project_detail = db.get_or_404(ProjectDetail, project_detail_id)
    works_tracking = db.session.execute(
        db.select(WorkTrack).where(WorkTrack.project_details_id == project_detail_id)).scalars().all()
    for work_tracking in works_tracking:
        try:
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                   secure_filename(work_tracking.file_path)))
        except FileNotFoundError:
            pass
        db.session.delete(work_tracking)
        db.session.commit()
    db.session.delete(requested_project_detail)
    db.session.commit()
    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))



@app.route("/opening_balance_subcontractor/<int:project_id>", methods=["GET", "POST"])
@login_required
@add_subcontractor_opening_account
def add_subcontractor_opening_balance(project_id):
    form = AddDataSubcontractors()
    form.subcontractor_name.choices = ["مقاول نجارة", "مقاول محارة", "مقاول كهرباء", "مقاول سباكة", "مقاول رخام",
                                       "مقاول سيراميك", "مقاول نقاشة", "مقاول حمام سباحة","مقاول تكييفات","مقاول حدادة"]
    if form.validate_on_submit():
        new_subcontractor = SubContractor(name=form.subcontractor_name.data, description=form.description.data,
                                          opening_balance=form.total.data, cash_out=0,
                                          date=datetime.datetime.now().strftime("%d/%m/%Y"), project_id=project_id)
        db.session.add(new_subcontractor)
        db.session.commit()
        flash("Opening balance added successfully.")
        return redirect(url_for('add_subcontractor_opening_balance', project_id=project_id))
    return render_template("add_opening_balance_subcontractor.html", form=form, opening_balance=True)



@app.route("/display_subcontractor_accounts/<int:project_id>", methods=["GET", "POST"])
@login_required
@display_subcontractor_account
def display_subcontractor_accounts(project_id):
    requested_project = db.get_or_404(Project, project_id)
    form = DisplaySubcontractorsAccount()
    list_subcontractors = []
    requested_contractors = db.session.execute(db.select(SubContractor).where(SubContractor.project_id == project_id)).scalars().all()
    for contract in requested_contractors:
        if contract.name not in list_subcontractors:
            list_subcontractors.append(contract.name)
    form.subcontractor_name.choices = list_subcontractors
    if form.validate_on_submit():
        subcontractors = db.session.execute(db.select(SubContractor).where(SubContractor.name == form.subcontractor_name.data, SubContractor.project_id == project_id)).scalars().all()
        total_opening_balance = 0
        total_cash_out = 0
        for subcontractor in subcontractors:
            total_opening_balance += subcontractor.opening_balance
            total_cash_out += subcontractor.cash_out
        balance = total_opening_balance - total_cash_out
        if subcontractors:
            return render_template("display_subcontractor_accounts.html", form=form,
                                   subcontractors=subcontractors,project=requested_project, balance=balance)
        else:
            flash("There is not data entry at this subcontractor")
            redirect(url_for("display_subcontractor_accounts", project_id=project_id))
    return render_template("display_subcontractor_accounts.html", form=form, project=requested_project)



@app.route("/delete_subcontractor_data/<int:subcontractor_id>")
@login_required
@delete_subcontractor_account
def delete_subcontractor_data(subcontractor_id):
    requested_subcontractor = db.session.execute(db.select(SubContractor).where(SubContractor.id == subcontractor_id)).scalar()
    requested_cash_out = db.session.execute(db.select(Cash).where(Cash.id == requested_subcontractor.cash_id)).scalar()
    requested_project_cost = db.session.execute(db.select(ProjectCost).where(ProjectCost.subcontractor_id == requested_subcontractor.id)).scalar()
    file_name = requested_subcontractor.file_path
    if requested_cash_out:
        db.session.delete(requested_cash_out)
        db.session.commit()
    if requested_project_cost:
        db.session.delete(requested_project_cost)
        db.session.commit()
    try:
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                               secure_filename(file_name)))
    except FileNotFoundError:
        pass
    except TypeError:
        pass
    except PermissionError:
        pass
    db.session.delete(requested_subcontractor)
    db.session.commit()
    flash("This item has been deleted")
    return redirect(url_for('display_subcontractor_accounts', project_id=requested_subcontractor.project_id))



@app.route("/insert_subcontractor_cash_out/<int:project_id>", methods=["GET", "POST"])
@login_required
@add_subcontractor_cash_out
def insert_subcontractor_cash_out(project_id):
    requested_project = db.get_or_404(Project, project_id)
    form = AddDataSubcontractors()
    form.subcontractor_name.choices = ["مقاول نجارة", "مقاول محارة", "مقاول كهرباء", "مقاول سباكة", "مقاول رخام",
                                       "مقاول سيراميك", "مقاول نقاشة", "مقاول حمام سباحة", "مقاول حدادة","مقاول تكييفات"]
    if form.validate_on_submit():
        new_cash = Cash(description=form.description.data, credit=form.total.data, debit=0, balance=0,
                        contra_account=f"{form.subcontractor_name.data} {project_id}",
                        date=datetime.datetime.now().strftime("%d/%m/%Y"))
        db.session.add(new_cash)
        db.session.commit()
        new_subcontractor = SubContractor(name=form.subcontractor_name.data, opening_balance=0,
                                          description=form.description.data,
                                          cash_out=form.total.data,
                                          date=datetime.datetime.now().strftime("%d/%m/%Y"), project_id=project_id, cash_id=new_cash.id)

        db.session.add(new_subcontractor)
        db.session.commit()
        new_project_cost = ProjectCost(description=form.description.data, total=form.total.data,
                                       date=datetime.datetime.now().strftime("%d/%m/%Y"),
                                       project_id=project_id,
                                       cost_name=form.subcontractor_name.data.replace("مقاول ", ""),
                                       user_id=current_user.id, subcontractor_id=new_subcontractor.id)

        db.session.add(new_project_cost)
        db.session.commit()
        flash("Cash Out added successfully.")
        return redirect(url_for('insert_subcontractor_cash_out', project_id=project_id))
    return render_template("add_opening_balance_subcontractor.html", form=form, cash_out=True)



@app.route("/edit_subcontractor_item/<int:subcontractor_id>", methods=["GET", "POST"])
@login_required
@edit_subcontractor_account
def edit_subcontractor_item(subcontractor_id):
    requested_subcontractor_item = db.get_or_404(SubContractor, subcontractor_id)
    requested_cash_out = db.session.execute(db.select(Cash).where(Cash.id == requested_subcontractor_item.cash_id)).scalar()
    requested_project_cost = db.session.execute(db.select(ProjectCost).where(ProjectCost.subcontractor_id == requested_subcontractor_item.id)).scalar()
    if requested_subcontractor_item.opening_balance == 0:
        form = AddDataSubcontractors(subcontractor_name=requested_subcontractor_item.name,
                                     description=requested_subcontractor_item.description,
                                     total=requested_subcontractor_item.cash_out)
        form.subcontractor_name.choices = ["مقاول نجارة", "مقاول محارة", "مقاول كهرباء", "مقاول سباكة", "مقاول رخام",
                                           "مقاول سيراميك", "مقاول نقاشة", "مقاول حمام سباحة", "مقاول تكييفات","مقاول حدادة"]
        if form.validate_on_submit():
            requested_subcontractor_item.name = form.subcontractor_name.data
            requested_subcontractor_item.description = form.description.data
            requested_subcontractor_item.cash_out = form.total.data
            requested_project_cost.cost_name = form.subcontractor_name.data.replace("مقاول ", "")
            requested_project_cost.description = form.description.data
            requested_project_cost.total = form.total.data
            requested_cash_out.credit = form.total.data
            requested_cash_out.contra_account = f"{form.subcontractor_name.data}{requested_subcontractor_item.project_id}"
            db.session.commit()
            return redirect(url_for('display_subcontractor_accounts',
                                    project_id=requested_subcontractor_item.project_id))
        return render_template("add_opening_balance_subcontractor.html", form=form, editing_cash_out=True)
    elif requested_subcontractor_item.cash_out == 0:
        form = AddDataSubcontractors(subcontractor_name=requested_subcontractor_item.name,
                                     description=requested_subcontractor_item.description,
                                     total=requested_subcontractor_item.opening_balance)
        form.subcontractor_name.choices = ["مقاول نجارة", "مقاول محارة", "مقاول كهرباء", "مقاول سباكة", "مقاول رخام",
                                           "مقاول سيراميك", "مقاول نقاشة", "مقاول حمام سباحة", "مقاول حدادة", "مقاول تكييفات"]
        if form.validate_on_submit():
            requested_subcontractor_item.name = form.subcontractor_name.data
            requested_subcontractor_item.description = form.description.data
            requested_subcontractor_item.opening_balance = form.total.data
            db.session.commit()
            return redirect(url_for('display_subcontractor_accounts',
                                    project_id=requested_subcontractor_item.project_id))
        return render_template("add_opening_balance_subcontractor.html", form=form, editing_opening_balance=True)



@app.route("/all_custodes")
@login_required
@display_all_custodes
def all_custodes():
    custodes = db.session.execute(db.select(Custody)).scalars().all()
    return render_template("custodes.html", custodes=custodes)


@app.route("/add_custody_settlement/<int:user_id>", methods=["GET", "POST"])
@login_required
@add_custody_settlement
def add_custody_settlement(user_id):
    form = AddCustodySettlement()
    form.cost_name.choices = ["حمام سباحة", "نجارة", "سباكة", "سيراميك", "حدادة", "كهرباء", "نقاشة", "رخام","محارة","تكييفات","مصروفات نثرية"]
    projects = db.session.execute(db.select(Project)).scalars().all()
    project_list = []
    for project in projects:
        project_list.append(project.id)
        form.project_id.choices = project_list
    if form.validate_on_submit():
        new_project_cost = ProjectCost(description=form.description.data, total=form.total.data,
                                       date=datetime.datetime.now().strftime("%d/%m/%Y"),
                                       project_id=form.project_id.data, cost_name=form.cost_name.data, user_id=current_user.id)
        db.session.add(new_project_cost)
        db.session.commit()
        new_custody_settlement = CustodySettlement(description=form.description.data, debit=0, credit=form.total.data,
                                                   date=datetime.datetime.now().strftime("%d/%m/%Y"),
                                                   user_id=current_user.id, project_cost_id=new_project_cost.id, custody_id=user_id)
        db.session.add(new_custody_settlement)
        db.session.commit()
        total_debit = 0
        total_credit = 0
        custody_settlements = db.session.execute(db.select(CustodySettlement).where(CustodySettlement.user_id == current_user.id)).scalars().all()
        requested_custody = db.session.execute(db.select(Custody).where(Custody.user_id == current_user.id)).scalar()
        for custody_settlement in custody_settlements:
            total_debit += custody_settlement.debit
            total_credit += custody_settlement.credit
        balance = total_debit - total_credit
        requested_custody.debit = total_debit
        requested_custody.credit = total_credit
        requested_custody.balance = balance
        db.session.commit()
        flash("This Item Added Successfully")
        return redirect(url_for('add_custody_settlement', user_id=current_user.id))
    return render_template("add_custody_settlement.html", form=form, current_user=current_user, custody_settlement=True)



@app.route("/custody_cash_out/<int:custody_id>", methods=["GET", "POST"])
@login_required
@add_custody_cash_out
def custody_cash_out(custody_id):
    form = AddCustodyCashOut()
    if form.validate_on_submit():
        new_cash_out = Cash(description=form.description.data, debit=0, credit=form.total.data, balance=0,
                            date=datetime.datetime.now().strftime("%d/%m/%Y"), contra_account=f"Custody User{custody_id}")
        db.session.add(new_cash_out)
        db.session.commit()
        new_custody_settlement = CustodySettlement(description=form.description.data, debit=form.total.data,
                                                   credit=0, date=datetime.datetime.now().strftime("%d/%m/%Y"),
                                                   user_id=current_user.id, custody_id=custody_id,cash_id=new_cash_out.id)

        db.session.add(new_custody_settlement)
        db.session.commit()
        total_debit = 0
        total_credit = 0
        custody_settlements = db.session.execute(db.select(CustodySettlement).where(CustodySettlement.custody_id == custody_id)).scalars().all()
        requested_custody = db.session.execute(db.select(Custody).where(Custody.id == custody_id)).scalar()
        for custody_settlement in custody_settlements:
            total_debit += custody_settlement.debit
            total_credit += custody_settlement.credit
        balance = total_debit - total_credit
        requested_custody.debit = total_debit
        requested_custody.credit = total_credit
        requested_custody.balance = balance
        db.session.commit()
        flash("This Item Added Successfully")
        return redirect(url_for('custody_cash_out', custody_id=custody_id))
    return render_template("add_custody_settlement.html", form=form, add_cash_out=True)



@app.route("/display_custody/<int:custody_id>")
@login_required
@display_employee_custody
def display_user_custodes(custody_id):
    requested_custody = db.session.execute(db.select(Custody).where(Custody.id == custody_id)).scalar()
    custody_settlements = db.session.execute(db.select(CustodySettlement).where(CustodySettlement.custody_id == custody_id)).scalars().all()
    total_debit = 0
    total_credit = 0
    for custody_settlement in custody_settlements:
        total_debit += custody_settlement.debit
        total_credit += custody_settlement.credit
    requested_custody.debit = total_debit
    requested_custody.credit = total_credit
    requested_custody.balance = total_debit - total_credit
    db.session.commit()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(custody_settlements, page=page, css_framework='bootstrap5',
                            total=len(custody_settlements), search=search,
                            record_name='Custody Details')
    all_settlements_paginate = db.paginate(
        db.select(CustodySettlement).where(CustodySettlement.custody_id == requested_custody.id), page=page,
        per_page=10, error_out=False)
    return render_template("display_user_custodes.html", custody=requested_custody,custody_settlements=all_settlements_paginate, display=True, pagination=pagination)


@app.route("/display_project_cost/<int:project_id>")
@login_required
@display_project_cost
def display_project_cost(project_id):
    requested_project = db.get_or_404(Project, project_id)
    plumbing_project_costs = db.session.execute(db.select(ProjectCost).where(ProjectCost.cost_name == "سباكة", ProjectCost.project_id == project_id)).scalars().all()
    electric_project_costs = db.session.execute(db.select(ProjectCost).where(ProjectCost.cost_name == "كهرباء", ProjectCost.project_id == project_id)).scalars().all()
    blacksmith_project_costs = db.session.execute(db.select(ProjectCost).where(ProjectCost.cost_name == "حدادة", ProjectCost.project_id == project_id)).scalars().all()
    carpentry_project_costs = db.session.execute(db.select(ProjectCost).where(ProjectCost.cost_name == "نجارة", ProjectCost.project_id == project_id)).scalars().all()
    painting_project_costs = db.session.execute(db.select(ProjectCost).where(ProjectCost.cost_name == "نقاشة", ProjectCost.project_id == project_id)).scalars().all()
    ceramic_project_costs = db.session.execute(db.select(ProjectCost).where(ProjectCost.cost_name == "سيراميك", ProjectCost.project_id == project_id)).scalars().all()
    marble_project_costs = db.session.execute(db.select(ProjectCost).where(ProjectCost.cost_name == "رخام", ProjectCost.project_id == project_id)).scalars().all()
    swimming_pool_project_costs = db.session.execute(db.select(ProjectCost).where(ProjectCost.cost_name == "حمام سباحة",ProjectCost.project_id == project_id)).scalars().all()
    air_conditions_costs = db.session.execute(db.select(ProjectCost).where(ProjectCost.cost_name == "تكييفات", ProjectCost.project_id == project_id)).scalars().all()
    expenses_project_costs = db.session.execute(db.select(ProjectCost).where(ProjectCost.cost_name == "مصروفات نثرية", ProjectCost.project_id == project_id)).scalars().all()
    wall_cement_costs = db.session.execute(db.select(ProjectCost).where(ProjectCost.cost_name == "محارة", ProjectCost.project_id == project_id)).scalars().all()
    total_plumbing = 0
    total_electric = 0
    total_black_smith = 0
    total_carpentry = 0
    total_painting = 0
    total_ceramic = 0
    total_marble = 0
    total_air_condition = 0
    total_swimming_pool = 0
    total_expenses = 0
    total_wall_cement = 0
    for project_cost in plumbing_project_costs:
        total_plumbing += project_cost.total
    for project_cost in electric_project_costs:
        total_electric += project_cost.total
    for project_cost in blacksmith_project_costs:
        total_black_smith += project_cost.total
    for project_cost in carpentry_project_costs:
        total_carpentry += project_cost.total
    for project_cost in painting_project_costs:
        total_painting += project_cost.total
    for project_cost in ceramic_project_costs:
        total_ceramic += project_cost.total
    for project_cost in marble_project_costs:
        total_marble += project_cost.total
    for project_cost in swimming_pool_project_costs:
        total_swimming_pool += project_cost.total
    for project_cost in expenses_project_costs:
        total_expenses += project_cost.total
    for project_cost in air_conditions_costs:
        total_air_condition += project_cost.total
    for project_cost in wall_cement_costs:
        total_wall_cement += project_cost.total
    total_cost = total_plumbing + total_electric + total_black_smith + total_carpentry + total_ceramic + total_marble +total_swimming_pool + total_expenses + total_painting + total_air_condition + total_wall_cement
    try:
        percentage = math.ceil((total_cost / requested_project.total * 100) * 100) /100
    except TypeError:
        flash("Please Add Project Details to Display Project Cost")
        return redirect(url_for('add_project_details', project_id=project_id))
    except ZeroDivisionError:
        flash("Please Add Project Details to Display Project Cost")
        return redirect(url_for('add_project_details', project_id=project_id))
    profit = requested_project.total - total_cost
    return render_template("display_project_cost.html", project=requested_project,
                           total_plumbing=total_plumbing, total_electric=total_electric,
                           total_black_smith=total_black_smith, total_carpentry=total_carpentry,total_wall_cement=total_wall_cement,
                           total_ceramic=total_ceramic, total_marble=total_marble,total_air_condition=total_air_condition,
                           total_swimming_pool=total_swimming_pool, total_expenses=total_expenses, total_painting=total_painting,
                           total_cost=total_cost, profit=profit, percentage=percentage, plumbing=plumbing_project_costs, electric=electric_project_costs,
                           carpentry=carpentry_project_costs, ceramic=ceramic_project_costs,
                           marble=marble_project_costs, swimming_pool=swimming_pool_project_costs,
                           expenses=expenses_project_costs, black_smith=blacksmith_project_costs, painting=painting_project_costs, air_condition=air_conditions_costs, wall_cement=wall_cement_costs)



@app.route("/add_employee_details", methods=["GET", "POST"])
@login_required
@add_employee
def add_employee_details():
    form = EmployeeDetails()
    if form.validate_on_submit():
        requested_employee = db.session.execute(db.select(Employee).where(Employee.name == form.name.data)).scalar()
        if requested_employee:
            flash("This employee is already existed")
            return redirect(url_for('add_employee_details'))
        else:
            new_employee = Employee(name=form.name.data.title(), description=form.job_title.data,contact_number=form.contact_number.data, total_salary=0)
            db.session.add(new_employee)
            db.session.commit()
            flash("The employee has been added successfully")
            return redirect(url_for('add_employee_details'))
    return render_template("add_employee.html", form=form)



@app.route("/edit_employee_details/<int:employee_id>", methods=["GET", "POST"])
@login_required
@edit_employee_details
def edit_employee_details(employee_id):
    requested_employee = db.get_or_404(Employee, employee_id)
    form = EmployeeDetails(name=requested_employee.name, job_title=requested_employee.description,contact_number=requested_employee.contact_number)
    if form.validate_on_submit():
        requested_employee.name = form.name.data
        requested_employee.description = form.job_title.data
        requested_employee.contact_number = form.contact_number.data
        db.session.commit()
        flash("Employee Details Have Been Edited Successfully")
        return redirect(url_for('display_employee_salaries', employee_id=employee_id))
    return render_template("add_employee.html", form=form, edit=True)



@app.route("/edit_employee_salary/<int:salary_id>", methods=["GET", "POST"])
@login_required
@edit_salary
def edit_employee_salary(salary_id):
    requested_employee_salary = db.get_or_404(EmployeesSalary, salary_id)
    requested_cash_out = db.session.execute(db.select(Cash).where(Cash.id == requested_employee_salary.cash_id)).scalar()
    first_requested_employee = db.session.execute(
        db.select(Employee).where(Employee.id == requested_employee_salary.employee_id)).scalar()
    form = SalaryCashOut(employee_name=first_requested_employee.name, description=requested_employee_salary.description,salary=requested_employee_salary.salary)
    all_employees = db.session.execute(db.select(Employee)).scalars().all()
    list_of_employees = []
    for employee in all_employees:
        list_of_employees.append(employee.name)
    form.employee_name.choices = list_of_employees
    if form.validate_on_submit():
        requested_employee = db.session.execute(db.select(Employee).where(Employee.name == form.employee_name.data)).scalar()
        requested_employee_salary.employee_id = requested_employee.id
        requested_employee_salary.description = form.description.data
        requested_employee_salary.salary = form.salary.data
        requested_cash_out.description = form.description.data
        requested_cash_out.credit = form.salary.data
        requested_cash_out.contra_account = f"Salary {requested_employee.name}"
        db.session.commit()
        flash("Employee Details Have Been Edited Successfully")
        return redirect(url_for('display_employee_salaries', employee_id=requested_employee_salary.employee_id))
    return render_template("salary_cash_out.html", form=form, edit=True)



@app.route("/delete_employee_salary/<int:salary_id>")
@login_required
@delete_salary
def delete_employee_salary(salary_id):
    requested_employee_salary = db.get_or_404(EmployeesSalary, salary_id)
    file_name = requested_employee_salary.file_path
    try:
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                               secure_filename(file_name)))
    except FileNotFoundError:
        pass
    except TypeError:
        pass
    except PermissionError:
        pass

    requested_cash_out = db.session.execute(db.select(Cash).where(Cash.id == requested_employee_salary.cash_id)).scalar()
    requested_employee = db.session.execute(db.select(Employee).where(Employee.id == requested_employee_salary.employee_id)).scalar()
    employee_salaries = db.session.execute(db.select(EmployeesSalary).where(EmployeesSalary.employee_id == requested_employee_salary.employee_id)).scalars().all()
    db.session.delete(requested_employee_salary)
    db.session.delete(requested_cash_out)
    db.session.commit()
    total_salary = 0
    for salary in employee_salaries:
        total_salary += salary.salary
    requested_employee.total_salary = total_salary
    db.session.commit()
    flash("This Item Has Been Deleted")
    return redirect(url_for('display_employee_salaries', employee_id=requested_employee_salary.employee_id))



@app.route("/display_all_employees")
@login_required
@display_all_employees
def display_all_employees():
    employees = db.session.execute(db.select(Employee)).scalars().all()
    for employee in employees:
        total_salary = 0
        salaries = db.session.execute(db.select(EmployeesSalary).where(EmployeesSalary.employee_id == employee.id)).scalars().all()
        if salaries:
            for salary in salaries:
                total_salary += salary.salary
            employee.total_salary = total_salary
            db.session.commit()
    return render_template("display_all_employees.html", employees=employees)



@app.route("/search_employees", methods=["GET", "POST"])
@login_required
def search_employees():
    all_employees = db.session.execute(db.select(Employee)).scalars().all()
    if request.method == "POST":
        search_text = request.form["input_name"]
        search_format = "%{}%".format(search_text)
        if db.session.execute(
                db.select(Employee).where(Employee.name.like(search_format.title()))).scalars().all():
            results = db.session.execute(
                db.select(Employee).where(Employee.name.like(search_format.title()))).scalars()
            return render_template("display_all_employees.html", employees=results, search=True)
        elif db.session.execute(
                db.select(Employee).where(Employee.description.like(search_format))).scalars().all():
            results = db.session.execute(
                db.select(Employee).where(Employee.description.like(search_format))).scalars()
            return render_template("display_all_employees.html", employees=results, search=True)
        else:
            flash("There are no results found.")
            return render_template("display_all_employees.html", employees=all_employees, search=True)


@app.route("/search_salaries/<int:employee_id>", methods=["GET", "POST"])
@login_required
@display_employee_salary
def search_salaries(employee_id):
    requested_employee = db.get_or_404(Employee, employee_id)
    if request.method == "POST":
        search_text = request.form["input_name"]
        search_format = "%{}%".format(search_text)
        if db.session.execute(db.select(EmployeesSalary).where(EmployeesSalary.description.like(search_format), EmployeesSalary.employee_id == employee_id)).scalars().all():
            results = db.session.execute(db.select(EmployeesSalary).where(EmployeesSalary.description.like(search_format), EmployeesSalary.employee_id == employee_id)).scalars()
            return render_template("display_employee_salaries.html", employee=requested_employee, salaries=results, search=True, year=year)
        elif db.session.execute(db.select(EmployeesSalary).where(EmployeesSalary.date.like(search_format), EmployeesSalary.employee_id == employee_id)).scalars().all():
            results = db.session.execute(db.select(EmployeesSalary).where(EmployeesSalary.date.like(search_format), EmployeesSalary.employee_id == employee_id)).scalars()
            return render_template("display_employee_salaries.html", employee=requested_employee, salaries=results, search=True, year=year)
        else:
            flash("There are no results found.")
            return render_template("display_employee_salaries.html", employee=requested_employee, year=year)


@app.route("/salary_cash_out", methods=["GET", "POST"])
@login_required
@salary_cash_out
def salary_cash_out():
    form = SalaryCashOut()
    employees = db.session.execute(db.select(Employee)).scalars().all()
    list_of_employees = []
    for employee in employees:
        list_of_employees.append(employee.name)
    form.employee_name.choices = list_of_employees
    if form.validate_on_submit():
        requested_employee = db.session.execute(db.select(Employee).where(Employee.name == form.employee_name.data)).scalar()
        new_cash_out = Cash(description=form.description.data, debit=0, credit=form.salary.data, balance=0,
                            date=datetime.datetime.now().strftime("%d/%m/%Y"),
                            contra_account=f"Salary {form.employee_name.data}")
        db.session.add(new_cash_out)
        db.session.commit()
        new_salary_cash_out = EmployeesSalary(description=form.description.data, salary=form.salary.data,
                                              date=datetime.datetime.now().strftime("%d/%m/%Y"),
                                              employee_id=requested_employee.id, cash_id=new_cash_out.id)
        db.session.add(new_salary_cash_out)
        db.session.commit()
        employee_salaries_details = db.session.execute(db.select(EmployeesSalary).where(EmployeesSalary.employee_id == requested_employee.id)).scalars().all()
        total_salary = 0
        for employee_salaries_detail in employee_salaries_details:
            total_salary += employee_salaries_detail.salary
        requested_employee.total_salary = total_salary
        db.session.commit()
        flash("salary cash out has been added successfully")
        return redirect(url_for('salary_cash_out'))
    return render_template("salary_cash_out.html", form=form)


@login_required
@display_employee_salary
@app.route("/display_employee_salaries/<int:employee_id>")
def display_employee_salaries(employee_id):
    requested_employee = db.session.execute(db.select(Employee).where(Employee.id == employee_id)).scalar()
    all_salaries = db.session.execute(db.select(EmployeesSalary).where(EmployeesSalary.employee_id == requested_employee.id)).scalars().all()
    total_salary = 0
    for salary in all_salaries:
        total_salary += salary.salary
    requested_employee.total_salary = total_salary
    db.session.commit()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(all_salaries, page=page, css_framework='bootstrap5',
                            total=len(all_salaries), search=search,
                            record_name='Item Movements')
    all_salary_paginate = db.paginate(
        db.select(EmployeesSalary).where(EmployeesSalary.employee_id == requested_employee.id), page=page,
        per_page=10, error_out=False)
    return render_template("display_employee_salaries.html", employee=requested_employee, salaries=all_salary_paginate, pagination=pagination)


@app.route("/add_expense", methods=["GET", "POST"])
@login_required
@add_expense
def add_expense():
    form = AddExpense()
    if form.validate_on_submit():
        requested_expense = db.session.execute(db.select(Expense).where(Expense.name == form.expense_name.data)).scalar()
        if requested_expense:
            flash("That expense is already existed")
            return redirect(url_for('add_expense'))
        else:
            new_expense = Expense(name=form.expense_name.data.title(),  total=0)
            db.session.add(new_expense)
            db.session.commit()
            flash("The expense has been added successfully")
            return redirect(url_for('add_expense'))
    return render_template("add_expense.html", form=form)



@app.route("/display_all_expenses")
@login_required
@display_all_expenses
def display_all_expenses():
    expenses = db.session.execute(db.select(Expense)).scalars().all()
    for expense in expenses:
        total_expense = 0
        expense_details = db.session.execute(db.select(ExpenseDetail).where(ExpenseDetail.expense_id == expense.id)).scalars().all()
        if expense_details:
            for expense_detail in expense_details:
                total_expense += expense_detail.total
            expense.total = total_expense
            db.session.commit()
    return render_template("display_all_expenses.html", expenses=expenses)



@app.route("/expense_cash_out", methods=["GET", "POST"])
@login_required
@expense_cash_out
def expense_cash_out():
    form = ExpenseCashOut()
    expenses = db.session.execute(db.select(Expense)).scalars().all()
    list_of_expenses = []
    for expense in expenses:
        list_of_expenses.append(expense.name)
    form.expense_name.choices = list_of_expenses
    if form.validate_on_submit():
        requested_expense = db.session.execute(db.select(Expense).where(Expense.name == form.expense_name.data)).scalar()
        new_cash_out = Cash(description=form.description.data, debit=0, credit=form.total.data, balance=0,
                            date=datetime.datetime.now().strftime("%d/%m/%Y"),
                            contra_account=f"Expense {form.expense_name.data}")
        db.session.add(new_cash_out)
        db.session.commit()
        new_expense_cash_out = ExpenseDetail(description=form.description.data, total=form.total.data,
                                              date=datetime.datetime.now().strftime("%d/%m/%Y"),
                                              expense_id=requested_expense.id, cash_id=new_cash_out.id)
        db.session.add(new_expense_cash_out)
        db.session.commit()
        expense_details = db.session.execute(db.select(ExpenseDetail).where(ExpenseDetail.expense_id == requested_expense.id)).scalars().all()
        total_expense = 0
        for expense_detail in expense_details:
            total_expense += expense_detail.total
        requested_expense.total_salary = total_expense
        db.session.commit()
        flash("Expense cash out has been added successfully")
        return redirect(url_for('expense_cash_out'))
    return render_template("expense_cash_out.html", form=form)



@app.route("/display_expense_details/<int:expense_id>")
@login_required
@display_expense_details
def display_expense_details(expense_id):
    requested_expense = db.session.execute(db.select(Expense).where(Expense.id == expense_id)).scalar()
    all_details = db.session.execute(db.select(ExpenseDetail).where(ExpenseDetail.expense_id == requested_expense.id)).scalars().all()
    total_expense = 0
    for detail in all_details:
        total_expense += detail.total
    requested_expense.total = total_expense
    db.session.commit()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(all_details, page=page, css_framework='bootstrap5',
                            total=len(all_details), search=search,
                            record_name='Expense Details')
    all_details_paginate = db.paginate(
        db.select(ExpenseDetail).where(ExpenseDetail.expense_id == requested_expense.id), page=page,
        per_page=10, error_out=False)
    return render_template("display_expense_details.html", expense=requested_expense, expense_details=all_details_paginate, pagination=pagination)



@app.route("/edit_expense/<int:expense_id>", methods=["GET", "POST"])
@login_required
@edit_expense
def edit_expense(expense_id):
    requested_expense = db.get_or_404(Expense, expense_id)
    form = AddExpense(expense_name=requested_expense.name )
    if form.validate_on_submit():
        requested_expense.name = form.expense_name.data
        db.session.commit()
        flash("Expense Has Been Edited Successfully")
        return redirect(url_for('display_expense_details', expense_id=expense_id))
    return render_template("add_expense.html", form=form, edit=True)



@app.route("/edit_expense_detail/<int:expense_detail_id>", methods=["GET", "POST"])
@login_required
@edit_expense_cash_out
def edit_expense_detail(expense_detail_id):
    requested_expense_detail = db.get_or_404(ExpenseDetail, expense_detail_id)
    requested_cash_out = db.session.execute(db.select(Cash).where(Cash.id == requested_expense_detail.cash_id)).scalar()
    first_requested_expense = db.session.execute(db.select(Expense).where(Expense.id == requested_expense_detail.expense_id)).scalar()
    form = ExpenseCashOut(expense_name=first_requested_expense.name, description=requested_expense_detail.description, total=requested_expense_detail.total)
    all_expenses = db.session.execute(db.select(Expense)).scalars().all()
    list_of_expenses = []
    for expense in all_expenses:
        list_of_expenses.append(expense.name)
    form.expense_name.choices = list_of_expenses
    if form.validate_on_submit():
        requested_expense = db.session.execute(db.select(Expense).where(Expense.name == form.expense_name.data)).scalar()
        requested_expense_detail.expense_id = requested_expense.id
        requested_expense_detail.description = form.description.data
        requested_expense_detail.total = form.total.data
        requested_cash_out.description = form.description.data
        requested_cash_out.credit = form.total.data
        requested_cash_out.contra_account = f"Salary {requested_expense.name}"
        db.session.commit()
        flash("Expense Details Have Been Edited Successfully")
        return redirect(url_for('display_expense_details', expense_id=requested_expense.id))
    return render_template("expense_cash_out.html", form=form, edit=True)



@app.route("/delete_expense_detail/<int:expense_detail_id>")
@login_required
@delete_expense_cash_out
def delete_expense_detail(expense_detail_id):
    requested_expense_detail = db.get_or_404(ExpenseDetail, expense_detail_id)
    file_name = requested_expense_detail.file_path
    try:
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                               secure_filename(file_name)))
    except FileNotFoundError:
        pass
    except TypeError:
        pass
    except PermissionError:
        pass
    requested_cash_out = db.session.execute(db.select(Cash).where(Cash.id == requested_expense_detail.cash_id)).scalar()
    requested_expense = db.session.execute(db.select(Expense).where(Expense.id == requested_expense_detail.expense_id)).scalar()
    expense_details = db.session.execute(db.select(ExpenseDetail).where(ExpenseDetail.expense_id == requested_expense.id)).scalars().all()
    db.session.delete(requested_expense_detail)
    db.session.delete(requested_cash_out)
    db.session.commit()
    total_expense = 0
    for detail in expense_details:
        total_expense += detail.total
    requested_expense.total = total_expense
    db.session.commit()
    flash("This Item Has Been Deleted")
    return redirect(url_for('display_expense_details', expense_id=requested_expense.id))



@app.route("/search_expense_details/<int:expense_id>", methods=["GET", "POST"])
@login_required
def search_expense_details(expense_id):
    requested_expense = db.get_or_404(Expense, expense_id)
    if request.method == "POST":
        search_text = request.form["input_name"]
        search_format = "%{}%".format(search_text)
        if db.session.execute(db.select(ExpenseDetail).where(ExpenseDetail.description.like(search_format), ExpenseDetail.expense_id == expense_id)).scalars().all():
            results = db.session.execute(db.select(ExpenseDetail).where(ExpenseDetail.description.like(search_format), ExpenseDetail.expense_id == expense_id)).scalars()
            return render_template("display_expense_details.html", expense=requested_expense, expense_details=results, search=True, year=year)
        elif db.session.execute(db.select(ExpenseDetail).where(ExpenseDetail.date.like(search_format),ExpenseDetail.expense_id == expense_id)).scalars().all():
            results = db.session.execute(db.select(ExpenseDetail).where(ExpenseDetail.date.like(search_format), ExpenseDetail.expense_id == expense_id)).scalars()
            return render_template("display_expense_details.html", expense=requested_expense, expense_details=results, search=True, year=year)
        else:
            flash("There are no results found.")
            return render_template("display_expense_details.html", expense=requested_expense, year=year, search=True)



@app.route("/edit_custody_employee_name/<int:custody_id>", methods=["GET", "POST"])
@login_required
@edit_employee_name
def edit_custody_employee_name(custody_id):
    requested_custody = db.get_or_404(Custody, custody_id)
    form = EditCustodyName(name=requested_custody.name)
    if form.validate_on_submit():
        requested_custody.name = form.name.data
        db.session.commit()
        return redirect(url_for('all_custodes'))
    return render_template('edit_custody_employee_name.html', form=form)


@app.route("/edit_custody_cash_out/<int:custody_settlement_id>", methods=["GET", "POST"])
@login_required
@edit_custody_cash_out
def edit_custody_cash_out(custody_settlement_id):
    requested_custody_settlement = db.get_or_404(CustodySettlement, custody_settlement_id)
    requested_cash_out = db.session.execute(db.select(Cash).where(Cash.id == requested_custody_settlement.cash_id)).scalar()
    form = AddCustodyCashOut(description=requested_custody_settlement.description, total=requested_custody_settlement.debit)
    if form.validate_on_submit():
        requested_custody_settlement.description = form.description.data
        requested_custody_settlement.debit = form.total.data
        requested_cash_out.description = form.description.data
        requested_cash_out.credit = form.total.data
        db.session.commit()
        total_debit = 0
        total_credit = 0
        custody_settlements = db.session.execute(db.select(CustodySettlement).where(CustodySettlement.custody_id == requested_custody_settlement.custody_id)).scalars().all()
        requested_custody = db.session.execute(db.select(Custody).where(Custody.id == requested_custody_settlement.custody_id)).scalar()
        for custody_settlement in custody_settlements:
            total_debit += custody_settlement.debit
            total_credit += custody_settlement.credit
        balance = total_debit - total_credit
        requested_custody.debit = total_debit
        requested_custody.credit = total_credit
        requested_custody.balance = balance
        db.session.commit()
        flash("This Item Edited Successfully")
        return redirect(url_for('display_user_custodes', custody_id=requested_custody.id))
    return render_template("add_custody_settlement.html", form=form, edit_cash_out=True)


@app.route("/edit_custody_settlement/<int:custody_settlement_id>", methods=["GET", "POST"])
@login_required
@edit_custody_settlement
def edit_custody_settlement(custody_settlement_id):
    requested_custody_settlement = db.get_or_404(CustodySettlement, custody_settlement_id)
    requested_project_cost = db.session.execute(db.select(ProjectCost).where(ProjectCost.id == requested_custody_settlement.project_cost_id)).scalar()
    form = AddCustodySettlement(description=requested_custody_settlement.description, cost_name=requested_project_cost.cost_name, total=requested_custody_settlement.credit)
    form.cost_name.choices = ["حمام سباحة", "نجارة", "سباكة", "سيراميك", "حدادة", "كهرباء", "نقاشة", "رخام",
                              "مصروفات نثرية"]
    projects = db.session.execute(db.select(Project)).scalars().all()
    project_list = []
    for project in projects:
        project_list.append(project.id)
        form.project_id.choices = project_list
    if form.validate_on_submit():
        requested_project_cost.cost_name = form.cost_name.data
        requested_project_cost.description = form.description.data
        requested_project_cost.total = form.total.data
        requested_project_cost.user_id = current_user.id
        requested_custody_settlement.description = form.description.data
        requested_custody_settlement.credit = form.total.data
        requested_custody_settlement.user_id = current_user.id
        db.session.commit()
        total_debit = 0
        total_credit = 0
        custody_settlements = db.session.execute(db.select(CustodySettlement).where(CustodySettlement.user_id == current_user.id)).scalars().all()
        requested_custody = db.session.execute(db.select(Custody).where(Custody.id == requested_custody_settlement.custody_id)).scalar()
        for custody_settlement in custody_settlements:
            total_debit += custody_settlement.debit
            total_credit += custody_settlement.credit
        balance = total_debit - total_credit
        requested_custody.debit = total_debit
        requested_custody.credit = total_credit
        requested_custody.balance = balance
        db.session.commit()
        flash("This Item Edited Successfully")
        return redirect(url_for('display_user_custodes', custody_id=requested_custody.id))
    return render_template("add_custody_settlement.html", form=form,  edit_custody_settlement=True)



@app.route("/delete_custody_cash_out/<int:custody_settlement_id>")
@login_required
@delete_custody_cash_out
def delete_custody_cash_out(custody_settlement_id):
    requested_custody_cash_out = db.get_or_404(CustodySettlement, custody_settlement_id)
    file_name = requested_custody_cash_out.file_path
    try:
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                               secure_filename(file_name)))
    except FileNotFoundError:
        pass
    except TypeError:
        pass
    except PermissionError:
        pass
    requested_custody = db.session.execute(db.select(Custody).where(Custody.id == requested_custody_cash_out.custody_id)).scalar()
    requested_cash_out = db.session.execute(db.select(Cash).where(Cash.id == requested_custody_cash_out.cash_id)).scalar()
    db.session.delete(requested_custody_cash_out)
    db.session.delete(requested_cash_out)
    db.session.commit()
    flash("This item has been deleted.")
    return redirect(url_for('display_user_custodes', custody_id=requested_custody_cash_out.custody_id))



@app.route("/delete_custody_settlement/<int:custody_settlement_id>")
@login_required
@delete_custody_settlement
def delete_custody_settlement(custody_settlement_id):
    requested_custody_settlement = db.get_or_404(CustodySettlement, custody_settlement_id)
    file_name = requested_custody_settlement.file_path
    try:
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                               secure_filename(file_name)))
    except FileNotFoundError:
        pass
    except TypeError:
        pass
    except PermissionError:
        pass
    requested_project_cost = db.session.execute(db.select(ProjectCost).where(ProjectCost.id == requested_custody_settlement.project_cost_id)).scalar()
    db.session.delete(requested_custody_settlement)
    db.session.delete(requested_project_cost)
    db.session.commit()
    flash("This item has been deleted.")
    return redirect(url_for('display_user_custodes', custody_id=requested_custody_settlement.custody_id))


@app.route("/add-inventory-item", methods=["GET", "POST"])
@login_required
@add_item
def add_inventory_item():
    form = AddInventoryItem()
    if form.validate_on_submit():
        result = db.session.execute(
            db.select(InventoryItem).where(InventoryItem.name == form.item_name.data)).scalar()
        if result:
            flash("This Item Is Already Existed")
            return redirect(url_for('add_inventory_item'))
        new_inventory_item = InventoryItem(name=form.item_name.data, quantity_in=0, unit_price_average=0,total_in=0,
                                           quantity_out=0, total_out=0, quantity_balance=0, total_balance=0)
        db.session.add(new_inventory_item)
        db.session.commit()
        flash("This item has been added successfully")
        return redirect(url_for('add_inventory_item'))
    return render_template("add_inventory_item.html", form=form, year=year, add_inventory_item=True)



@app.route("/display_all_items")
@login_required
@display_all_items
def display_all_items():
    all_items = db.session.execute(db.select(InventoryItem)).scalars().all()
    return render_template("display_all_items.html", year=year, items=all_items)


@app.route("/edit_item_name/<int:item_id>", methods=["GET", "POST"])
@login_required
@edit_item
def edit_item_name(item_id):
    requested_inventory_item = db.get_or_404(InventoryItem, item_id)
    form = AddInventoryItem(item_name=requested_inventory_item.name)
    if form.validate_on_submit():
        requested_inventory_item.name = form.item_name.data
        db.session.commit()
        flash("The item has been edited successfully")
        return redirect(url_for("display_all_items"))
    return render_template("add_inventory_item.html", form=form, edit_item_name=True)



@app.route("/search_item_name", methods=["GET", "POST"])
@login_required
def search_item_name():
    all_item = db.session.execute(db.select(InventoryItem))
    if request.method == "POST":
        search_text = request.form["input_name"]
        search_format = "%{}%".format(search_text)
        if db.session.execute(
                db.select(InventoryItem).where(InventoryItem.name.like(search_format.title()))).scalars().all():
            result = db.session.execute(
                db.select(InventoryItem).where(InventoryItem.name.like(search_format.title()))).scalars()
            return render_template("display_all_items.html", items=result, year=year, search=True)
        else:
            flash("There are no results found")
            return redirect("display_all_items")


@app.route("/add_item_opening_balance/<int:item_id>", methods=["GET", "POST"])
def add_item_opening_balance(item_id):
    form = ImportInventoryMovement()
    requested_inventory_item = db.get_or_404(InventoryItem, item_id)
    if form.validate_on_submit():
        new_opening_balance = InventoryMovement(description=form.description.data, quantity_in=form.quantity.data,unit_price_in=form.unit_price.data,total_in=form.quantity.data * form.unit_price.data,quantity_out=0, unit_price_out=0, total_out=0, inventory_item_id=item_id, date=datetime.datetime.now().strftime("%d/%m/%Y"))
        db.session.add(new_opening_balance)
        db.session.commit()
        item_inventory_movements = db.session.execute(db.select(InventoryMovement).where(
            InventoryMovement.inventory_item_id == item_id)).scalars().all()
        total_quantity_in = 0
        total_total_in = 0
        for item_inventory_movement in item_inventory_movements:
            total_quantity_in += item_inventory_movement.quantity_in
            total_total_in += item_inventory_movement.total_in
        requested_inventory_item.quantity_in = total_quantity_in
        requested_inventory_item.total_in = total_total_in
        requested_inventory_item.quantity_balance = total_quantity_in - requested_inventory_item.quantity_out
        requested_inventory_item.total_balance = total_total_in - requested_inventory_item.total_out
        requested_inventory_item.unit_price_average = math.ceil(
            (total_total_in - requested_inventory_item.total_out) / (
                        total_quantity_in - requested_inventory_item.quantity_out))
        db.session.commit()
        flash("Item Opening Balance Has Been Added Successfully.")
        return redirect(url_for('import_inventory_item', inventory_item_id=item_id))
    return render_template("import_inventory_item.html", form=form, item=requested_inventory_item, opening_balance=True)



@app.route("/import_inventory_item/<int:inventory_item_id>", methods=["GET", "POST"])
@login_required
@import_item
def import_inventory_item(inventory_item_id):
    requested_inventory_item = db.get_or_404(InventoryItem, inventory_item_id)
    form = ImportInventoryMovement()
    if form.validate_on_submit():
        new_cash_out = Cash(description=form.description.data, debit=0, credit=form.quantity.data * form.unit_price.data, balance=0,
                            date=datetime.datetime.now().strftime("%d/%m/%Y"),
                            contra_account=f"Inventory {requested_inventory_item.name}")
        db.session.add(new_cash_out)
        db.session.commit()
        new_inventory_movement = InventoryMovement(description=form.description.data,quantity_in=form.quantity.data,
                                                   unit_price_in=form.unit_price.data,
                                                   total_in=form.quantity.data * form.unit_price.data,
                                                   quantity_out=0, unit_price_out=0, total_out=0,
                                                   inventory_item_id=inventory_item_id, date=datetime.datetime.now().strftime("%d/%m/%Y"), cash_id=new_cash_out.id)
        db.session.add(new_inventory_movement)
        db.session.commit()
        item_inventory_movements = db.session.execute(db.select(InventoryMovement).where(InventoryMovement.inventory_item_id == inventory_item_id)).scalars().all()
        total_quantity_in = 0
        total_total_in = 0
        for item_inventory_movement in item_inventory_movements:
            total_quantity_in += item_inventory_movement.quantity_in
            total_total_in += item_inventory_movement.total_in
        requested_inventory_item.quantity_in = total_quantity_in
        requested_inventory_item.total_in = total_total_in
        requested_inventory_item.quantity_balance = total_quantity_in - requested_inventory_item.quantity_out
        requested_inventory_item.total_balance = total_total_in - requested_inventory_item.total_out
        requested_inventory_item.unit_price_average = math.ceil((total_total_in - requested_inventory_item.total_out)/ (total_quantity_in - requested_inventory_item.quantity_out))
        db.session.commit()
        flash("This Item Has Been Imported Successfully")
        return redirect(url_for('import_inventory_item',inventory_item_id=inventory_item_id))
    return render_template("import_inventory_item.html",form=form, item=requested_inventory_item, import_item=True)



@app.route("/export_inventory_item/<int:inventory_item_id>", methods=["GET", "POST"])
@login_required
@export_item
def export_inventory_item(inventory_item_id):
    requested_inventory_item = db.get_or_404(InventoryItem, inventory_item_id)
    form = ExportInventoryMovement(unit_price=requested_inventory_item.unit_price_average)
    form.cost_name.choices = ["حمام سباحة", "نجارة", "سباكة", "سيراميك", "حدادة", "كهرباء", "نقاشة", "رخام",
                              "مصروفات نثرية"]
    projects = db.session.execute(db.select(Project)).scalars().all()
    project_list = []
    for project in projects:
        project_list.append(project.id)
        form.project_id.choices = project_list
    if form.validate_on_submit():
        if form.quantity.data > requested_inventory_item.quantity_balance:
            flash("The balance of exporting goods is greater than the stock balance")
            return redirect(url_for('export_inventory_item',inventory_item_id=inventory_item_id))
        new_project_cost = ProjectCost(description=form.description.data, total=form.unit_price.data * form.quantity.data,
                                       date=datetime.datetime.now().strftime("%d/%m/%Y"),
                                       project_id=form.project_id.data, cost_name=form.cost_name.data,
                                       user_id=current_user.id)
        db.session.add(new_project_cost)
        db.session.commit()
        new_inventory_movement = InventoryMovement(description=form.description.data, quantity_in=0, unit_price_in=0,
                                                   total_in=0, quantity_out=form.quantity.data,
                                                   unit_price_out=form.unit_price.data,
                                                   total_out=form.quantity.data * form.unit_price.data,
                                                   project_id=form.project_id.data, inventory_item_id=inventory_item_id,
                                                   date=datetime.datetime.now().strftime("%d/%m/%Y"),
                                                   project_cost_id=new_project_cost.id)
        db.session.add(new_inventory_movement)
        db.session.commit()
        item_inventory_movements = db.session.execute(db.select(InventoryMovement).where(
            InventoryMovement.inventory_item_id == inventory_item_id)).scalars().all()
        total_quantity_out = 0
        total_total_out = 0
        for item_inventory_movement in item_inventory_movements:
            total_quantity_out += item_inventory_movement.quantity_out
            total_total_out += item_inventory_movement.total_out
        requested_inventory_item.quantity_out = total_quantity_out
        requested_inventory_item.total_out = total_total_out
        requested_inventory_item.quantity_balance = requested_inventory_item.quantity_in - total_quantity_out
        requested_inventory_item.total_balance = requested_inventory_item.total_in - total_total_out
        db.session.commit()
        if requested_inventory_item.total_in - total_total_out == 0:
            requested_inventory_item.unit_price_average = 0
            db.session.commit()
            flash("This Item Has Been Exported Successfully")
            return redirect(url_for('import_inventory_item', inventory_item_id=inventory_item_id))
        elif requested_inventory_item.total_in - total_total_out > 0 :
            requested_inventory_item.unit_price_average = math.ceil((requested_inventory_item.total_in - total_total_out) / (
                    requested_inventory_item.quantity_in - total_quantity_out))
            db.session.commit()
            flash("This Item Has Been Exported Successfully")
            return redirect(url_for('import_inventory_item', inventory_item_id=inventory_item_id))
    return render_template("import_inventory_item.html", form=form, item=requested_inventory_item, export=True)



@app.route("/display_item_movements/<int:inventory_item_id>")
@login_required
@display_item_movements
def display_item_movements(inventory_item_id):
    requested_item = db.get_or_404(InventoryItem, inventory_item_id)
    item_inventory_movements = db.session.execute(db.select(InventoryMovement).where(
        InventoryMovement.inventory_item_id == requested_item.id)).scalars().all()
    total_quantity_in = 0
    total_total_in = 0
    total_quantity_out = 0
    total_total_out = 0
    for item_inventory_movement in item_inventory_movements:
        total_quantity_in += item_inventory_movement.quantity_in
        total_total_in += item_inventory_movement.total_in
        total_quantity_out += item_inventory_movement.quantity_out
        total_total_out += item_inventory_movement.total_out
    requested_item.quantity_in = total_quantity_in
    requested_item.total_in = total_total_in
    requested_item.quantity_out = total_quantity_out
    requested_item.total_out = total_total_out
    requested_item.quantity_balance = total_quantity_in - total_quantity_out
    requested_item.total_balance = total_total_in - total_total_out
    db.session.commit()
    if total_total_in - total_total_out > 0:
        requested_item.unit_price_average = math.ceil(
            (total_total_in - total_total_out) / (
                    total_quantity_in - total_quantity_out))
        db.session.commit()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(item_inventory_movements, page=page, css_framework='bootstrap5', total=len(item_inventory_movements), search=search,
                            record_name='Item Movements')
    all_movements_paginate = db.paginate(db.select(InventoryMovement).where(InventoryMovement.inventory_item_id == requested_item.id), page=page, per_page=10, error_out=False)
    return render_template("display_item_movements.html", item=requested_item, item_movements=all_movements_paginate, pagination=pagination)



@app.route("/edit_item_movements/<int:item_movement_id>", methods=["GET", "POST"])
@login_required
@edit_item_movement
def edit_item_movements(item_movement_id):
    requested_item_movement = db.get_or_404(InventoryMovement, item_movement_id)
    requested_cash_out = db.session.execute(db.select(Cash).where(Cash.id == requested_item_movement.cash_id)).scalar()
    requested_item = db.session.execute(db.select(InventoryItem).where(InventoryItem.id == requested_item_movement.inventory_item_id)).scalar()
    if requested_item_movement.total_in > 0:
        form = ImportInventoryMovement(description=requested_item_movement.description,
                                       quantity=requested_item_movement.quantity_in,
                                       unit_price=requested_item_movement.unit_price_in)
        if form.validate_on_submit():
            if form.quantity.data < requested_item.quantity_balance:
                flash("Quantity in less than  stock quantity balance please input instead quantity")
                return redirect(url_for('edit_item_movements', item_movement_id=item_movement_id))

            requested_item_movement.description = form.description.data
            requested_item_movement.quantity_in = form.quantity.data
            requested_item_movement.unit_price_in = form.unit_price.data
            requested_item_movement.total_in = form.quantity.data * form.unit_price.data
            requested_cash_out.description = form.description.data
            requested_cash_out.credit = form.quantity.data * form.unit_price.data
            db.session.commit()
            flash("This Item Has Been Edited Successfully")
            return redirect(url_for('display_item_movements', inventory_item_id=requested_item.id))
        return render_template("import_inventory_item.html", form=form, edit_import=True, item=requested_item)
    elif requested_item_movement.total_out > 0:
        requested_cost = db.session.execute(db.select(ProjectCost).where(ProjectCost.id == requested_item_movement.project_cost_id)).scalar()
        form = ExportInventoryMovement(project_id=requested_item_movement.project_id, cost_name=requested_cost.cost_name,
                                       description=requested_item_movement.description,
                                       quantity=requested_item_movement.quantity_out,
                                       unit_price=requested_item.unit_price_average)
        form.cost_name.choices = ["حمام سباحة", "نجارة", "سباكة", "سيراميك", "حدادة", "كهرباء", "نقاشة", "رخام","تكييفات","محارة"
                                  "مصروفات نثرية"]
        projects = db.session.execute(db.select(Project)).scalars().all()
        project_list = []
        for project in projects:
            project_list.append(project.id)
            form.project_id.choices = project_list
        if form.validate_on_submit():
            if form.quantity.data > requested_item.quantity_balance + requested_item_movement.quantity_out:
                flash("The balance of exporting goods is greater than the stock balance")
                return redirect(url_for('edit_item_movements', item_movement_id=item_movement_id))
            requested_cost.description = form.description.data
            requested_cost.total = form.quantity.data * form.unit_price.data
            requested_cost.cost_name = form.cost_name.data
            requested_cost.project_id = form.project_id.data
            requested_item_movement.description = form.description.data
            requested_item_movement.quantity_out = form.quantity.data
            requested_item_movement.unit_price_out = form.unit_price.data
            requested_item_movement.total_out = form.quantity.data * form.unit_price.data
            requested_item_movement.project_id = form.project_id.data
            db.session.commit()
            flash("This Item Has Been Edited Successfully")
            return redirect(url_for('display_item_movements', inventory_item_id=requested_item.id))
        return render_template("import_inventory_item.html", form=form, edit_export=True, item=requested_item)




@app.route("/delete_item_movements/<int:item_movement_id>")
@login_required
@delete_item_movement
def delete_item_movements(item_movement_id):
    requested_item_movement = db.get_or_404(InventoryMovement, item_movement_id)
    requested_cash_out = db.session.execute(db.select(Cash).where(Cash.id == requested_item_movement.cash_id)).scalar()
    requested_item = db.session.execute(db.select(InventoryItem).where(InventoryItem.id == requested_item_movement.inventory_item_id)).scalar()
    requested_project_cost = db.session.execute(db.select(ProjectCost).where(ProjectCost.id == requested_item_movement.project_cost_id)).scalar()
    if requested_item_movement.quantity_in > requested_item.quantity_balance:
        flash("Item movement quantity is greater than item quantity balance")
        return redirect(url_for('display_item_movements', inventory_item_id=requested_item.id))
    elif requested_item_movement.total_in > 0:
        file_name = requested_item_movement.file_path
        try:
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                   secure_filename(file_name)))
        except FileNotFoundError:
            pass
        except TypeError:
            pass
        except PermissionError:
            pass
        db.session.delete(requested_item_movement)
        db.session.delete(requested_cash_out)
        db.session.commit()
        flash("This Item Has Been Deleted Successfully")
        return redirect(url_for('display_item_movements', inventory_item_id=requested_item.id))
    else:
        file_name = requested_item_movement.file_path
        try:
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                   secure_filename(file_name)))
        except FileNotFoundError:
            pass
        except TypeError:
            pass
        except PermissionError:
            pass
        db.session.delete(requested_item_movement)
        db.session.delete(requested_project_cost)
        db.session.commit()
        flash("This Item Has Been Deleted Successfully")
        return redirect(url_for('display_item_movements', inventory_item_id=requested_item.id))



@app.route("/search_item_movements/<int:inventory_item_id>", methods=["GET", "POST"])
@login_required
def search_item_movements(inventory_item_id):
    requested_item = db.get_or_404(InventoryItem, inventory_item_id)
    all_item_movements = db.session.execute(db.select(InventoryMovement).where(InventoryMovement.inventory_item_id == requested_item.id)).scalars().all()
    if request.method == "POST":
        search_text = request.form["input_name"]
        search_format = "%{}%".format(search_text)
        if db.session.execute(
                db.select(InventoryMovement).where(InventoryMovement.description.like(search_format.title()), InventoryMovement.inventory_item_id == requested_item.id)).scalars().all():
            results = db.session.execute(
                db.select(InventoryMovement).where(InventoryMovement.description.like(search_format.title()), InventoryMovement.inventory_item_id == requested_item.id)).scalars()
            return render_template("display_item_movements.html", item=requested_item, search=True, all_movements=results)
        elif db.session.execute(
                db.select(InventoryMovement).where(InventoryMovement.date.like(search_format.title()), InventoryMovement.inventory_item_id == requested_item.id)).scalars().all():
            results = db.session.execute(
                db.select(InventoryMovement).where(InventoryMovement.date.like(search_format.title()), InventoryMovement.inventory_item_id == requested_item.id)).scalars()
            return render_template("display_item_movements.html", item=requested_item, search=True, all_movements=results)
        else:
            flash("There are no results found")
            return redirect(url_for('display_item_movements', inventory_item_id=requested_item.id))



@app.route("/search_custody_settlement/<int:custody_id>", methods=["GET", "POST"])
@login_required
def search_custody_settlement(custody_id):
    requested_custody = db.get_or_404(Custody, custody_id)
    if request.method == "POST":
        search_text = request.form["input_name"]
        search_format = "%{}%".format(search_text)
        if db.session.execute(db.select(CustodySettlement).where(CustodySettlement.description.like(search_format),
                                                                 CustodySettlement.custody_id == custody_id)).scalars().all():
            results = db.session.execute(db.select(CustodySettlement).where(CustodySettlement.description.like(search_format), CustodySettlement.custody_id == custody_id)).scalars()

            return render_template("display_user_custodes.html", custody_settlements=results, custody=requested_custody, search=True)
        elif db.session.execute(db.select(CustodySettlement).where(CustodySettlement.date.like(search_format),
                                                                 CustodySettlement.custody_id == custody_id)).scalars().all():
            results = db.session.execute(
                db.select(CustodySettlement).where(CustodySettlement.date.like(search_format),
                                                   CustodySettlement.custody_id == custody_id)).scalars()

            return render_template("display_user_custodes.html", custody_settlements=results, custody=requested_custody,search=True)

        else:
            flash("There are no results found")
            return render_template("display_user_custodes.html", custody=requested_custody)



@app.route("/cash_in", methods=["GET", "POST"])
@login_required
@add_cash
def cash_in():
    form = CashIn()
    if form.validate_on_submit():
        new_cash_in = Cash(description=form.description.data, debit=form.amount.data, credit=0, balance=0, date=datetime.datetime.now().strftime("%d/%m/%Y"), contra_account="Cash In")
        db.session.add(new_cash_in)
        db.session.commit()
        flash("Cash In has been added successfully")
        return redirect(url_for('cash_in'))
    return render_template("add_cash_movement.html", form=form)




@app.route("/display_cash")
@login_required
@display_cash_account
def display_cash():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    all_cash = db.session.execute(db.select(Cash)).scalars().all()
    page = request.args.get(get_page_parameter(), type=int, default=1)

    total_balance = 0
    total_debit = 0
    total_credit = 0
    for cash in all_cash:
        total_balance += cash.debit - cash.credit
        total_debit += cash.debit
        total_credit += cash.credit
        cash.balance = total_balance
        db.session.commit()
    pagination = Pagination(all_cash, page=page, css_framework='bootstrap5', total=len(all_cash), search=search,
                            record_name='Cash Account')
    all_cash_paginate = db.paginate(db.select(Cash), page=page, per_page=10, error_out=False)
    return render_template("display_cash.html",all_cash=all_cash_paginate, total_credit=total_credit, total_debit=total_debit, total_balance=total_balance, year=year, pagination=pagination)



@app.route("/search_cash", methods=["GET", "POST"])
@login_required
def search_cash():
    if request.method == "POST":
        search_text = request.form["input_name"]
        search_format = "%{}%".format(search_text)
        if db.session.execute(db.select(Cash).where(Cash.description.like(search_format))).scalars().all():
            results = db.session.execute(db.select(Cash).where(Cash.description.like(search_format))).scalars()
            return render_template("display_cash.html", all_cash=results, search=True, year=year)
        elif db.session.execute(db.select(Cash).where(Cash.date.like(search_format))).scalars().all():
            results = db.session.execute(db.select(Cash).where(Cash.date.like(search_format))).scalars()
            return render_template("display_cash.html", all_cash=results, search=True, year=year)
        elif db.session.execute(db.select(Cash).where(Cash.contra_account.like(search_format))).scalars().all():
            results = db.session.execute(db.select(Cash).where(Cash.contra_account.like(search_format))).scalars()
            return render_template("display_cash.html", all_cash=results, search=True, year=year)
        else:
            flash("There are no results found")
            return redirect(url_for('display_cash'))



@app.route("/edit_cash_in/<int:cash_id>", methods=["GET", "POST"])
@login_required
@edit_cash_in
def edit_cash_in(cash_id):
    requested_cash_in = db.get_or_404(Cash, cash_id)
    form = CashIn(description=requested_cash_in.description, amount=requested_cash_in.debit)
    if form.validate_on_submit():
        requested_cash_in.description = form.description.data
        requested_cash_in.debit = form.amount.data
        db.session.commit()
        return redirect(url_for('display_cash'))
    return render_template("add_cash_movement.html", form=form, edit=True)



@app.route("/delete_cash_in/<int:cash_id>")
@login_required
@delete_cash_in
def delete_cash_in(cash_id):
    requested_cash_in = db.get_or_404(Cash, cash_id)
    file_name = requested_cash_in.file_path
    try:
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                               secure_filename(file_name)))
    except FileNotFoundError:
        pass
    except TypeError:
        pass
    except PermissionError:
        pass
    db.session.delete(requested_cash_in)
    db.session.commit()
    flash("Cash In has been deleted successfully.")
    return redirect(url_for('display_cash'))


def track_number(project_id):
    list_letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                   "u", "v", "w", "x", "y", "z"]
    list_sympol = ["@", "!", "&", "#", "$", "*", "%"]
    first_number = random.randint(0, 9)
    second_number = random.randint(0, 9)
    first_litter = random.choice(list_letter)
    second_litter = random.choice(list_letter)
    first_sympol = random.choice(list_sympol)
    second_sympol = random.choice(list_sympol)
    password = f"{first_number}{first_sympol}{first_litter}{second_sympol}{second_number}{second_litter}"
    if db.session.execute(db.select(Project).where(Project.track_number == password)).scalar():
        track_number(project_id)
    else:
        requested_project = db.session.execute(db.select(Project).where(Project.id == project_id)).scalar()
        requested_project.track_number = password
        db.session.commit()



@app.route('/uploads/<name>')
@login_required
@download_file
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)



@app.route("/upload_file/<string:name>/<int:id>", methods=["GET", "POST"])
@login_required
@upload_file
def upload_file(name, id):
    form = UploadFile()
    file = form.file_name.data
    if form.validate_on_submit():
        projects = db.session.execute(db.select(Project)).scalars().all()
        for project in projects:
            if project.file_path:
                if secure_filename(file.filename) == project.file_path:
                    flash(f"This file existed at projects please upload instead or change the file name.")
                    return redirect(url_for('upload_file', name=name, id=id))
        subcontractors = db.session.execute(db.select(SubContractor)).scalars().all()
        for subcontractor in subcontractors:
            if subcontractor.file_path:
                if secure_filename(file.filename) == subcontractor.file_path:
                    flash(f"This file existed at subcontractor please upload instead or change the file name.")
                    return redirect(url_for('upload_file', name=name, id=id))
        custody_settlements = db.session.execute(db.select(CustodySettlement)).scalars().all()
        for custody_settlement in custody_settlements:
            if custody_settlement.file_path:
                if secure_filename(file.filename) == custody_settlement.file_path:
                    flash(f"This file existed at custody settlement  please upload instead or change the file name.")
                    return redirect(url_for('upload_file', name=name, id=id))
        employee_salaries = db.session.execute(db.select(EmployeesSalary)).scalars().all()
        for employee_salary in employee_salaries:
            if employee_salary.file_path:
                if secure_filename(file.filename) == employee_salary.file_path:
                    flash(f"This file existed at employee salary please upload instead or change the file name.")
                    return redirect(url_for('upload_file', name=name, id=id))
        inventory_movements = db.session.execute(db.select(InventoryMovement)).scalars().all()
        for inventory_movement in inventory_movements:
            if inventory_movement.file_path:
                if secure_filename(file.filename) == inventory_movement.file_path:
                    flash("This file existed at inventory movement please upload instead or change the file name.")
                    return redirect(url_for('upload_file', name=name, id=id))
        cashes = db.session.execute(db.select(Cash)).scalars().all()
        for cash in cashes:
            if cash.file_path:
                if secure_filename(file.filename) == cash.file_path:
                    flash("This file existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('upload_file', name=name, id=id))
        expenses_details = db.session.execute(db.select(ExpenseDetail)).scalars().all()
        for expenses_detail in expenses_details:
            if expenses_detail.file_path:
                if secure_filename(file.filename) == expenses_detail.file_path:
                    flash("This file existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('upload_file', name=name, id=id))
        works_tracking = db.session.execute(db.select(WorkTrack)).scalars().all()
        for work_tracking in works_tracking:
            if work_tracking.file_path:
                if secure_filename(file.filename) == work_tracking.file_path:
                    flash("This file existed at works tracking in please upload instead or change the file name.")
                    return redirect(url_for('upload_file', name=name, id=id))
        financial_requirements = db.session.execute(db.select(FinancialRequirement)).scalars().all()
        for financial_requirement in financial_requirements:
            if financial_requirement.file_path:
                if secure_filename(file.filename) == financial_requirement.file_path:
                    flash("This file existed at financial requirements in please upload instead or change the file name.")
                    return redirect(url_for('upload_file', name=name, id=id))
        operation_expenses = db.session.execute(db.select(OperationExpense)).scalars().all()
        for operation_expense in operation_expenses:
            if operation_expense.file_path:
                if secure_filename(file.filename) == operation_expense.file_path:
                    flash(
                        "This file existed at operating expense in please upload instead or change the file name.")
                    return redirect(url_for('upload_file', name=name, id=id))

        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                               secure_filename(file.filename)))
        if name == "Project":
            requested_project = db.get_or_404(Project, id)
            requested_project.file_path = file.filename
            db.session.commit()
            flash("File Has Been Uploaded Successfully")
            return redirect(url_for('display_project', project_id=id))
        elif name == "SubContractor":
            requested_subcontractor = db.session.execute(db.select(SubContractor).where(SubContractor.id == id)).scalar()
            if requested_subcontractor.opening_balance > 0:
                requested_subcontractor.file_path = file.filename
                db.session.commit()
                flash("File Has Been Uploaded Successfully")
                return redirect(url_for('display_subcontractor_accounts', project_id=requested_subcontractor.project_id))
            elif requested_subcontractor.cash_out > 0:
                requested_cash = db.session.execute(db.select(Cash).where(Cash.id == requested_subcontractor.cash_id)).scalar()
                requested_project_cost = db.session.execute(db.select(ProjectCost).where(ProjectCost.subcontractor_id == requested_subcontractor.id)).scalar()
                requested_subcontractor.file_path = file.filename
                requested_cash.file_path = file.filename
                requested_project_cost.file_path = file.filename
                db.session.commit()
                flash("File Has Been Uploaded Successfully")
                return redirect(url_for('display_subcontractor_accounts', project_id=requested_subcontractor.project_id))
        elif name == "CustodySettlement":
            requested_custody_settlement = db.session.execute(db.select(CustodySettlement).where(CustodySettlement.id == id)).scalar()
            if requested_custody_settlement.debit > 0:
                requested_cash = db.session.execute(db.select(Cash).where(Cash.id == requested_custody_settlement.cash_id)).scalar()
                requested_custody_settlement.file_path = file.filename
                requested_cash.file_path = file.filename
                db.session.commit()
                flash("File Has Been Uploaded Successfully")
                return redirect(url_for("display_user_custodes", custody_id=requested_custody_settlement.custody_id))
            elif requested_custody_settlement.credit > 0:
                requested_project_cost = db.session.execute(db.select(ProjectCost).where(ProjectCost.id == requested_custody_settlement.project_cost_id)).scalar()
                requested_custody_settlement.file_path = file.filename
                requested_project_cost.file_path = file.filename
                db.session.commit()
                flash("File Has Been Uploaded Successfully")
                return redirect(url_for("display_user_custodes", custody_id=requested_custody_settlement.custody_id))
        elif name == "EmployeeSalary":
            requested_employee_salary = db.session.execute(db.select(EmployeesSalary).where(EmployeesSalary.id == id)).scalar()
            requested_cash = db.session.execute(db.select(Cash).where(Cash.id == requested_employee_salary.cash_id)).scalar()
            requested_employee_salary.file_path = file.filename
            requested_cash.file_path = file.filename
            db.session.commit()
            flash("File Has Been Uploaded Successfully")
            return redirect(url_for('display_employee_salaries', employee_id=requested_employee_salary.employee_id))
        elif name == "InventoryMovement":
            requested_inventory_movement = db.session.execute(db.select(InventoryMovement).where(InventoryMovement.id == id)).scalar()
            if requested_inventory_movement.quantity_in > 0:
                requested_cash = db.session.execute(db.select(Cash).where(Cash.id == requested_inventory_movement.cash_id)).scalar()
                requested_inventory_movement.file_path = file.filename
                requested_cash.file_path = file.filename
                db.session.commit()
                flash("File Has Been Uploaded Successfully")
                return redirect(url_for('display_item_movements', inventory_item_id=requested_inventory_movement.inventory_item_id))
            elif requested_inventory_movement.quantity_out > 0:
                requested_project_cost = db.session.execute(db.select(ProjectCost).where(ProjectCost.id == requested_inventory_movement.project_cost_id)).scalar()
                requested_inventory_movement.file_path = file.filename
                requested_project_cost.file_path = file.filename
                db.session.commit()
                flash("File Has Been Uploaded Successfully")
                return redirect(url_for('display_item_movements', inventory_item_id=requested_inventory_movement.inventory_item_id))
        elif name == "Cash In":
            requested_cash_in = db.get_or_404(Cash, id)
            requested_cash_in.file_path = file.filename
            db.session.commit()
            flash("File Has Been Uploaded Successfully")
            return redirect(url_for('display_cash'))
        elif name == "ExpenseDetail":
            requested_expense_detail = db.session.execute(db.select(ExpenseDetail).where(ExpenseDetail.id == id)).scalar()
            requested_cash_out = db.session.execute(db.select(Cash).where(Cash.id == requested_expense_detail.cash_id)).scalar()
            requested_expense_detail.file_path = file.filename
            requested_cash_out.file_path = file.filename
            db.session.commit()
            flash("File Has Been Uploaded Successfully")
            return redirect(url_for('display_expense_details', expense_id=requested_expense_detail.expense_id))
        elif name == "OperationExpense":
            requested_operation_expense = db.session.execute(db.select(OperationExpense).where(OperationExpense.id == id)).scalar()
            requested_cash_out = db.session.execute(db.select(Cash).where(Cash.id == requested_operation_expense.cash_id)).scalar()
            requested_project_cost = db.session.execute(
                db.select(ProjectCost).where(ProjectCost.id == requested_operation_expense.project_cost_id)).scalar()
            requested_operation_expense.file_path = file.filename
            requested_cash_out.file_path = file.filename
            requested_project_cost.file_path = file.filename
            db.session.commit()
            flash("File Has Been Uploaded Successfully")
            return redirect(url_for('display_all_operation_expenses'))
    return render_template("upload_file.html", form=form, name=name, id=id)



@app.route("/delete_upload_file/<string:name>/<int:id>")
@login_required
@delete_file
def delete_upload_file(name, id):
    if name == "Project":
        requested_project = db.get_or_404(Project, id)
        file_name = requested_project.file_path
        try:
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                   secure_filename(file_name)))
        except FileNotFoundError:
            pass
        except TypeError:
            pass
        except PermissionError:
            pass
        requested_project.file_path = ""
        db.session.commit()
        flash("File Has Been deleted Successfully")
        return redirect(url_for('display_project', project_id=id))
    elif name == "SubContractor":
        requested_subcontractor = db.session.execute(db.select(SubContractor).where(SubContractor.id == id)).scalar()
        file_name = requested_subcontractor.file_path
        try:
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                   secure_filename(file_name)))
        except FileNotFoundError:
            pass
        except TypeError:
            pass
        except PermissionError:
            pass
        if requested_subcontractor.opening_balance > 0:
            requested_subcontractor.file_path = ""
            db.session.commit()
            flash("File Has Been Deleted Successfully")
            return redirect(url_for('display_subcontractor_accounts', project_id=requested_subcontractor.project_id))
        elif requested_subcontractor.cash_out > 0:
            requested_cash = db.session.execute(db.select(Cash).where(Cash.id == requested_subcontractor.cash_id)).scalar()
            requested_project_cost = db.session.execute(db.select(ProjectCost).where(ProjectCost.subcontractor_id == requested_subcontractor.id)).scalar()
            requested_subcontractor.file_path = ""
            requested_cash.file_path = ""
            requested_project_cost.file_path = ""
            db.session.commit()
            flash("File Has Been Deleted Successfully")
            return redirect(url_for('display_subcontractor_accounts', project_id=requested_subcontractor.project_id))
    elif name == "CustodySettlement":
        requested_custody_settlement = db.session.execute(db.select(CustodySettlement).where(CustodySettlement.id == id)).scalar()
        file_name = requested_custody_settlement.file_path
        try:
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                   secure_filename(file_name)))
        except FileNotFoundError:
            pass
        except TypeError:
            pass
        except PermissionError:
            pass
        if requested_custody_settlement.debit > 0:
            requested_cash = db.session.execute(db.select(Cash).where(Cash.id == requested_custody_settlement.cash_id)).scalar()
            requested_custody_settlement.file_path = ""
            requested_cash.file_path = ""
            db.session.commit()
            flash("File Has Been Deleted Successfully")
            return redirect(url_for("display_user_custodes", custody_id=requested_custody_settlement.custody_id))
        elif requested_custody_settlement.credit > 0:
            requested_project_cost = db.session.execute(db.select(ProjectCost).where(ProjectCost.id == requested_custody_settlement.project_cost_id)).scalar()
            requested_custody_settlement.file_path = ""
            requested_project_cost.file_path = ""
            db.session.commit()
            flash("File Has Been Deleted Successfully")
            return redirect(url_for("display_user_custodes", custody_id=requested_custody_settlement.custody_id))
    elif name == "EmployeeSalary":
        requested_employee_salary = db.session.execute(db.select(EmployeesSalary).where(EmployeesSalary.id == id)).scalar()
        file_name = requested_employee_salary.file_path
        try:
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                   secure_filename(file_name)))
        except FileNotFoundError:
            pass
        except TypeError:
            pass
        except PermissionError:
            pass
        requested_cash = db.session.execute(db.select(Cash).where(Cash.id == requested_employee_salary.cash_id)).scalar()
        requested_employee_salary.file_path = ""
        requested_cash.file_path = ""
        db.session.commit()
        flash("File Has Been Deleted Successfully")
        return redirect(url_for('display_employee_salaries', employee_id=requested_employee_salary.employee_id))
    elif name == "InventoryMovement":
        requested_inventory_movement = db.session.execute(db.select(InventoryMovement).where(InventoryMovement.id == id)).scalar()
        file_name = requested_inventory_movement.file_path
        try:
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                   secure_filename(file_name)))
        except FileNotFoundError:
            pass
        except TypeError:
            pass
        except PermissionError:
            pass
        if requested_inventory_movement.quantity_in > 0:
            requested_cash = db.session.execute(db.select(Cash).where(Cash.id == requested_inventory_movement.cash_id)).scalar()
            requested_inventory_movement.file_path = ""
            requested_cash.file_path = ""
            db.session.commit()
            flash("File Has Been Deleted Successfully")
            return redirect(url_for('display_item_movements', inventory_item_id=requested_inventory_movement.inventory_item_id))
        elif requested_inventory_movement.quantity_out > 0:
            requested_project_cost = db.session.execute(db.select(ProjectCost).where(ProjectCost.id == requested_inventory_movement.project_cost_id)).scalar()
            requested_inventory_movement.file_path = ""
            requested_project_cost.file_path = ""
            db.session.commit()
            flash("File Has Been Deleted Successfully")
            return redirect(url_for('display_item_movements', inventory_item_id=requested_inventory_movement.inventory_item_id))
    elif name == "Cash In":
        requested_cash_in = db.get_or_404(Cash, id)
        file_name = requested_cash_in.file_path
        try:
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                   secure_filename(file_name)))
        except FileNotFoundError:
            pass
        except TypeError:
            pass
        except PermissionError:
            pass
        requested_cash_in.file_path = ""
        db.session.commit()
        flash("File Has Been Deleted Successfully")
        return redirect(url_for('display_cash'))
    elif name == "ExpenseDetail":
        requested_expense_detail = db.session.execute(db.select(ExpenseDetail).where(ExpenseDetail.id == id)).scalar()
        file_name = requested_expense_detail.file_path
        try:
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                   secure_filename(file_name)))
        except FileNotFoundError:
            pass
        except TypeError:
            pass
        except PermissionError:
            pass
        requested_cash = db.session.execute(db.select(Cash).where(Cash.id == requested_expense_detail.cash_id)).scalar()
        requested_expense_detail.file_path = ""
        requested_cash.file_path = ""
        db.session.commit()
        flash("File Has Been Deleted Successfully")
        return redirect(url_for('display_expense_details', expense_id=requested_expense_detail.expense_id))
    elif name == "OperationExpense":
        requested_operating_expense = db.session.execute(db.select(OperationExpense).where(OperationExpense.id == id)).scalar()
        file_name = requested_operating_expense.file_path
        try:
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                   secure_filename(file_name)))
        except FileNotFoundError:
            pass
        except TypeError:
            pass
        except PermissionError:
            pass
        requested_cash = db.session.execute(db.select(Cash).where(Cash.id == requested_operating_expense.cash_id)).scalar()
        requested_project_cost = db.session.execute(db.select(ProjectCost).where(ProjectCost.id == requested_operating_expense.project_cost_id)).scalar()
        requested_operating_expense.file_path = ""
        requested_cash.file_path = ""
        requested_project_cost.file_path = ""
        db.session.commit()
        flash("File Has Been Deleted Successfully")
        return redirect(url_for('display_all_operation_expenses'))


@app.route("/edit_user_permission/<int:user_id>", methods=["GET", "POST"])
@login_required
@admin_only
def edit_user_permission(user_id):
    requested_user = db.get_or_404(User, user_id)
    form = Permissions(cash=requested_user.cash, add_cash=requested_user.add_cash,
                       display_cash_account=requested_user.display_cash_account, edit_cash_in=requested_user.edit_cash_in,
                       delete_cash_in=requested_user.delete_cash_in,projects=requested_user.projects,
                       add_project=requested_user.add_project,display_all_projects=requested_user.display_all_projects,
                       display_project=requested_user.display_project, add_project_details=requested_user.add_project_details,
                       edit_project_details=requested_user.edit_project_details, delete_project_details=requested_user.delete_project_details,
                       add_works_tracking=requested_user.add_works_tracking, delete_works_tracking=requested_user.delete_works_tracking,
                       add_subcontractor_opening_balance=requested_user.add_subcontractor_opening_account,
                       add_subcontractor_cash_out=requested_user.add_subcontractor_cash_out,edit_project=requested_user.edit_project,
                       display_subcontractor_account=requested_user.display_subcontractor_account,
                       edit_subcontractor_account=requested_user.edit_subcontractor_account,
                       delete_subcontractor_account=requested_user.delete_subcontractor_account,
                       display_project_cost=requested_user.display_project_cost,custody=requested_user.custody,
                       display_my_custody=requested_user.display_my_custody,display_all_custodes=requested_user.display_all_custodes,
                       display_employee_custody=requested_user.display_employee_custody,
                       edit_employee_name=requested_user.edit_employee_name,add_custody_settlement=requested_user.add_custody_settlement,
                       add_custody_cash_out=requested_user.add_custody_cash_out,edit_custody_cash_out=requested_user.edit_custody_cash_out,
                       delete_custody_cash_out=requested_user.delete_custody_cash_out,edit_custody_settlement=requested_user.edit_custody_settlement,
                       delete_custody_settlement=requested_user.delete_custody_settlement,payroll=requested_user.payroll,
                       add_employee=requested_user.add_employee,display_all_employees=requested_user.display_all_employees,salary_cash_out=requested_user.salary_cash_out,
                       display_employee_salary=requested_user.display_employee_salary,edit_employee_details=requested_user.edit_employee_details,
                       edit_salary=requested_user.edit_salary,delete_salary=requested_user.delete_salary,inventory=requested_user.inventory,
                       add_item=requested_user.add_item, display_all_items=requested_user.display_all_items,
                       display_item_movements=requested_user.display_item_movements, edit_item=requested_user.edit_item,
                       import_item=requested_user.import_item, export_item=requested_user.export_item,
                       edit_item_movement=requested_user.edit_item_movement,delete_item_movement=requested_user.delete_item_movement,
                       expenses=requested_user.expenses, add_expense=requested_user.add_expense,display_all_expenses=requested_user.display_all_expenses, expense_cash_out=requested_user.expense_cash_out,
                       display_expense_details=requested_user.display_expense_details, edit_expense=requested_user.edit_expense, edit_expense_cash_out=requested_user.edit_expense_cash_out,
                       delete_expense_cash_out=requested_user.delete_expense_cash_out,operating_expense_cash_out=requested_user.operating_expense_cash_out,
                       display_all_operating_expenses=requested_user.display_all_operating_expenses,edit_operating_expense=requested_user.edit_operating_expense, delete_operating_expense=requested_user.delete_operating_expense, notifications=requested_user.notifications,
                       add_financial_requirement=requested_user.add_financial_requirement, display_all_financial_requirements=requested_user.display_all_financial_requirements,
                       delete_financial_requirement=requested_user.delete_financial_requirement, add_subcontractor_requirement=requested_user.add_subcontractor_requirement,
                       display_subcontractor_requirements=requested_user.display_subcontractor_requirements,add_purchase_requirement=requested_user.add_purchase_requirement, display_purchase_requirements=requested_user.display_purchase_requirements,
                       edit_subcontractor_requirement=requested_user.edit_subcontractor_requirement, delete_subcontractor_requirement=requested_user.delete_subcontractor_requirement,
                       upload_file=requested_user.upload_file, download_file=requested_user.download_file,delete_file=requested_user.delete_file)
    if form.validate_on_submit():
        requested_user.cash = int(form.cash.data)
        requested_user.add_cash = int(form.add_cash.data)
        requested_user.display_cash_account = int(form.display_cash_account.data)
        requested_user.edit_cash_in = int(form.edit_cash_in.data)
        requested_user.delete_cash_in = int(form.delete_cash_in.data)
        requested_user.projects = int(form.projects.data)
        requested_user.add_project = int(form.add_project.data)
        requested_user.edit_project = int(form.edit_project.data)
        requested_user.display_all_projects = int(form.display_all_projects.data)
        requested_user.display_project = int(form.display_project.data)
        requested_user.add_project_details = int(form.add_project_details.data)
        requested_user.edit_project_details = int(form.edit_project_details.data)
        requested_user.delete_project_details = int(form.delete_project_details.data)
        requested_user.add_works_tracking = int(form.add_works_tracking.data)
        requested_user.delete_works_tracking = int(form.delete_works_tracking.data)
        requested_user.add_subcontractor_opening_account = int(form.add_subcontractor_opening_balance.data)
        requested_user.add_subcontractor_cash_out = int(form.add_subcontractor_cash_out.data)
        requested_user.display_subcontractor_account = int(form.display_subcontractor_account.data)
        requested_user.edit_subcontractor_account = int(form.edit_subcontractor_account.data)
        requested_user.delete_subcontractor_account = int(form.delete_subcontractor_account.data)
        requested_user.display_project_cost = int(form.display_project_cost.data)
        requested_user.custody = int(form.custody.data)
        requested_user.display_my_custody = int(form.display_my_custody.data)
        requested_user.display_all_custodes = int(form.display_all_custodes.data)
        requested_user.display_employee_custody = int(form.display_employee_custody.data)
        requested_user.edit_employee_name = int(form.edit_employee_name.data)
        requested_user.add_custody_settlement = int(form.add_custody_settlement.data)
        requested_user.edit_custody_settlement = int(form.edit_custody_settlement.data)
        requested_user.delete_custody_settlement = int(form.delete_custody_settlement.data)
        requested_user.add_custody_cash_out = int(form.add_custody_cash_out.data)
        requested_user.edit_custody_cash_out = int(form.edit_custody_cash_out.data)
        requested_user.delete_custody_cash_out = int(form.delete_custody_cash_out.data)
        requested_user.payroll = int(form.payroll.data)
        requested_user.add_employee = int(form.add_employee.data)
        requested_user.display_all_employees = int(form.display_all_employees.data)
        requested_user.salary_cash_out = int(form.salary_cash_out.data)
        requested_user.display_employee_salary = int(form.display_employee_salary.data)
        requested_user.edit_employee_details = int(form.edit_employee_details.data)
        requested_user.edit_salary = int(form.edit_salary.data)
        requested_user.delete_salary = int(form.delete_salary.data)
        requested_user.inventory = int(form.inventory.data)
        requested_user.add_item = int(form.add_item.data)
        requested_user.edit_item = int(form.edit_item.data)
        requested_user.display_all_items = int(form.display_all_items.data)
        requested_user.display_item_movements = int(form.display_item_movements.data)
        requested_user.edit_item_movement = int(form.edit_item_movement.data)
        requested_user.delete_item_movement = int(form.delete_item_movement.data)
        requested_user.import_item = int(form.import_item.data)
        requested_user.export_item = int(form.export_item.data)
        requested_user.expenses = int(form.expenses.data)
        requested_user.add_expense = int(form.add_expense.data)
        requested_user.display_all_expenses = int(form.display_all_expenses.data)
        requested_user.expense_cash_out = int(form.expense_cash_out.data)
        requested_user.display_expense_details = int(form.display_expense_details.data)
        requested_user.edit_expense = int(form.edit_expense.data)
        requested_user.edit_expense_cash_out = int(form.edit_expense_cash_out.data)
        requested_user.delete_expense_cash_out = int(form.delete_expense_cash_out.data)
        requested_user.operating_expense_cash_out = int(form.operating_expense_cash_out.data)
        requested_user.display_all_operating_expenses = int(form.display_all_operating_expenses.data)
        requested_user.edit_operating_expense = int(form.edit_operating_expense.data)
        requested_user.delete_operating_expense = int(form.delete_operating_expense.data)
        requested_user.notifications = int(form.notifications.data)
        requested_user.add_financial_requirement = int(form.add_financial_requirement.data)
        requested_user.display_all_financial_requirements = int(form.display_all_financial_requirements.data)
        requested_user.delete_financial_requirement = int(form.delete_financial_requirement.data)
        requested_user.add_subcontractor_requirement = int(form.add_subcontractor_requirement.data)
        requested_user.display_subcontractor_requirements = int(form.display_subcontractor_requirements.data)
        requested_user.edit_subcontractor_requirement = int(form.edit_subcontractor_requirement.data)
        requested_user.delete_subcontractor_requirement = int(form.delete_subcontractor_requirement.data)
        requested_user.add_purchase_requirement = int(form.add_purchase_requirement.data)
        requested_user.display_purchase_requirements = int(form.display_purchase_requirements.data)
        requested_user.upload_file = int(form.upload_file.data)
        requested_user.download_file = int(form.download_file.data)
        requested_user.delete_file = int(form.delete_file.data)
        db.session.commit()
        return redirect(url_for('all_users'))
    return render_template('edit_user_permission.html', user=requested_user, form=form,
                           logged_in=current_user.is_authenticated)


@app.route("/add_works_track/<int:project_detail_id>", methods=["GET", "POST"])
@login_required
@add_works_tracking
def add_works_tracking(project_detail_id):
    requested_project_detail = db.get_or_404(ProjectDetail, project_detail_id)
    form = WorksTrack()
    if form.validate_on_submit():
        if form.image_1.data:
            projects = db.session.execute(db.select(Project)).scalars().all()
            for project in projects:
                if secure_filename(form.image_1.data.filename) == project.file_path:
                    flash(f"Image 1 existed at projects please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            subcontractors = db.session.execute(db.select(SubContractor)).scalars().all()
            for subcontractor in subcontractors:
                if secure_filename(form.image_1.data.filename) == subcontractor.file_path:
                    flash(f"Image 1  existed at subcontractor please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            custody_settlements = db.session.execute(db.select(CustodySettlement)).scalars().all()
            for custody_settlement in custody_settlements:
                if secure_filename(form.image_1.data.filename) == custody_settlement.file_path:
                    flash(f"Image 1  existed at custody settlement  please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            employee_salaries = db.session.execute(db.select(EmployeesSalary)).scalars().all()
            for employee_salary in employee_salaries:
                if secure_filename(form.image_1.data.filename) == employee_salary.file_path:
                    flash(f"Image 1  existed at employee salary please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            inventory_movements = db.session.execute(db.select(InventoryMovement)).scalars().all()
            for inventory_movement in inventory_movements:
                if secure_filename(form.image_1.data.filename) == inventory_movement.file_path:
                    flash("This file existed at inventory movement please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            cashes = db.session.execute(db.select(Cash)).scalars().all()
            for cash in cashes:
                if secure_filename(form.image_1.data.filename) == cash.file_path:
                    flash("Image 1  existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            works_tracking = db.session.execute(db.select(WorkTrack)).scalars().all()
            for work_tracking in works_tracking:
                if secure_filename(form.image_1.data.filename) == work_tracking.file_path:
                    flash("This file existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            financial_requirements = db.session.execute(db.select(FinancialRequirement)).scalars().all()
            for financial_requirement in financial_requirements:
                if financial_requirement.file_path:
                    if secure_filename(form.image_5.data.filename) == financial_requirement.file_path:
                        flash(
                            "Image 1  existed at financial requirements in please upload instead or change the file name.")
                        return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            new_work_track = WorkTrack(file_path=form.image_1.data.filename, project_details_id=project_detail_id, percentage=form.percentage.data, project_id=requested_project_detail.project_id)
            db.session.add(new_work_track)
            db.session.commit()

            form.image_1.data.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                   secure_filename(form.image_1.data.filename)))
        if form.image_2.data:
            projects = db.session.execute(db.select(Project)).scalars().all()
            for project in projects:
                if secure_filename(form.image_2.data.filename) == project.file_path:
                    flash(f"Image 2 existed at projects please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            subcontractors = db.session.execute(db.select(SubContractor)).scalars().all()
            for subcontractor in subcontractors:
                if secure_filename(form.image_2.data.filename) == subcontractor.file_path:
                    flash(f"Image 2 existed at subcontractor please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            custody_settlements = db.session.execute(db.select(CustodySettlement)).scalars().all()
            for custody_settlement in custody_settlements:
                if secure_filename(form.image_2.data.filename) == custody_settlement.file_path:
                    flash(f"Image 2 existed at custody settlement  please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            employee_salaries = db.session.execute(db.select(EmployeesSalary)).scalars().all()
            for employee_salary in employee_salaries:
                if secure_filename(form.image_2.data.filename) == employee_salary.file_path:
                    flash(f"Image 2 existed at employee salary please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            inventory_movements = db.session.execute(db.select(InventoryMovement)).scalars().all()
            for inventory_movement in inventory_movements:
                if secure_filename(form.image_2.data.filename) == inventory_movement.file_path:
                    flash("Image 2 existed at inventory movement please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            cashes = db.session.execute(db.select(Cash)).scalars().all()
            for cash in cashes:
                if secure_filename(form.image_2.data.filename) == cash.file_path:
                    flash("Image 2 existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            works_tracking = db.session.execute(db.select(WorkTrack)).scalars().all()
            for work_tracking in works_tracking:
                if secure_filename(form.image_2.data.filename) == work_tracking.file_path:
                    flash("Image 2 existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            financial_requirements = db.session.execute(db.select(FinancialRequirement)).scalars().all()
            for financial_requirement in financial_requirements:
                if financial_requirement.file_path:
                    if secure_filename(form.image_5.data.filename) == financial_requirement.file_path:
                        flash(
                            "Image 2 existed at financial requirements in please upload instead or change the file name.")
                        return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            new_work_track = WorkTrack(file_path=form.image_2.data.filename, project_details_id=project_detail_id, percentage=form.percentage.data, project_id=requested_project_detail.project_id)
            db.session.add(new_work_track)
            db.session.commit()
            form.image_2.data.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                                secure_filename(form.image_2.data.filename)))
        if form.image_3.data:
            projects = db.session.execute(db.select(Project)).scalars().all()
            for project in projects:
                if secure_filename(form.image_3.data.filename) == project.file_path:
                    flash(f"Image 3 existed at projects please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            subcontractors = db.session.execute(db.select(SubContractor)).scalars().all()
            for subcontractor in subcontractors:
                if secure_filename(form.image_3.data.filename) == subcontractor.file_path:
                    flash(f"Image 3 existed at subcontractor please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            custody_settlements = db.session.execute(db.select(CustodySettlement)).scalars().all()
            for custody_settlement in custody_settlements:
                if secure_filename(form.image_3.data.filename) == custody_settlement.file_path:
                    flash(f"Image 3 existed at custody settlement  please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            employee_salaries = db.session.execute(db.select(EmployeesSalary)).scalars().all()
            for employee_salary in employee_salaries:
                if secure_filename(form.image_3.data.filename) == employee_salary.file_path:
                    flash(f"Image 3 existed at employee salary please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            inventory_movements = db.session.execute(db.select(InventoryMovement)).scalars().all()
            for inventory_movement in inventory_movements:
                if secure_filename(form.image_3.data.filename) == inventory_movement.file_path:
                    flash("Image 3 existed at inventory movement please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            cashes = db.session.execute(db.select(Cash)).scalars().all()
            for cash in cashes:
                if secure_filename(form.image_3.data.filename) == cash.file_path:
                    flash("Image 3 existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            works_tracking = db.session.execute(db.select(WorkTrack)).scalars().all()
            for work_tracking in works_tracking:
                if secure_filename(form.image_3.data.filename) == work_tracking.file_path:
                    flash("Image 3 existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            financial_requirements = db.session.execute(db.select(FinancialRequirement)).scalars().all()
            for financial_requirement in financial_requirements:
                if financial_requirement.file_path:
                    if secure_filename(form.image_5.data.filename) == financial_requirement.file_path:
                        flash(
                            "Image 3 existed at financial requirements in please upload instead or change the file name.")
                        return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            new_work_track = WorkTrack(file_path=form.image_3.data.filename, project_details_id=project_detail_id, percentage=form.percentage.data, project_id=requested_project_detail.project_id)
            db.session.add(new_work_track)
            db.session.commit()
            form.image_3.data.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                                secure_filename(form.image_3.data.filename)))
        if form.image_4.data:
            projects = db.session.execute(db.select(Project)).scalars().all()
            for project in projects:
                if secure_filename(form.image_4.data.filename) == project.file_path:
                    flash(f"Image 4 existed at projects please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            subcontractors = db.session.execute(db.select(SubContractor)).scalars().all()
            for subcontractor in subcontractors:
                if secure_filename(form.image_4.data.filename) == subcontractor.file_path:
                    flash(f"Image 4 existed at subcontractor please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            custody_settlements = db.session.execute(db.select(CustodySettlement)).scalars().all()
            for custody_settlement in custody_settlements:
                if secure_filename(form.image_4.data.filename) == custody_settlement.file_path:
                    flash(f"Image 4 existed at custody settlement  please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            employee_salaries = db.session.execute(db.select(EmployeesSalary)).scalars().all()
            for employee_salary in employee_salaries:
                if secure_filename(form.image_4.data.filename) == employee_salary.file_path:
                    flash(f"Image 4 existed at employee salary please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            inventory_movements = db.session.execute(db.select(InventoryMovement)).scalars().all()
            for inventory_movement in inventory_movements:
                if secure_filename(form.image_4.data.filename) == inventory_movement.file_path:
                    flash("Image 4 existed at inventory movement please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            cashes = db.session.execute(db.select(Cash)).scalars().all()
            for cash in cashes:
                if secure_filename(form.image_4.data.filename) == cash.file_path:
                    flash("Image 4 existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            works_tracking = db.session.execute(db.select(WorkTrack)).scalars().all()
            for work_tracking in works_tracking:
                if secure_filename(form.image_4.data.filename) == work_tracking.file_path:
                    flash("Image 4 existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            financial_requirements = db.session.execute(db.select(FinancialRequirement)).scalars().all()
            for financial_requirement in financial_requirements:
                if financial_requirement.file_path:
                    if secure_filename(form.image_5.data.filename) == financial_requirement.file_path:
                        flash(
                            "Image 4 existed at financial requirements in please upload instead or change the file name.")
                        return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            new_work_track = WorkTrack(file_path=form.image_4.data.filename, project_details_id=project_detail_id, percentage=form.percentage.data, project_id=requested_project_detail.project_id)
            db.session.add(new_work_track)
            db.session.commit()
            form.image_4.data.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                                secure_filename(form.image_4.data.filename)))
        if form.image_5.data:
            projects = db.session.execute(db.select(Project)).scalars().all()
            for project in projects:
                if secure_filename(form.image_5.data.filename) == project.file_path:
                    flash(f"Image 5 existed at projects please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            subcontractors = db.session.execute(db.select(SubContractor)).scalars().all()
            for subcontractor in subcontractors:
                if secure_filename(form.image_5.data.filename) == subcontractor.file_path:
                    flash(f"Image 5 existed at subcontractor please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            custody_settlements = db.session.execute(db.select(CustodySettlement)).scalars().all()
            for custody_settlement in custody_settlements:
                if secure_filename(form.image_5.data.filename) == custody_settlement.file_path:
                    flash(f"Image 5 existed at custody settlement  please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            employee_salaries = db.session.execute(db.select(EmployeesSalary)).scalars().all()
            for employee_salary in employee_salaries:
                if secure_filename(form.image_5.data.filename) == employee_salary.file_path:
                    flash(f"Image 5 existed at employee salary please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            inventory_movements = db.session.execute(db.select(InventoryMovement)).scalars().all()
            for inventory_movement in inventory_movements:
                if secure_filename(form.image_5.data.filename) == inventory_movement.file_path:
                    flash("Image 5 existed at inventory movement please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            cashes = db.session.execute(db.select(Cash)).scalars().all()
            for cash in cashes:
                if secure_filename(form.image_5.data.filename) == cash.file_path:
                    flash("Image 5 existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            works_tracking = db.session.execute(db.select(WorkTrack)).scalars().all()
            for work_tracking in works_tracking:
                if secure_filename(form.image_5.data.filename) == work_tracking.file_path:
                    flash("Image 5  existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            financial_requirements = db.session.execute(db.select(FinancialRequirement)).scalars().all()
            for financial_requirement in financial_requirements:
                if financial_requirement.file_path:
                    if secure_filename(form.image_5.data.filename) == financial_requirement.file_path:
                        flash( "Image 5 existed at financial requirements in please upload instead or change the file name.")
                        return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            new_work_track = WorkTrack(file_path=form.image_5.data.filename, project_details_id=project_detail_id, percentage=form.percentage.data, project_id=requested_project_detail.project_id)
            db.session.add(new_work_track)
            db.session.commit()
            form.image_5.data.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                                secure_filename(form.image_5.data.filename)))
        if form.image_6.data:
            projects = db.session.execute(db.select(Project)).scalars().all()
            for project in projects:
                if secure_filename(form.image_6.data.filename) == project.file_path:
                    flash(f"Image 6 existed at projects please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            subcontractors = db.session.execute(db.select(SubContractor)).scalars().all()
            for subcontractor in subcontractors:
                if secure_filename(form.image_6.data.filename) == subcontractor.file_path:
                    flash(f"Image 6 existed at subcontractor please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            custody_settlements = db.session.execute(db.select(CustodySettlement)).scalars().all()
            for custody_settlement in custody_settlements:
                if secure_filename(form.image_6.data.filename) == custody_settlement.file_path:
                    flash(f"Image 6 existed at custody settlement  please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            employee_salaries = db.session.execute(db.select(EmployeesSalary)).scalars().all()
            for employee_salary in employee_salaries:
                if secure_filename(form.image_6.data.filename) == employee_salary.file_path:
                    flash(f"Image 6 existed at employee salary please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            inventory_movements = db.session.execute(db.select(InventoryMovement)).scalars().all()
            for inventory_movement in inventory_movements:
                if secure_filename(form.image_6.data.filename) == inventory_movement.file_path:
                    flash("Image 6 existed at inventory movement please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            cashes = db.session.execute(db.select(Cash)).scalars().all()
            for cash in cashes:
                if secure_filename(form.image_6.data.filename) == cash.file_path:
                    flash("Image 6 existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            works_tracking = db.session.execute(db.select(WorkTrack)).scalars().all()
            for work_tracking in works_tracking:
                if secure_filename(form.image_6.data.filename) == work_tracking.file_path:
                    flash("Image 6 existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            financial_requirements = db.session.execute(db.select(FinancialRequirement)).scalars().all()
            for financial_requirement in financial_requirements:
                if financial_requirement.file_path:
                    if secure_filename(form.image_5.data.filename) == financial_requirement.file_path:
                        flash("Image 6 existed at financial requirements in please upload instead or change the file name.")
                        return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            new_work_track = WorkTrack(file_path=form.image_6.data.filename, project_details_id=project_detail_id, percentage=form.percentage.data, project_id=requested_project_detail.project_id)
            db.session.add(new_work_track)
            db.session.commit()
            form.image_6.data.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                                secure_filename(form.image_6.data.filename)))
        if form.image_7.data:
            projects = db.session.execute(db.select(Project)).scalars().all()
            for project in projects:
                if secure_filename(form.image_7.data.filename) == project.file_path:
                    flash(f"Image 7 existed at projects please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            subcontractors = db.session.execute(db.select(SubContractor)).scalars().all()
            for subcontractor in subcontractors:
                if secure_filename(form.image_7.data.filename) == subcontractor.file_path:
                    flash(f"Image 7 existed at subcontractor please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            custody_settlements = db.session.execute(db.select(CustodySettlement)).scalars().all()
            for custody_settlement in custody_settlements:
                if secure_filename(form.image_7.data.filename) == custody_settlement.file_path:
                    flash(f"Image 7 existed at custody settlement  please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            employee_salaries = db.session.execute(db.select(EmployeesSalary)).scalars().all()
            for employee_salary in employee_salaries:
                if secure_filename(form.image_7.data.filename) == employee_salary.file_path:
                    flash(f"Image 7 existed at employee salary please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            inventory_movements = db.session.execute(db.select(InventoryMovement)).scalars().all()
            for inventory_movement in inventory_movements:
                if secure_filename(form.image_7.data.filename) == inventory_movement.file_path:
                    flash("Image 7 existed at inventory movement please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            cashes = db.session.execute(db.select(Cash)).scalars().all()
            for cash in cashes:
                if secure_filename(form.image_7.data.filename) == cash.file_path:
                    flash("Image 7 existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            works_tracking = db.session.execute(db.select(WorkTrack)).scalars().all()
            for work_tracking in works_tracking:
                if secure_filename(form.image_7.data.filename) == work_tracking.file_path:
                    flash("Image 7 existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            financial_requirements = db.session.execute(db.select(FinancialRequirement)).scalars().all()
            for financial_requirement in financial_requirements:
                if financial_requirement.file_path:
                    if secure_filename(form.image_5.data.filename) == financial_requirement.file_path:
                        flash("Image 7 existed at financial requirements in please upload instead or change the file name.")
                        return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            new_work_track = WorkTrack(file_path=form.image_7.data.filename, project_details_id=project_detail_id, percentage=form.percentage.data, project_id=requested_project_detail.project_id)
            db.session.add(new_work_track)
            db.session.commit()
            form.image_7.data.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                                secure_filename(form.image_7.data.filename)))
        if form.image_8.data:
            projects = db.session.execute(db.select(Project)).scalars().all()
            for project in projects:
                if secure_filename(form.image_8.data.filename) == project.file_path:
                    flash(f"Image 8 existed at projects please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            subcontractors = db.session.execute(db.select(SubContractor)).scalars().all()
            for subcontractor in subcontractors:
                if secure_filename(form.image_8.data.filename) == subcontractor.file_path:
                    flash(f"Image 8 existed at subcontractor please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            custody_settlements = db.session.execute(db.select(CustodySettlement)).scalars().all()
            for custody_settlement in custody_settlements:
                if secure_filename(form.image_8.data.filename) == custody_settlement.file_path:
                    flash(f"Image 8 existed at custody settlement  please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            employee_salaries = db.session.execute(db.select(EmployeesSalary)).scalars().all()
            for employee_salary in employee_salaries:
                if secure_filename(form.image_8.data.filename) == employee_salary.file_path:
                    flash(f"Image 8 existed at employee salary please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            inventory_movements = db.session.execute(db.select(InventoryMovement)).scalars().all()
            for inventory_movement in inventory_movements:
                if secure_filename(form.image_8.data.filename) == inventory_movement.file_path:
                    flash("Image 8 existed at inventory movement please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            cashes = db.session.execute(db.select(Cash)).scalars().all()
            for cash in cashes:
                if secure_filename(form.image_8.data.filename) == cash.file_path:
                    flash("Image 8 existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            works_tracking = db.session.execute(db.select(WorkTrack)).scalars().all()
            for work_tracking in works_tracking:
                if secure_filename(form.image_8.data.filename) == work_tracking.file_path:
                    flash("Image 8 existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            financial_requirements = db.session.execute(db.select(FinancialRequirement)).scalars().all()
            for financial_requirement in financial_requirements:
                if financial_requirement.file_path:
                    if secure_filename(form.image_5.data.filename) == financial_requirement.file_path:
                        flash(
                            "Image 8 existed at financial requirements in please upload instead or change the file name.")
                        return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
            new_work_track = WorkTrack(file_path=form.image_8.data.filename, project_details_id=project_detail_id, percentage=form.percentage.data, project_id=requested_project_detail.project_id)
            db.session.add(new_work_track)
            db.session.commit()
            form.image_8.data.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                                secure_filename(form.image_8.data.filename)))
        flash("Works tracking has been added successfully")
        return redirect(url_for('display_project', project_id=requested_project_detail.project_id))
    return render_template('add_works_tracking.html', form=form)


@app.route("/delete_works_tracking/<int:project_detail_id>")
@login_required
@delete_works_tracking
def delete_works_tracking(project_detail_id):
    requested_project_detail = db.get_or_404(ProjectDetail, project_detail_id)
    works_tracking = db.session.execute(db.select(WorkTrack).where(WorkTrack.project_details_id == project_detail_id)).scalars().all()
    for work_tracking in works_tracking:
        try:
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                                   secure_filename(work_tracking.file_path)))
        except FileNotFoundError:
            pass
        db.session.delete(work_tracking)
        db.session.commit()
    flash("Works tracking has been deleted successfully")
    return redirect(url_for('display_project', project_id=requested_project_detail.project_id))


@app.route("/display_works_tracking", methods=["GET", "POST"])
def display_works_tracking():
    form = InputWorksTracking()
    if form.validate_on_submit():
        requested_project = db.session.execute(
            db.select(Project).where(Project.track_number == form.tracking_number.data)).scalar()
        if requested_project:
            requested_works_tracking = db.session.execute(db.select(WorkTrack).where(WorkTrack.project_id == requested_project.id)).scalars().all()
            if requested_works_tracking:
                return render_template("works_tracking.html", form=form, project=requested_project )
            else:
                flash("Works tracking has not been uploaded yet")
                return render_template("works_tracking.html", form=form)
        else:
            flash("Tracking number incorrect, please try again.")

    return render_template("works_tracking.html", form=form, year=year)


@app.route("/add_financial_requirement", methods=["GET", "POST"])
@login_required
@add_financial_requirement
def add_financial_requirement():
    form = AddFinancialRequirement()
    if form.validate_on_submit():
        file = form.excel_file.data
        projects = db.session.execute(db.select(Project)).scalars().all()
        for project in projects:
            if project.file_path:
                if secure_filename(file.filename) == project.file_path:
                    flash(f"This file existed at projects please upload instead or change the file name.")
                    return redirect(url_for('add_financial_requirement'))
        subcontractors = db.session.execute(db.select(SubContractor)).scalars().all()
        for subcontractor in subcontractors:
            if subcontractor.file_path:
                if secure_filename(file.filename) == subcontractor.file_path:
                    flash(f"This file existed at subcontractor please upload instead or change the file name.")
                    return redirect(url_for('add_financial_requirement'))
        custody_settlements = db.session.execute(db.select(CustodySettlement)).scalars().all()
        for custody_settlement in custody_settlements:
            if custody_settlement.file_path:
                if secure_filename(file.filename) == custody_settlement.file_path:
                    flash(f"This file existed at custody settlement  please upload instead or change the file name.")
                    return redirect(url_for('add_financial_requirement'))
        employee_salaries = db.session.execute(db.select(EmployeesSalary)).scalars().all()
        for employee_salary in employee_salaries:
            if employee_salary.file_path:
                if secure_filename(file.filename) == employee_salary.file_path:
                    flash(f"This file existed at employee salary please upload instead or change the file name.")
                    return redirect(url_for('add_financial_requirement'))
        inventory_movements = db.session.execute(db.select(InventoryMovement)).scalars().all()
        for inventory_movement in inventory_movements:
            if inventory_movement.file_path:
                if secure_filename(file.filename) == inventory_movement.file_path:
                    flash("This file existed at inventory movement please upload instead or change the file name.")
                    return redirect(url_for('add_financial_requirement'))
        cashes = db.session.execute(db.select(Cash)).scalars().all()
        for cash in cashes:
            if cash.file_path:
                if secure_filename(file.filename) == cash.file_path:
                    flash("This file existed at cash in please upload instead or change the file name.")
                    return redirect(url_for('add_financial_requirement'))
        expenses_details = db.session.execute(db.select(ExpenseDetail)).scalars().all()
        for expenses_detail in expenses_details:
            if expenses_detail.file_path:
                if secure_filename(file.filename) == expenses_detail.file_path:
                    flash("This file existed at expenses detail in please upload instead or change the file name.")
                    return redirect(url_for('add_financial_requirement'))
        works_tracking = db.session.execute(db.select(WorkTrack)).scalars().all()
        for work_tracking in works_tracking:
            if work_tracking.file_path:
                if secure_filename(file.filename) == work_tracking.file_path:
                    flash("This file existed at works tracking in please upload instead or change the file name.")
                    return redirect(url_for('add_financial_requirement'))
        financial_requirements = db.session.execute(db.select(FinancialRequirement)).scalars().all()
        for financial_requirement in financial_requirements:
            if financial_requirement.file_path:
                if secure_filename(file.filename) == financial_requirement.file_path:
                    flash("This file existed at financial requirements in please upload instead or change the file name.")
                    return redirect(url_for('add_financial_requirement'))
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                               secure_filename(file.filename)))
        new_financial_requirement = FinancialRequirement(name="متطلبات مالية", total=form.total.data, date=datetime.datetime.now().strftime("%d/%m/%Y"), file_path=file.filename)
        db.session.add(new_financial_requirement)
        db.session.commit()
        all_users = db.session.execute(db.select(User).where(User.display_all_financial_requirements == 2)).scalars().all()
        if all_users:
            for user in all_users:
                password = "hvra dvjy tgfg ooxb"
                msg = MIMEMultipart()
                msg["From"] = 'technoteam1980@gmail.com'
                msg["To"] = user.email
                msg["Subject"] = "Financial Requirement"
                file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],secure_filename(file.filename))
                with open(file_path, 'rb') as file:
                    # Attach the file with filename to the email
                    msg.attach(MIMEApplication(file.read(), Name=new_financial_requirement.file_path))
                with SMTP("Smtp.gmail.com:587") as connection:
                    connection.starttls()
                    connection.login(user=msg["From"], password=password)
                    connection.sendmail(from_addr=msg["From"], to_addrs=msg["To"], msg=msg.as_string())
        flash("Financial Requirement Has Been Added Successfully and  Successfully sent your messages")
        return redirect(url_for('add_financial_requirement'))
    return render_template("add_financial_requirement.html", form=form)


@app.route("/delete_financial_requirement/<int:financial_requirement_id>")
@login_required
@delete_financial_requirement
def delete_financial_requirement(financial_requirement_id):
    requested_financial_requirement = db.get_or_404(FinancialRequirement, financial_requirement_id)
    file_name = requested_financial_requirement.file_path
    try:
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                               secure_filename(file_name)))
    except FileNotFoundError:
        pass
    except TypeError:
        pass
    except PermissionError:
        pass
    db.session.delete(requested_financial_requirement)
    db.session.commit()
    flash("Financial Requirement Has Been Deleted Successfully.")
    return redirect(url_for('display_all_financial_requirements'))


@app.route("/display_all_financial_requirements")
@login_required
@display_all_financial_requirements
def display_all_financial_requirements():
    financial_requirements = db.session.execute(db.select(FinancialRequirement)).scalars().all()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(financial_requirements, page=page, css_framework='bootstrap5', total=len(financial_requirements), search=search,
                            record_name='All Financial Requirements')
    all_financial_requirements_paginate = db.paginate(db.select(FinancialRequirement), page=page, per_page=10, error_out=False)
    return render_template("display_all_financial_requirements.html", financial_requirements=all_financial_requirements_paginate, pagination=pagination)


@app.route("/search_financial_requirements", methods=["GET", "POST"])
@login_required
def search_financial_requirements():
    if request.method == "POST":
        search_text = request.form["input_name"]
        search_format = "%{}%".format(search_text)
        if db.session.execute(db.select(FinancialRequirement).where(FinancialRequirement.name.like(search_format))).scalars().all():
            results = db.session.execute(db.select(FinancialRequirement).where(FinancialRequirement.name.like(search_format))).scalars()
            return render_template("display_all_financial_requirements.html",financial_requirements=results, search=True)
        elif db.session.execute(db.select(FinancialRequirement).where(FinancialRequirement.date.like(search_format))).scalars().all():
            results = db.session.execute(db.select(FinancialRequirement).where(FinancialRequirement.date.like(search_format))).scalars()
            return render_template("display_all_financial_requirements.html", financial_requirements=results, search=True)
        else:
            flash("There are no results.")
            return render_template("display_all_financial_requirements.html",search=True)


@app.route("/add_subcontractor_requirement", methods=["GET", "POST"])
@login_required
@add_subcontractor_requirement
def add_subcontractor_requirement():
    form = AddSubcontractorRequirement()
    projects = db.session.execute(db.select(Project)).scalars().all()
    list_projects = []
    for project in projects:
        list_projects.append((project.id, project.project_name))
    form.project_name.choices = list_projects
    form.subcontractor_name.choices = ["مقاول نجارة", "مقاول محارة", "مقاول كهرباء", "مقاول سباكة", "مقاول رخام",
                                       "مقاول سيراميك", "مقاول نقاشة", "مقاول حمام سباحة", "مقاول حدادة","مقاول تكييفات"]
    if form.validate_on_submit():
        subcontractor_requirements = db.session.execute(db.select(SubcontractorRequirement)).scalars().all()
        for subcontractor_requirement in subcontractor_requirements:
            if subcontractor_requirement.project_id == int(form.project_name.data) and subcontractor_requirement.subcontractor_name == form.subcontractor_name.data:
                flash("That Subcontractor Requirement Existed Please Add Another One or Edit the Percentage of Existed One")
                return redirect(url_for('add_subcontractor_requirement'))
        requested_project = db.get_or_404(Project, form.project_name.data)
        if form.percentage.data < 100:
            new_subcontractor_requirement = SubcontractorRequirement(project_id=int(form.project_name.data),
                                                                     project_name=requested_project.project_name,
                                                                     subcontractor_name=form.subcontractor_name.data,
                                                                     percentage=form.percentage.data,
                                                                     date=datetime.datetime.now().strftime("%d/%m/%Y"),
                                                                     status="Current")
            db.session.add(new_subcontractor_requirement)
            db.session.commit()
        else:
            new_subcontractor_requirement = SubcontractorRequirement(project_id=int(form.project_name.data),
                                                                     project_name=requested_project.project_name,
                                                                     subcontractor_name=form.subcontractor_name.data,
                                                                     percentage=form.percentage.data,
                                                                     date=datetime.datetime.now().strftime("%d/%m/%Y"),
                                                                     status="Final")
            db.session.add(new_subcontractor_requirement)
            db.session.commit()
        all_users = db.session.execute(
            db.select(User).where(User.display_subcontractor_requirements == 2)).scalars().all()
        if all_users:
            for user in all_users:
                password = "hvra dvjy tgfg ooxb"
                msg = MIMEMultipart()
                msg["From"] = 'technoteam1980@gmail.com'
                msg["To"] = user.email
                msg["Subject"] = "Add Subcontractor Requirement"
                all_message = f"Project Name is: {requested_project.project_name}\nSubcontractor Name is: {new_subcontractor_requirement.subcontractor_name}\nExecution Percentage is: {new_subcontractor_requirement.percentage}%\nStatus is: {new_subcontractor_requirement.status}\nDate is: {new_subcontractor_requirement.date}"
                msg.attach(MIMEText(all_message, 'plain'))
                with SMTP("Smtp.gmail.com:587") as connection:
                    connection.starttls()
                    connection.login(user=msg["From"], password=password)
                    connection.sendmail(from_addr=msg["From"], to_addrs=msg["To"], msg=msg.as_string())
        flash("That Subcontractor Requirement Has Been Added Successfully")
        return redirect(url_for('add_subcontractor_requirement'))
    return render_template("add_subcontractor_requirement.html", form=form)


@app.route("/display_all_subcontractors_requirements")
@login_required
@display_subcontractor_requirements
def display_all_subcontractors_requirements():
    all_subcontractors_requirements = db.session.execute(db.select(SubcontractorRequirement)).scalars().all()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(all_subcontractors_requirements, page=page, css_framework='bootstrap5',
                            total=len(all_subcontractors_requirements), search=search,
                            record_name='All Financial Requirements')
    all_subcontractors_requirements_paginate = db.paginate(db.select(SubcontractorRequirement), page=page, per_page=10, error_out=False)
    return render_template("display_all_subcontractors_requirements.html", subcontractors_requirements=all_subcontractors_requirements_paginate, pagination=pagination, year=year)


@app.route("/search_subcontractors_requirements", methods=["GET", "POST"])
@login_required
def search_subcontractors_requirements():
    all_subcontractors_requirements = db.session.execute(db.select(SubcontractorRequirement)).scalars().all()
    if request.method == "POST":
        search_text = request.form["input_name"]
        search_format = "%{}%".format(search_text)
        if db.session.execute(
                db.select(SubcontractorRequirement).where(SubcontractorRequirement.project_name.like(search_format))).scalars().all():
            results = db.session.execute(
                db.select(SubcontractorRequirement).where(SubcontractorRequirement.project_name.like(search_format))).scalars()
            return render_template("display_all_subcontractors_requirements.html", subcontractors_requirements=results,
                                   search=True)
        elif db.session.execute(
                db.select(SubcontractorRequirement).where(SubcontractorRequirement.subcontractor_name.like(search_format))).scalars().all():
            results = db.session.execute(
                db.select(SubcontractorRequirement).where(SubcontractorRequirement.subcontractor_name.like(search_format))).scalars()
            return render_template("display_all_subcontractors_requirements.html", subcontractors_requirements=results,
                                   search=True)
        elif db.session.execute(
                db.select(SubcontractorRequirement).where(SubcontractorRequirement.status.like(search_format))).scalars().all():
            results = db.session.execute(
                db.select(SubcontractorRequirement).where(SubcontractorRequirement.status.like(search_format))).scalars()
            return render_template("display_all_subcontractors_requirements.html", subcontractors_requirements=results,
                                   search=True)
        elif db.session.execute(
                db.select(SubcontractorRequirement).where(SubcontractorRequirement.date.like(search_format))).scalars().all():
            results = db.session.execute(
                db.select(SubcontractorRequirement).where(SubcontractorRequirement.date.like(search_format))).scalars()
            return render_template("display_all_subcontractors_requirements.html", subcontractors_requirements=results,
                                   search=True)
        else:
            flash("There are no results.")
            return redirect(url_for('display_all_subcontractors_requirements'))


@app.route("/edit_subcontractor_requirement/<int:subcontractor_requirement_id>", methods=["GET", "POST"])
@login_required
@edit_subcontractor_requirement
def edit_subcontractor_requirement(subcontractor_requirement_id):
    requested_subcontractor_requirement = db.get_or_404(SubcontractorRequirement, subcontractor_requirement_id)
    form = AddSubcontractorRequirement(project_name=requested_subcontractor_requirement.project_name, percentage=requested_subcontractor_requirement.percentage,
                                       subcontractor_name=requested_subcontractor_requirement.subcontractor_name)

    projects = db.session.execute(db.select(Project)).scalars().all()
    list_projects = []
    for project in projects:
        list_projects.append((project.id, project.project_name))
    form.project_name.choices = list_projects
    form.subcontractor_name.choices = ["مقاول نجارة", "مقاول محارة", "مقاول كهرباء", "مقاول سباكة", "مقاول رخام",
                                       "مقاول سيراميك", "مقاول نقاشة", "مقاول حمام سباحة", "مقاول حدادة",
                                       "مقاول تكييفات"]
    if form.validate_on_submit():
        db.session.delete(requested_subcontractor_requirement)
        db.session.commit()
        subcontractor_requirements = db.session.execute(db.select(SubcontractorRequirement)).scalars().all()
        for subcontractor_requirement in subcontractor_requirements:
            if subcontractor_requirement.project_id == int(
                    form.project_name.data) and subcontractor_requirement.subcontractor_name == form.subcontractor_name.data:
                flash(
                    "That Subcontractor Requirement Existed Please Add Another One or Edit the Percentage of Existed One")
                return render_template("add_subcontractor_requirement.html", form=form, edit=True)
        requested_project = db.get_or_404(Project, int(form.project_name.data))
        if form.percentage.data < 100:
            new_subcontractor_requirement = SubcontractorRequirement(project_id=int(form.project_name.data),
                                                                     project_name=requested_project.project_name,
                                                                     subcontractor_name=form.subcontractor_name.data,
                                                                     percentage=form.percentage.data,
                                                                     date=datetime.datetime.now().strftime("%d/%m/%Y"),
                                                                     status="Current")
            db.session.add(new_subcontractor_requirement)
            db.session.commit()
        else:
            new_subcontractor_requirement = SubcontractorRequirement(project_id=int(form.project_name.data),
                                                                     project_name=requested_project.project_name,
                                                                     subcontractor_name=form.subcontractor_name.data,
                                                                     percentage=form.percentage.data,
                                                                     date=datetime.datetime.now().strftime("%d/%m/%Y"),
                                                                     status="Final")
            db.session.add(new_subcontractor_requirement)
            db.session.commit()
        all_users = db.session.execute(
            db.select(User).where(User.display_subcontractor_requirements == 2)).scalars().all()
        if all_users:
            for user in all_users:
                password = "hvra dvjy tgfg ooxb"
                msg = MIMEMultipart()
                msg["From"] = 'technoteam1980@gmail.com'
                msg["To"] = user.email
                msg["Subject"] = "Edit Subcontractor Requirement"
                all_message = f"Project Name is: {requested_project.project_name}\nSubcontractor Name is: {new_subcontractor_requirement.subcontractor_name}\nExecution Percentage is: {new_subcontractor_requirement.percentage}%\nStatus is: {new_subcontractor_requirement.status}\nDate is: {new_subcontractor_requirement.date}"
                msg.attach(MIMEText(all_message, 'plain'))
                with SMTP("Smtp.gmail.com:587") as connection:
                    connection.starttls()
                    connection.login(user=msg["From"], password=password)
                    connection.sendmail(from_addr=msg["From"], to_addrs=msg["To"], msg=msg.as_string())
        flash("That Subcontractor Requirement Has Been Edited Successfully")
        return redirect(url_for('display_all_subcontractors_requirements'))
    return render_template("add_subcontractor_requirement.html", form=form, edit=True)


@app.route("/delete_subcontractor_requirement/<int:subcontractor_requirement_id>")
@login_required
@delete_subcontractor_requirement
def delete_subcontractor_requirement(subcontractor_requirement_id):
    requested_subcontractor_requirement = db.get_or_404(SubcontractorRequirement, subcontractor_requirement_id)
    db.session.delete(requested_subcontractor_requirement)
    requested_project = db.session.execute(db.select(Project).where(Project.id == requested_subcontractor_requirement.project_id)).scalar()
    all_users = db.session.execute(
        db.select(User).where(User.display_subcontractor_requirements == 2)).scalars().all()
    if all_users:
        for user in all_users:
            password = "hvra dvjy tgfg ooxb"
            msg = MIMEMultipart()
            msg["From"] = 'technoteam1980@gmail.com'
            msg["To"] = user.email
            msg["Subject"] = "Delete Subcontractor Requirement"
            all_message = f"Project Name is: {requested_project.project_name}\nSubcontractor Name is: {requested_subcontractor_requirement.subcontractor_name}\nExecution Percentage is: {requested_subcontractor_requirement.percentage} %\nStatus is: {requested_subcontractor_requirement.status}\nDate is: {requested_subcontractor_requirement.date}"
            msg.attach(MIMEText(all_message, 'plain'))
            with SMTP("Smtp.gmail.com:587") as connection:
                connection.starttls()
                connection.login(user=msg["From"], password=password)
                connection.sendmail(from_addr=msg["From"], to_addrs=msg["To"], msg=msg.as_string())
    db.session.commit()
    flash("Subcontractor Requirement Has Been Deleted Successfully")
    return redirect(url_for('display_all_subcontractors_requirements'))


@app.route("/add_purchase_requirement", methods=["GET", "POST"])
@login_required
@add_purchase_requirement
def add_purchase_requirement():
    form = AddPurchaseRequirement()
    projects = db.session.execute(db.select(Project)).scalars().all()
    list_projects = []
    for project in projects:
        list_projects.append((project.id, project.project_name))
    form.project_name.choices = list_projects
    if form.validate_on_submit():
        purchase_requirements = db.session.execute(db.select(PurchaseRequirement)).scalars().all()
        for purchase_requirement in purchase_requirements:
            if purchase_requirement.project_id == int(form.project_name.data):
                flash("That Project Has Been Existed Please Add Other Purchase Requirement.")
                return redirect(url_for('add_purchase_requirement'))
        requested_project = db.session.execute(db.select(Project).where(Project.id == int(form.project_name.data))).scalar()
        new_purchase_requirement = PurchaseRequirement(project_id=requested_project.id, project_name=requested_project.project_name, date=datetime.datetime.now().strftime("%d/%m/%Y"), status="Follow Up")
        db.session.add(new_purchase_requirement)
        db.session.commit()
        all_users = db.session.execute(
            db.select(User).where(User.display_purchase_requirements == 2)).scalars().all()
        if all_users:
            for user in all_users:
                password = "hvra dvjy tgfg ooxb"
                msg = MIMEMultipart()
                msg["From"] = 'technoteam1980@gmail.com'
                msg["To"] = user.email
                msg["Subject"] = "Add Purchase Requirement"

                all_message = f"Please Check this Purchase Requirement it is added now \nProject Name is: {requested_project.project_name}\nStatus is: {new_purchase_requirement.status}\nDate is: {new_purchase_requirement.date}"
                msg.attach(MIMEText(all_message, 'plain'))
                with SMTP("Smtp.gmail.com:587") as connection:
                    connection.starttls()
                    connection.login(user=msg["From"], password=password)
                    connection.sendmail(from_addr=msg["From"], to_addrs=msg["To"], msg=msg.as_string())
        flash("Purchase Requirement has been added successfully.")
        return redirect("add_purchase_requirement")
    return render_template("add_purchase_requirement.html", form=form)


@app.route("/display_all_purchase_requirements")
@login_required
@display_purchase_requirements
def display_all_purchase_requirements():
    purchase_requirements = db.session.execute(db.select(PurchaseRequirement)).scalars().all()
    for purchase_requirement in purchase_requirements:
        requested_project = db.session.execute(db.select(Project).where(Project.id == purchase_requirement.project_id)).scalar()
        purchase_requirement.project_name = requested_project.project_name
        db.session.commit()
        purchase_requirement_items = db.session.execute(db.select(PurchaseRequirementItem).where(PurchaseRequirementItem.purchase_requirement_id == purchase_requirement.id)).scalars().all()
        completed_requirement_item = db.session.execute(db.select(PurchaseRequirementItem).where(PurchaseRequirementItem.purchase_requirement_id == purchase_requirement.id, PurchaseRequirementItem.status == "Done")).scalars().all()
        if len(purchase_requirement_items) == len(completed_requirement_item):
            purchase_requirement.status = "Done"
            db.session.commit()
        else:
            purchase_requirement.status = "Follow Up"
            db.session.commit()

    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(purchase_requirements, page=page, css_framework='bootstrap5',
                            total=len(purchase_requirements), search=search,
                            record_name='All Purchase Requirements')
    all_purchase_requirements_paginate = db.paginate(db.select(PurchaseRequirement), page=page, per_page=10,error_out=False)

    return render_template("display_all_purchase_requirements.html", purchase_requirements=all_purchase_requirements_paginate, pagination=pagination)


@app.route("/edit_purchase_requirement/<int:purchase_requirement_id>", methods=["GET", "POST"])
@login_required
def edit_purchase_requirement(purchase_requirement_id):
    requested_purchase_requirement = db.get_or_404(PurchaseRequirement, purchase_requirement_id)
    form = AddPurchaseRequirement(project_name=requested_purchase_requirement.id)
    projects = db.session.execute(db.select(Project)).scalars().all()
    list_projects = []
    for project in projects:
        list_projects.append((project.id, project.project_name))
    form.project_name.choices = list_projects
    if form.validate_on_submit():
        purchase_requirements = db.session.execute(db.select(PurchaseRequirement)).scalars().all()
        for purchase_requirement in purchase_requirements:
            if purchase_requirement.project_id == int(form.project_name.data):
                flash("That Purchase Requirement Has Been Existed Please Edit Other Purchase Requirement.")
                return redirect(url_for('edit_purchase_requirement', purchase_requirement_id=requested_purchase_requirement.id))
        requested_purchase_requirement.project_id = int(form.project_name.data)
        requested_purchase_requirement.project_name = form.project_name.data
        db.session.commit()
        all_users = db.session.execute(
            db.select(User).where(User.display_purchase_requirements == 2)).scalars().all()
        requested_project = db.session.execute(db.select(Project).where(Project.id == requested_purchase_requirement.project_id)).scalar()
        if all_users:
            for user in all_users:
                password = "hvra dvjy tgfg ooxb"
                msg = MIMEMultipart()
                msg["From"] = 'technoteam1980@gmail.com'
                msg["To"] = user.email
                msg["Subject"] = "Edit Purchase Requirement"
                all_message = f"Please Check this Purchase Requirement it is edited now \nProject Name is: {requested_project.project_name}\nStatus is: {requested_purchase_requirement.status}\nDate is: {requested_purchase_requirement.date}"
                msg.attach(MIMEText(all_message, 'plain'))
                with SMTP("Smtp.gmail.com:587") as connection:
                    connection.starttls()
                    connection.login(user=msg["From"], password=password)
                    connection.sendmail(from_addr=msg["From"], to_addrs=msg["To"], msg=msg.as_string())
        flash("Purchase Requirement Has Been Edited Successfully.")
        return redirect(url_for('display_all_purchase_requirements'))
    return render_template("add_purchase_requirement.html", form=form, edit=True)


@app.route("/search_purchase_requirement", methods=["GET", "POST"])
@login_required
def search_purchase_requirement():
    if request.method == "POST":
        search_text = request.form["input_name"]
        search_format = "%{}%".format(search_text)
        if db.session.execute(db.select(PurchaseRequirement).where(PurchaseRequirement.project_name.like(search_format))).scalars().all():
            results = db.session.execute(db.select(PurchaseRequirement).where(PurchaseRequirement.project_name.like(search_format))).scalars()
            return render_template("display_all_purchase_requirements.html",purchase_requirements=results, search=True)
        elif db.session.execute(db.select(PurchaseRequirement).where(PurchaseRequirement.date.like(search_format))).scalars().all():
            results = db.session.execute(db.select(PurchaseRequirement).where(PurchaseRequirement.date.like(search_format))).scalars()
            return render_template("display_all_purchase_requirements.html",purchase_requirements=results, search=True)
        else:
            flash("There Are No Results.")
            return redirect(url_for('display_all_purchase_requirements'))


@app.route("/delete_purchase_requirement/<int:purchase_requirement_id>")
@login_required
def delete_purchase_requirement(purchase_requirement_id):
    requested_purchase_requirement = db.get_or_404(PurchaseRequirement, purchase_requirement_id)
    purchase_requirement_items = db.session.execute(db.select(PurchaseRequirementItem).where(PurchaseRequirementItem.purchase_requirement_id == purchase_requirement_id)).scalars().all()
    if purchase_requirement_items:
        for purchase_requirement_item in purchase_requirement_items:
            db.session.delete(purchase_requirement_item)
            db.session.commit()
    db.session.delete(requested_purchase_requirement)
    db.session.commit()
    flash("Purchase Requirement Has Been Deleted Successfully.")
    return redirect(url_for('display_all_purchase_requirements'))


@app.route("/add_purchase_requirement_item/<int:purchase_requirement_id>", methods=["GET", "POST"])
@login_required
def add_purchase_requirement_item(purchase_requirement_id):
    purchase_requirement = db.get_or_404(PurchaseRequirement, purchase_requirement_id)
    form = AddPurchaseRequirementItem()
    if form.validate_on_submit():
        new_purchase_requirement_item = PurchaseRequirementItem(name=form.name.data, purchase_requirement_id=purchase_requirement_id, status="Follow Up")
        db.session.add(new_purchase_requirement_item)
        db.session.commit()
        purchase_requirements = db.session.execute(db.select(PurchaseRequirement)).scalars().all()
        for purchase_requirement in purchase_requirements:
            requested_project = db.session.execute(
                db.select(Project).where(Project.id == purchase_requirement.project_id)).scalar()
            purchase_requirement.project_name = requested_project.project_name
            db.session.commit()
            purchase_requirement_items = db.session.execute(db.select(PurchaseRequirementItem).where(
                PurchaseRequirementItem.purchase_requirement_id == purchase_requirement.id)).scalars().all()
            completed_requirement_item = db.session.execute(db.select(PurchaseRequirementItem).where(
                PurchaseRequirementItem.purchase_requirement_id == purchase_requirement.id,
                PurchaseRequirementItem.status == "Done")).scalars().all()
            if len(purchase_requirement_items) == len(completed_requirement_item):
                purchase_requirement.status = "Done"
                db.session.commit()
            else:
                purchase_requirement.status = "Follow Up"
                db.session.commit()
        flash("Item Has Been Added Successfully.")
        return redirect(url_for('add_purchase_requirement_item', purchase_requirement_id=purchase_requirement.id))
    return render_template("add_purchase_requirement_item.html", purchase_requirement=purchase_requirement, form=form, add=True)


@app.route("/display_purchase_requirement_items/<int:purchase_requirement_id>")
@login_required
def display_purchase_requirement_items(purchase_requirement_id):
    purchase_requirement = db.get_or_404(PurchaseRequirement, purchase_requirement_id)
    purchase_requirements = db.session.execute(db.select(PurchaseRequirement)).scalars().all()
    for purchase_requirement in purchase_requirements:
        requested_project = db.session.execute(
            db.select(Project).where(Project.id == purchase_requirement.project_id)).scalar()
        purchase_requirement.project_name = requested_project.project_name
        db.session.commit()
        purchase_requirement_items = db.session.execute(db.select(PurchaseRequirementItem).where(
            PurchaseRequirementItem.purchase_requirement_id == purchase_requirement.id)).scalars().all()
        completed_requirement_item = db.session.execute(db.select(PurchaseRequirementItem).where(
            PurchaseRequirementItem.purchase_requirement_id == purchase_requirement.id,
            PurchaseRequirementItem.status == "Done")).scalars().all()
        if len(purchase_requirement_items) == len(completed_requirement_item):
            purchase_requirement.status = "Done"
            db.session.commit()
        else:
            purchase_requirement.status = "Follow Up"
            db.session.commit()
    return render_template("add_purchase_requirement_item.html", purchase_requirement=purchase_requirement, display=True)


@app.route("/edit_purchase_requirement_item/<int:purchase_requirement_item_id>", methods=["GET", "POST"])
@login_required
def edit_purchase_requirement_item(purchase_requirement_item_id):
    requested_purchase_requirement_item = db.get_or_404(PurchaseRequirementItem, purchase_requirement_item_id)
    requested_purchase_requirement = db.session.execute(db.select(PurchaseRequirement).where(PurchaseRequirement.id == requested_purchase_requirement_item.purchase_requirement_id)).scalar()
    form = AddPurchaseRequirementItem(name=requested_purchase_requirement_item.name)
    if form.validate_on_submit():
        requested_purchase_requirement_item.name = form.name.data
        db.session.commit()
        flash("Item Has Been Edited Successfully.")
        return redirect(url_for('display_purchase_requirement_items', purchase_requirement_id=requested_purchase_requirement_item.purchase_requirement_id))
    return render_template("add_purchase_requirement_item.html", purchase_requirement=requested_purchase_requirement, form=form, edit=True)


@app.route("/delete_purchase_requirement_item/<int:purchase_requirement_item_id>")
@login_required
def delete_purchase_requirement_item(purchase_requirement_item_id):
    requested_purchase_requirement_item = db.get_or_404(PurchaseRequirementItem, purchase_requirement_item_id)
    db.session.delete(requested_purchase_requirement_item)
    db.session.commit()
    flash("Item Has Been Deleted Successfully.")
    return redirect(url_for('display_purchase_requirement_items',purchase_requirement_id=requested_purchase_requirement_item.purchase_requirement_id))


@app.route("/complete_purchase_requirement_item/<int:purchase_requirement_item_id>")
@login_required
def complete_purchase_requirement_item(purchase_requirement_item_id):
    requested_purchase_requirement_item = db.get_or_404(PurchaseRequirementItem, purchase_requirement_item_id)
    requested_purchase_requirement_item.status = "Done"
    db.session.commit()
    return redirect(url_for("display_purchase_requirement_items", purchase_requirement_id=requested_purchase_requirement_item.purchase_requirement_id))


@app.route("/add_operation_expense", methods=["GET", "POST"])
@login_required
@operating_expense_cash_out
def add_operation_expense():
    form = OperationExpensesCashOut()
    form.cost_name.choices = ["حمام سباحة", "نجارة", "سباكة", "سيراميك", "حدادة", "كهرباء", "نقاشة", "رخام", "محارة",
                              "تكييفات", "مصروفات نثرية"]
    projects = db.session.execute(db.select(Project)).scalars().all()
    projects_list = []
    for project in projects:
        projects_list.append(project.project_name)
    form.project_name.choices = projects_list
    if form.validate_on_submit():
        requested_project = db.session.execute(db.select(Project).where(Project.project_name == form.project_name.data)).scalar()
        new_cash_out = Cash(description=form.description.data, debit=0,
                            credit=form.total.data, balance=0,
                            date=datetime.datetime.now().strftime("%d/%m/%Y"),
                            contra_account=f"Ope Expenses {requested_project.project_name}")
        db.session.add(new_cash_out)
        db.session.commit()
        new_project_cost = ProjectCost(description=form.description.data, total=form.total.data,
                                       date=datetime.datetime.now().strftime("%d/%m/%Y"),
                                       project_id=requested_project.id,
                                       cost_name=form.cost_name.data,
                                       user_id=current_user.id)
        db.session.add(new_project_cost)
        db.session.commit()
        new_operation_expense = OperationExpense(description=form.description.data, total=form.total.data, date=datetime.datetime.now().strftime("%d/%m/%Y"),cash_id=new_cash_out.id,project_id=requested_project.id, project_cost_id=new_project_cost.id )
        db.session.add(new_operation_expense)
        db.session.commit()
        flash("Operation Expense Has Been Added Successfully.")
        return redirect(url_for('add_operation_expense'))
    return render_template('add_operation_expense.html', form=form)


@app.route("/display_all_operation_expenses")
@login_required
@display_all_operating_expenses
def display_all_operation_expenses():
    operation_expenses = db.session.execute(db.select(OperationExpense)).scalars().all()
    total_expenses = 0
    for operation_expense in operation_expenses:
        total_expenses += operation_expense.total
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(operation_expenses, page=page, css_framework='bootstrap5', total=len(operation_expenses), search=search,
                            record_name='All Operating Expenses')
    all_operation_expenses_paginate = db.paginate(db.select(OperationExpense), page=page, per_page=10, error_out=False)
    return render_template("display_all_operation_expenses.html",operation_expenses=all_operation_expenses_paginate, pagination=pagination )


@app.route("/search_operation_expenses", methods=["GET", "POST"])
@login_required
def search_operation_expenses():
    if request.method == "POST":
        search_text = request.form["input_name"]
        search_format = "%{}%".format(search_text)
        if db.session.execute(db.select(OperationExpense).where(OperationExpense.description.like(search_format))).scalars().all():
            results = db.session.execute(db.select(OperationExpense).where(OperationExpense.description.like(search_format))).scalars()
            return render_template("display_all_operation_expenses.html",operation_expenses=results, search=True)
        elif db.session.execute(db.select(OperationExpense).where(OperationExpense.date.like(search_format))).scalars().all():
            results = db.session.execute(
                db.select(OperationExpense).where(OperationExpense.date.like(search_format))).scalars()
            return render_template("display_all_operation_expenses.html", operation_expenses=results, search=True)
        else:
            flash("There are no results.")
            redirect(url_for('display_all_operation_expenses'))


@app.route("/edit_operation_expense/<int:operation_expense_id>", methods=["GET", "POST"])
@login_required
@edit_operating_expense
def edit_operation_expense(operation_expense_id):
    requested_operation_expense = db.get_or_404(OperationExpense, operation_expense_id)
    requested_cash_out = db.session.execute(db.select(Cash).where(Cash.id == requested_operation_expense.cash_id)).scalar()
    requested_project_cost = db.session.execute(db.select(ProjectCost).where(ProjectCost.id == requested_operation_expense.project_cost_id)).scalar()
    requested_project = db.session.execute(db.select(Project).where(Project.id == requested_operation_expense.project_id)).scalar()
    form = OperationExpensesCashOut(description=requested_operation_expense.description, project_name=requested_project.project_name, cost_name=requested_project_cost.cost_name, total=requested_operation_expense.total)
    form.cost_name.choices = ["حمام سباحة", "نجارة", "سباكة", "سيراميك", "حدادة", "كهرباء", "نقاشة", "رخام", "محارة",
                              "تكييفات", "مصروفات نثرية"]
    projects = db.session.execute(db.select(Project)).scalars().all()
    projects_list = []
    for project in projects:
        projects_list.append(project.project_name)
    form.project_name.choices = projects_list
    if form.validate_on_submit():
        requested_project = db.session.execute(db.select(Project).where(Project.project_name == form.project_name.data)).scalar()
        requested_operation_expense.description = form.description.data
        requested_operation_expense.total = form.total.data
        requested_operation_expense.project_id = requested_project.id
        requested_cash_out.description = form.description.data
        requested_cash_out.credit = form.total.data
        requested_cash_out.contra_account = f"Ope Expenses {requested_project.project_name}"
        requested_project_cost.description = form.description.data
        requested_project_cost.total = form.total.data
        requested_project_cost.project_id = requested_project.id
        requested_project_cost.cost_name = form.cost_name.data
        requested_project_cost.user_id = current_user.id
        db.session.commit()
        flash("Operating Expense Has Been Edited Successfully.")
        return redirect(url_for('display_all_operation_expenses'))
    return render_template('add_operation_expense.html', form=form, edit=True)


@app.route("/delete_operation_expense/<int:operation_expense_id>")
@login_required
@delete_operating_expense
def delete_operation_expense(operation_expense_id):
    requested_operation_expense = db.get_or_404(OperationExpense, operation_expense_id)
    requested_cash_out = db.session.execute(
        db.select(Cash).where(Cash.id == requested_operation_expense.cash_id)).scalar()
    requested_project_cost = db.session.execute(
        db.select(ProjectCost).where(ProjectCost.id == requested_operation_expense.project_cost_id)).scalar()
    file_name = requested_operation_expense.file_path
    try:
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"],
                               secure_filename(file_name)))
    except FileNotFoundError:
        pass
    except TypeError:
        pass
    except PermissionError:
        pass
    db.session.delete(requested_operation_expense)
    db.session.delete(requested_cash_out)
    db.session.delete(requested_project_cost)
    db.session.commit()
    flash('Operating expense Has Been Deleted Successfully')
    return redirect(url_for('display_all_operation_expenses'))



        # @app.route("/edit_purchase_order_item/<int:commercial_offer_item_id>", methods=["GET", "POST"])
    # @login_requiredadd_works_track
    # def edit_commercial_offer_item(commercial_offer_item_id):
    #     requested_commercial_offer_item = db.get_or_404(CommercialOfferItem, commercial_offer_item_id)
    #     requested_commercial_offer = db.session.execute(db.select(CommercialOffer).where(
    #         CommercialOffer.id == requested_commercial_offer_item.commercial_offer_id)).scalar()
    #     form = AddItem(serial_number=requested_commercial_offer_item.serial_number,
    #                    quantity=requested_commercial_offer_item.quantity,
    #                    description=requested_commercial_offer_item.description,
    #                    commercial_offer=requested_commercial_offer,
    #                    user=current_user, unit_price=requested_commercial_offer_item.unit_price)
    #     if form.validate_on_submit():
    #         requested_commercial_offer_item.serial_number = form.serial_number.data
    #         requested_commercial_offer_item.description = form.description.data
    #         requested_commercial_offer_item.quantity = form.quantity.data
    #         requested_commercial_offer_item.unit_price = form.unit_price.data
    #         requested_commercial_offer_item.commercial_offer = requested_commercial_offer
    #         requested_commercial_offer_item.user = current_user
    #         requested_commercial_offer_item.total = form.unit_price.data * form.quantity.data
    #         db.session.commit()
    #         return redirect(url_for('display_commercial_offer', commercial_offer_id=requested_commercial_offer.id))
    #     return render_template('edit_commercial_offer_item.html', form=form,
    #                            commercial_offer=requested_commercial_offer, logged_in=current_user.is_authenticated)
    #

if __name__ == "__main__":
    app.run(debug=True, port=5001)

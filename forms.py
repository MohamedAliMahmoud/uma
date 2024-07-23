from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, SelectField, FloatField, FileField
from wtforms.validators import DataRequired, Optional
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post


# Create a form to register new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a form to login existing users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


class AddProject(FlaskForm):
    project_name = StringField("Project Name", validators=[DataRequired()])
    description = CKEditorField("Description", validators=[DataRequired()])
    customer_name = StringField("Customer Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AddProjectDetails(FlaskForm):
    item_name = SelectField("Item Name", validators=[DataRequired()])
    description = CKEditorField("Description", validators=[DataRequired()])
    total = FloatField("Total", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AddDataSubcontractors(FlaskForm):
    subcontractor_name = SelectField("Subcontractor Name", validators=[DataRequired()])
    description = CKEditorField("Description", validators=[DataRequired()])
    total = FloatField("Total", validators=[DataRequired()])
    submit = SubmitField("Submit")


class DisplaySubcontractorsAccount(FlaskForm):
    subcontractor_name = SelectField("Subcontractor Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AddCustodySettlement(FlaskForm):
    cost_name = SelectField("Cost Item", validators=[DataRequired()])
    project_id = SelectField("Project Id", validators=[DataRequired()])
    description = CKEditorField("Description", validators=[DataRequired()])
    total = FloatField("Total", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AddCustodyCashOut(FlaskForm):
    description = CKEditorField("Description", validators=[DataRequired()])
    total = FloatField("Total", validators=[DataRequired()])
    submit = SubmitField("Submit")


class EditCustodyName(FlaskForm):
    name = StringField("Employee Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


class EmployeeDetails(FlaskForm):
    name = StringField("Employee Name", validators=[DataRequired()])
    job_title = StringField("Job Title", validators=[DataRequired()])
    contact_number = IntegerField("Contact Number", validators=[DataRequired()])
    submit = SubmitField("Submit")


class SalaryCashOut(FlaskForm):
    employee_name = SelectField("Employee Name", validators=[DataRequired()])
    description = CKEditorField("Description", validators=[DataRequired()])
    salary = FloatField("Total", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AddExpense(FlaskForm):
    expense_name = StringField("Expense Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ExpenseCashOut(FlaskForm):
    expense_name = SelectField("Expense Name", validators=[DataRequired()])
    description = CKEditorField("Description", validators=[DataRequired()])
    total = FloatField("Total", validators=[DataRequired()])
    submit = SubmitField("Submit")


class SalaryCashOut(FlaskForm):
    employee_name = SelectField("Employee Name", validators=[DataRequired()])
    description = CKEditorField("Description", validators=[DataRequired()])
    salary = FloatField("Total", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AddInventoryItem(FlaskForm):
    item_name = StringField("Item Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ImportInventoryMovement(FlaskForm):
    description = CKEditorField("Description", validators=[DataRequired()])
    quantity = FloatField("Qty ", validators=[DataRequired()])
    unit_price = FloatField("Unit Price ", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ExportInventoryMovement(FlaskForm):
    project_id = SelectField("Project Id", validators=[DataRequired()])
    cost_name = SelectField("Cost Item", validators=[DataRequired()])
    description = CKEditorField("Description", validators=[DataRequired()])
    quantity = FloatField("Qty ", validators=[DataRequired()])
    unit_price = FloatField("Unit Price ", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CashIn(FlaskForm):
    description = CKEditorField("Description", validators=[DataRequired()])
    amount = FloatField("Total Amount ", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UploadFile(FlaskForm):
    file_name = FileField("Select File", validators=[DataRequired()])
    submit = SubmitField("Submit")


class Permissions(FlaskForm):
    cash = SelectField("Cash", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    add_cash = SelectField("Add Cash In", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    display_cash_account = SelectField("Display Cash Account", validators=[DataRequired()],
                                       choices=[(1, "Lock"), (2, "Unlock")])
    edit_cash_in = SelectField("Edit Cash In", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    delete_cash_in = SelectField("Delete Cash In", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    projects = SelectField("Projects", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    add_project = SelectField("Add Project", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    edit_project = SelectField("Edit Project", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    display_all_projects = SelectField("Display All Projects", validators=[DataRequired()],
                                       choices=[(1, "Lock"), (2, "Unlock")])
    display_project = SelectField("Display Project", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    add_project_details = SelectField("Add Project Details", validators=[DataRequired()],
                                      choices=[(1, "Lock"), (2, "Unlock")])
    edit_project_details = SelectField("Edit Project Details", validators=[DataRequired()],
                                       choices=[(1, "Lock"), (2, "Unlock")])
    delete_project_details = SelectField("Delete Project Details", validators=[DataRequired()],
                                         choices=[(1, "Lock"), (2, "Unlock")])
    add_works_tracking = SelectField("Add Works Tracking", validators=[DataRequired()],
                                     choices=[(1, "Lock"), (2, "Unlock")])
    delete_works_tracking = SelectField("Delete Works Tracking", validators=[DataRequired()],
                                        choices=[(1, "Lock"), (2, "Unlock")])
    add_subcontractor_opening_balance = SelectField("Add Subcontractor Opening Balance", validators=[DataRequired()],
                                                    choices=[(1, "Lock"), (2, "Unlock")])
    add_subcontractor_cash_out = SelectField("Add Subcontractor Cash Out", validators=[DataRequired()],
                                             choices=[(1, "Lock"), (2, "Unlock")])
    display_subcontractor_account = SelectField("Display Subcontractor Account", validators=[DataRequired()],
                                                choices=[(1, "Lock"), (2, "Unlock")])
    edit_subcontractor_account = SelectField("Edit Subcontractor Account", validators=[DataRequired()],
                                             choices=[(1, "Lock"), (2, "Unlock")])
    delete_subcontractor_account = SelectField("Delete Subcontractor Account", validators=[DataRequired()],
                                               choices=[(1, "Lock"), (2, "Unlock")])
    display_project_cost = SelectField("Display Project Cost", validators=[DataRequired()],
                                       choices=[(1, "Lock"), (2, "Unlock")])
    custody = SelectField("Custody", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    display_my_custody = SelectField("Display my Custody", validators=[DataRequired()],
                                     choices=[(1, "Lock"), (2, "Unlock")])
    display_all_custodes = SelectField("Display All Custodes", validators=[DataRequired()],
                                       choices=[(1, "Lock"), (2, "Unlock")])
    display_employee_custody = SelectField("Display Employee Custody", validators=[DataRequired()],
                                           choices=[(1, "Lock"), (2, "Unlock")])
    edit_employee_name = SelectField("Edit Employee Name", validators=[DataRequired()],
                                     choices=[(1, "Lock"), (2, "Unlock")])
    add_custody_settlement = SelectField("Add Custody Settlement", validators=[DataRequired()],
                                         choices=[(1, "Lock"), (2, "Unlock")])
    add_custody_cash_out = SelectField("Add Custody Cash Out", validators=[DataRequired()],
                                       choices=[(1, "Lock"), (2, "Unlock")])
    edit_custody_cash_out = SelectField("Edit Custody Cash Out", validators=[DataRequired()],
                                        choices=[(1, "Lock"), (2, "Unlock")])
    delete_custody_cash_out = SelectField("Delete Custody Cash Out", validators=[DataRequired()],
                                          choices=[(1, "Lock"), (2, "Unlock")])
    edit_custody_settlement = SelectField("Edit Custody Settlement", validators=[DataRequired()],
                                          choices=[(1, "Lock"), (2, "Unlock")])
    delete_custody_settlement = SelectField("Delete Custody Settlement", validators=[DataRequired()],
                                            choices=[(1, "Lock"), (2, "Unlock")])
    payroll = SelectField("Payroll", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    add_employee = SelectField("Add Employee", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    display_all_employees = SelectField("Display All Employees", validators=[DataRequired()],
                                        choices=[(1, "Lock"), (2, "Unlock")])
    salary_cash_out = SelectField("Salary Cash Out", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    display_employee_salary = SelectField("Display Employee Salary", validators=[DataRequired()],
                                          choices=[(1, "Lock"), (2, "Unlock")])
    edit_employee_details = SelectField("Edit Employee Details", validators=[DataRequired()],
                                        choices=[(1, "Lock"), (2, "Unlock")])
    edit_salary = SelectField("Edit Salary", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    delete_salary = SelectField("Delete Salary", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    inventory = SelectField("Inventory", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    add_item = SelectField("Add Item", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    display_all_items = SelectField("Display All Items", validators=[DataRequired()],
                                    choices=[(1, "Lock"), (2, "Unlock")])
    display_item_movements = SelectField("Display Item Movement", validators=[DataRequired()],
                                         choices=[(1, "Lock"), (2, "Unlock")])
    edit_item = SelectField("Edit Item", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    import_item = SelectField("Import Item", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    export_item = SelectField("Export Item", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    edit_item_movement = SelectField("Edit Item Movement", validators=[DataRequired()],
                                     choices=[(1, "Lock"), (2, "Unlock")])
    delete_item_movement = SelectField("Delete Item Movement", validators=[DataRequired()],
                                       choices=[(1, "Lock"), (2, "Unlock")])
    expenses = SelectField("Expense", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    add_expense = SelectField("Add Expense", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    display_all_expenses = SelectField("Display All Administrative Expenses", validators=[DataRequired()],
                                       choices=[(1, "Lock"), (2, "Unlock")])
    expense_cash_out = SelectField("Administrative Expense Cash Out", validators=[DataRequired()],
                                   choices=[(1, "Lock"), (2, "Unlock")])
    display_expense_details = SelectField("Display Administrative Expense Detail", validators=[DataRequired()],
                                          choices=[(1, "Lock"), (2, "Unlock")])
    edit_expense = SelectField("Edit Expense", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    edit_expense_cash_out = SelectField("Edit Administrative Expense Cash Out", validators=[DataRequired()],
                                        choices=[(1, "Lock"), (2, "Unlock")])
    delete_expense_cash_out = SelectField("Delete Administrative Expense Cash Out", validators=[DataRequired()],
                                          choices=[(1, "Lock"), (2, "Unlock")])
    operating_expense_cash_out = SelectField("Operating Expense Cash Out", validators=[DataRequired()],
                                             choices=[(1, "Lock"), (2, "Unlock")])
    display_all_operating_expenses = SelectField("Display All Operating Expenses", validators=[DataRequired()],
                                                 choices=[(1, "Lock"), (2, "Unlock")])
    edit_operating_expense = SelectField("Edit Operating Expense", validators=[DataRequired()],
                                          choices=[(1, "Lock"), (2, "Unlock")])
    delete_operating_expense = SelectField("Delete Operating Expense", validators=[DataRequired()],
                                            choices=[(1, "Lock"), (2, "Unlock")])
    notifications = SelectField("Notifications", validators=[DataRequired()],
                                choices=[(1, "Lock"), (2, "Unlock")])
    add_financial_requirement = SelectField("Add Financial Requirement", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    display_all_financial_requirements = SelectField("Display All Financial Requirements", validators=[DataRequired()],
                                                     choices=[(1, "Lock"), (2, "Unlock")])
    delete_financial_requirement = SelectField("Delete Financial_Requirement", validators=[DataRequired()],
                                               choices=[(1, "Lock"), (2, "Unlock")])
    add_subcontractor_requirement = SelectField("Add Subcontractor Requirement", validators=[DataRequired()],
                                                choices=[(1, "Lock"), (2, "Unlock")])
    display_subcontractor_requirements = SelectField("Display Subcontractor Requirements", validators=[DataRequired()],
                                                     choices=[(1, "Lock"), (2, "Unlock")])
    edit_subcontractor_requirement = SelectField("Edit Subcontractor Requirement", validators=[DataRequired()],
                                                 choices=[(1, "Lock"), (2, "Unlock")])
    delete_subcontractor_requirement = SelectField("Delete Subcontractor Requirement", validators=[DataRequired()],
                                                   choices=[(1, "Lock"), (2, "Unlock")])
    add_purchase_requirement = SelectField("Add Purchase Requirement", validators=[DataRequired()],
                                            choices=[(1, "Lock"), (2, "Unlock")])
    display_purchase_requirements = SelectField("Display Purchase Requirements", validators=[DataRequired()],
                                                   choices=[(1, "Lock"), (2, "Unlock")])
    upload_file = SelectField("Upload File", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    download_file = SelectField("Download File", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    delete_file = SelectField("Delete File", validators=[DataRequired()], choices=[(1, "Lock"), (2, "Unlock")])
    submit = SubmitField("Submit")


class WorksTrack(FlaskForm):
    image_1 = FileField("Select image", validators=[DataRequired()])
    image_2 = FileField("Select image", validators=[Optional()])
    image_3 = FileField("Select image", validators=[Optional()])
    image_4 = FileField("Select image", validators=[Optional()])
    image_5 = FileField("Select image", validators=[Optional()])
    image_6 = FileField("Select image", validators=[Optional()])
    image_7 = FileField("Select image", validators=[Optional()])
    image_8 = FileField("Select image", validators=[Optional()])
    percentage = FloatField("Input Percentage From 1 to 100", validators=[DataRequired()])
    submit = SubmitField("Submit")


class InputWorksTracking(FlaskForm):
    tracking_number = PasswordField("Please insert your tracking number")


class AddFinancialRequirement(FlaskForm):
    total = FloatField("Total", validators=[DataRequired()])
    excel_file = FileField("Select Excel File", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AddSubcontractorRequirement(FlaskForm):
    project_name = SelectField("Project Name", validators=[DataRequired()])
    subcontractor_name = SelectField("Subcontractor Name", validators=[DataRequired()])
    percentage = FloatField("Input Percentage From 1 to 100", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AddPurchaseRequirement(FlaskForm):
    project_name = SelectField("Project Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AddPurchaseRequirementItem(FlaskForm):
    name = StringField("Item Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


class OperationExpensesCashOut(FlaskForm):
    project_name = SelectField("Project Name", validators=[DataRequired()])
    cost_name = SelectField("Cost Item", validators=[DataRequired()])
    description = CKEditorField("Item Description", validators=[DataRequired()])
    total = FloatField("Total", validators=[DataRequired()])
    submit = SubmitField("Submit")


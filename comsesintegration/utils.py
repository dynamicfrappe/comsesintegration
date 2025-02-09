import frappe


# get cost center from Cost Center Mapping
def get_cost_center(hotel):
    return frappe.get_cached_value("Cost Center Mapping", hotel, "cost_center")

#get account from Accounts Mapping
def get_account(account):
    return frappe.get_cached_value("Accounts Mapping", account, "erp_account")



def remove_brackets(number):
    number_str = str(number)
    if "(" in number_str and ")" in number_str:
        number_str = number_str.replace("(", "").replace(")", "")

    cleaned_number = float(number_str or 0)

    return cleaned_number

def get_account_name(account):
    sql = f"select erp_account , debit ,credit from `tabAccounts Mapping` where comsys_account like '%{account}%'"
    data = frappe.db.sql(sql, as_dict=True)
    # get department_difference_account from Account Integration Settings
    if len(data) > 0:
        return {
            "exist":True,
            "account":data[0].erp_account,
            "debit":data[0].debit,
            "credit":data[0].credit
        }
    return {
        "exist":False
    }


def get_dept_difference_account():
    department_difference_account = frappe.get_cached_value("Account Integration Settings", None, "department_difference_account")
    return department_difference_account

def get_customer_diff_account():
    customer_difference_account = frappe.get_cached_value("Account Integration Settings", None, "customer_difference_account")
    return customer_difference_account

def get_employee_diff_account():
    employee_difference_account = frappe.get_cached_value("Account Integration Settings", None, "employee_difference_account")
    return employee_difference_account

def get_employee_account():
    employee_account = frappe.get_cached_value("Account Integration Settings", None, "employee_account")
    return employee_account


# Copyright (c) 2025, kazem and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import json
import requests
from datetime import datetime
from erpnext import get_default_company
from frappe.model.document import Document




class ComsysEmployeeInvoice(Document):
	pass


@frappe.whitelist()
def send_invoice(doc , child):
	doc = json.loads(doc)
	child = json.loads(child)
	res = send_emoloyee_inovice(child.get("employee_code") , doc.get("posting_date") , child.get("total"))
	return res

	
	
def send_emoloyee_inovice(employee , posting_date , total):
	
	domain = frappe.get_active_domains()
	if "Dynamic HR" not in domain:
		frappe.msgprint(_("Please Active the Domain"))
		return False
	
	from dynamic_hr_v15.dynamic_hr.doctype.monthly_salaries.monthly_salaries import get_year_and_month


	nova_id = frappe.get_value("Employee",employee,"attendance_device_id")
	setting = frappe.get_doc("Account Integration Settings")
	nova_setting = frappe.get_doc("HR Intgration Setting",{"company":get_default_company()})

	if setting.element_id:
		url = f"{nova_setting.url}PayrollEmpElementVal/Save"
		date = get_next_year_and_month(posting_date)
		year_month = get_year_and_month(date.get("year") , date.get("month"))
		payload = json.dumps({
			"id": 0, #Default Value
			"employeeCode": int(nova_id),
			"employeeId": 0, #Default Value
			"payTemplateId": 1, #Default Value
			"elementId": int(setting.element_id), 
			"elementModeId": 2, #Default Value
			"monthId": year_month.get("month"),
			"yearId": year_month.get("year"),
			"notes": f"Service On {posting_date}",
			"elemVal": str(total),
			"transDate": posting_date
		})
		headers = {
			'Content-Type': 'application/json',
			'Authorization': f'Bearer {nova_setting.token}'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		if response.status_code == 204:
			frappe.throw("لا يوجد بيانات لهذا الشهر")
			return

		if response.status_code == 401:
			frappe.throw("لم يتم تسجيل الدخول " )
			return
		
		if response.status_code == 404:
			frappe.throw("Internal Server Error")
			return

		if response.status_code != 200:
			frappe.log_error("get_payroll_totals", response.text)
			frappe.throw(response.text)

		print(response)
		return True

def get_next_year_and_month(date_str):

	date_obj = datetime.strptime(str(date_str), "%Y-%m-%d")
	next_year = date_obj.year
	month_name = date_obj.strftime("%B")
	return {"year": next_year, "month": month_name}
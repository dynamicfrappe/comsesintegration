# Copyright (c) 2025, kazem and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import pandas as pd
from frappe.utils import cstr, get_site_name
from comsesintegration.utils import remove_brackets , get_employee_diff_account , get_employee_account

class JournalEntryforEmployee(Document):
	@frappe.whitelist()
	def upload(self):
		# read the excel file
		sitename = frappe.local.site
		df = pd.read_excel(sitename + self.sheet)
		for index, row in df.iterrows():
			print("asd+++++++++++++", row)
			if not pd.isnull(row.iloc[7]) and not pd.isnull(row.iloc[8]):
				try:
					self.append("accounts", {
						"employee": str(row.iloc[7]) if not pd.isnull(row.iloc[7]) else "",
						"amount": remove_brackets(str(row.iloc[8])) if not pd.isnull(row.iloc[8]) else "",
					})
				except:
					pass
		self.save()


	@frappe.whitelist()
	def create_jv(self):
		total_depit = 0
		difference_account = get_employee_diff_account()
		journal_entry = frappe.new_doc("Journal Entry")
		journal_entry.posting_date = self.date
		default_receivable_account = get_employee_account()
		for account in self.accounts:
			employee = frappe.db.sql(f"select name from tabEmployee where employee_name = '{account.employee}'",as_dict=1)
			if len(employee) > 0:
				journal_entry.append("accounts", {
					"account": default_receivable_account,
					"party_type":"Employee",
					"party": employee[0].name,
					"debit_in_account_currency": account.amount,
					"cost_center":self.cost_center
				})
				total_depit += account.amount
		journal_entry.append("accounts", {
			"account": difference_account,
			"credit_in_account_currency": total_depit,
			"cost_center":self.cost_center
		})
		journal_entry.save(ignore_permissions=True)
		self.journal_entry = journal_entry
		self.save()
		frappe.msgprint(f"Journal Entry for Employee {journal_entry.name} Created Successfully")
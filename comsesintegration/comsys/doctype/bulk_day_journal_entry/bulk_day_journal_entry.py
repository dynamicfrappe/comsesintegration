# Copyright (c) 2024, kazem and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import pandas as pd
from frappe.utils import cstr, get_site_name
from comsesintegration.utils import remove_brackets,get_account_name ,get_dept_difference_account

class BulkDayjournalEntry(Document):
	@frappe.whitelist()
	def upload(self):
		print("from upload function")
		# read the excel file
		sitename = frappe.local.site
		df = pd.read_excel(sitename + self.sheet)
		for index, row in df.iterrows():
			if not pd.isnull(row.iloc[0]) and not pd.isnull(row.iloc[1]):
				try:
					amount = remove_brackets(str(row.iloc[1]))
					if isinstance(amount, (int, float)):
						print("asd55",amount)
						if "total" not in str(row.iloc[0]).lower() and row.iloc[0] != "":
							self.append("accounts", {
								"account": str(row.iloc[0]) if not pd.isnull(row.iloc[0]) else "",
								"amount": remove_brackets(str(row.iloc[1])),
							})
				except:
					pass
		self.save()

	@frappe.whitelist()
	def create_jv(self):
		total_depit = 0
		total_credit = 0
		difference_account = get_dept_difference_account()
		journal_entry = frappe.new_doc("Journal Entry")
		journal_entry.posting_date = self.date
		for account in self.accounts:
			erp_account = get_account_name(account.account)
			print(erp_account)
			if erp_account["exist"]:
				if erp_account["debit"] == 1:
					journal_entry.append("accounts", {
						"account": erp_account["account"],
						"debit_in_account_currency": account.amount,
						"cost_center":self.cost_center
					})
					total_depit += account.amount
				elif erp_account["credit"] == 1:
					journal_entry.append("accounts", {
						"account": erp_account["account"],
						"credit_in_account_currency": account.amount,
						"cost_center":self.cost_center
					})
					total_credit += account.amount
		if total_depit > total_credit:
			journal_entry.append("accounts", {
				"account": difference_account,
				"credit_in_account_currency": total_depit - total_credit,
			})
		elif total_credit > total_depit:
			journal_entry.append("accounts", {
				"account": difference_account,
				"debit_in_account_currency": total_credit - total_depit,
			})
		journal_entry.save(ignore_permissions=True)
		self.journal_entry = journal_entry.name
		self.save(ignore_permissions=True)
		frappe.msgprint("Journal Entry Created Successfully")
		return journal_entry


# Copyright (c) 2024, kazem and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import pandas as pd
from frappe.utils import cstr, get_site_name
from comsesintegration.utils import remove_brackets,get_customer_diff_account
from erpnext import get_default_company

class JournalEntryforcustomer(Document):
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
						"customer": str(row.iloc[7]) if not pd.isnull(row.iloc[7]) else "",
						"amount": remove_brackets(str(row.iloc[8])) if not pd.isnull(row.iloc[8]) else "",
					})
				except:
					pass
		self.save()

	@frappe.whitelist()
	def create_jv(self):
		total_depit = 0
		difference_account = get_customer_diff_account()
		journal_entry = frappe.new_doc("Journal Entry")
		journal_entry.posting_date = self.date
		company = get_default_company()
		default_receivable_account = frappe.db.get_value("Company", company, "default_receivable_account")
		for account in self.accounts:
			if frappe.db.exists("Customer", account.customer):
				journal_entry.append("accounts", {
					"account": default_receivable_account,
					"party_type":"Customer",
					"party": account.customer,
					"debit_in_account_currency": account.amount,
					"cost_center":self.cost_center
				})
				total_depit += account.amount
			else:
				customer = self.create_customer(account.customer)
				journal_entry.append("accounts", {
					"account": default_receivable_account,
					"party_type":"Customer",
					"party": customer,
					"debit_in_account_currency": account.amount,
					"cost_center":self.cost_center
				})
				total_depit += account.amount

		journal_entry.append("accounts", {
			"account": difference_account,
			"credit_in_account_currency": total_depit,
		})
		journal_entry.save(ignore_permissions=True)
		self.journal_entry = journal_entry
		self.save()
		frappe.msgprint(f"Journal Entry for Customer {journal_entry.name} Created Successfully")
	

	def create_customer(self,customer_name):
		customer = frappe.new_doc("Customer")
		customer.customer_name = customer_name
		customer.save(ignore_permissions = True)
		return customer.name

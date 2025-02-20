// Copyright (c) 2025, kazem and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Comsys Employee Invoice", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on("Comsys invoice", {
	send:function(frm, cdt, cdn){
		child = locals[cdt][cdn];

		if (child.total <= 0 || child.total == null){
			frappe.msgprint("Total must be greater than 0");
			return;

		}
		
		if (child.sent == 0){
			frappe.call({
				method: "comsesintegration.comsys.doctype.comsys_employee_invoice.comsys_employee_invoice.send_invoice",
				args: {
					doc: frm.doc,
					child: child
				},
				callback: function(r) {
					if(r.message) {
										
						if (r.message == true){
							
							console.log("Invoice sent");
							
							frappe.model.set_value(cdt, cdn, "sent", 1);

							frm.refresh_field("table_oaas");
							frm.dirty();
							frm.save();
							frappe.msgprint("Invoice sent");
						}
					}
				}
			});	
		}
		else
		{
			frappe.msgprint("Invoice already sent");
		}
	},
});


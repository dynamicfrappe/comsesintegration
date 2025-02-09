// Copyright (c) 2025, kazem and contributors
// For license information, please see license.txt

frappe.ui.form.on("Journal Entry for Employee", {
// 	refresh(frm) {

// 	},
    upload:(frm)=>{
        if (frm.doc.sheet)  {
            frappe.call({
                method:"upload",
                doc:frm.doc
            })
        }
    },
    create_journal_entry:(frm)=>{
        if (frm.doc.docstatus == 1 && frm.doc.journal_entry == null){
        frappe.call({
            method:"create_jv",
            doc:frm.doc
        })
    }
    }
});

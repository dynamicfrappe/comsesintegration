// Copyright (c) 2024, kazem and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bulk Day journal Entry", {
// 	refresh(frm) {

// 	},
    upload:(frm)=>{
        if (frm.doc.sheet)  {
            console.log("hello world")
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

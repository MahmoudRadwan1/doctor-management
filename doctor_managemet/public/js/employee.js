// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee', {
	setup: function(frm) {
        check_customer_field(frm)
	},
	designation: function(frm) {
        check_customer_field(frm)
	}
});

let check_customer_field = function (frm) {
    if (frm.doc.designation == 'Doctor' || frm.doc.designation == 'Nurse' || frm.doc.designation == 'Driver') {
        frm.set_df_property('customer', 'reqd', true);
    } else {
        frm.set_df_property('customer', 'reqd', false);
        frm.set_value('customer', '')
    }
    frm.refresh_field('customer');
}
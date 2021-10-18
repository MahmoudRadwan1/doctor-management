// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance', {
	setup: function(frm) {
        check_shift_type(frm)
	},
	designation: function(frm) {
        check_shift_type(frm)
	},
	on_submit: function() {
        cur_frm.reload_doc()
    }
});

let check_shift_type = function (frm) {
    if (frm.doc.status == 'Present') {
        frm.set_df_property('shift', 'reqd', true);
    } else {
        frm.set_df_property('shift', 'reqd', false);
        frm.set_value('shift', '')
    }
    frm.refresh_field('shift');
}
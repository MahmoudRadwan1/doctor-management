// Copyright (c) 2021, MiM and contributors
// For license information, please see license.txt

frappe.ui.form.on('Component Option', {
	type: function(frm) {
        check_reqd_field(frm)
	}
});


let check_reqd_field = function (frm) {
    if (frm.doc.type == 'Grade') {
        frm.set_df_property('grade', 'reqd', true);
    } else {
        frm.set_df_property('grade', 'reqd', false);
        frm.set_value('grade', '')
    }

    if (frm.doc.type == 'Years of Service') {
        frm.set_df_property('number_of_years', 'reqd', true);
    } else {
        frm.set_df_property('number_of_years', 'reqd', false);
        frm.set_value('number_of_years', '')
    }
    frm.refresh_many(['grade','number_of_years']);
}

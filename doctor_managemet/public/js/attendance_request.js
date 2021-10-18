// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance Request', {
	reason: function(frm) {
		if(frm.doc.reason == 'Site Visit'){
			frm.set_df_property('customer', 'reqd', true);
			frm.set_df_property('shift', 'reqd', true);
		}
		else{
			frm.set_df_property('customer', 'reqd', false);
			frm.set_df_property('shift', 'reqd', false);
			frm.set_value('customer','')
			frm.set_value('shift','')
		}
		frm.refresh_many (['customer','shift']);
	}
});

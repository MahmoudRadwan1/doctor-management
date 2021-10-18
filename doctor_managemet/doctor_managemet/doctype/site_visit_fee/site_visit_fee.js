// Copyright (c) 2021, MiM and contributors
// For license information, please see license.txt

frappe.ui.form.on('Site Visit Fee', {
	setup: function (frm) {
		frm.set_query("salary_component","component_detail", function () {
			return {
				filters: {
					type: "earning"
				}
			}
		});
	}
});


frappe.ui.form.on('Component Detail', {
	amount: function(frm) {
		calculate_total(frm)
	},
	component_detail_remove:function(frm){
		calculate_total(frm)
	}
});


var calculate_total = function (frm) {
	var tbl = cur_frm.doc.component_detail || [];
	var total = 0;
	var expatriate_total = 0;
	var all_components_total = 0;
	for (var i = 0; i < tbl.length; i++) {
		if(tbl[i].component_option !='Expatriate'){
			total += tbl[i].amount
		}
		else{
			expatriate_total += tbl[i].amount
		}

		all_components_total += tbl[i].amount
	}
	cur_frm.set_value("total", total)
	cur_frm.set_value("expatriate_total", expatriate_total)
	cur_frm.set_value("all_components_total", all_components_total)
	refresh_many(['total','expatriate_total','all_components_total'])
}
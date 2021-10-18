# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, nowdate, cint,date_diff, add_days, flt
from erpnext.hr.doctype.employee.employee import is_holiday
from erpnext.hr.utils import validate_dates
from calendar import monthrange
from datetime import datetime, timedelta
from dateutil import relativedelta

def create_additional_salaries(doc, method=None):
    att_list = frappe.db.get_list("Attendance",
			filters={"attendance_request":doc.name},
			fields=['name','customer','employee','attendance_date'],
            order_by='attendance_date',
		)
    if att_list:
        for item in att_list:
            components = frappe.db.get_list("Component Detail",filters={"parent":item["customer"]},fields=["salary_component","amount"])
            if components:
                for component in components:
                    additional_salary = frappe.new_doc('Additional Salary')
                    additional_salary.employee = item["employee"]
                    additional_salary.salary_component = component["salary_component"]
                    additional_salary.amount = component["amount"]
                    additional_salary.payroll_date = item["attendance_date"]
                    additional_salary.from_attendance = item["name"]
                    additional_salary.type = "Earning"
                    additional_salary.company = doc.company
                    additional_salary.submit()
            else:
                frappe.throw(_("Please Add Site Visit Fee for This Customer first"))

def create_additional_salary(doc, method=None):
        if doc.status =="Present":
            # components = frappe.db.get_list("Component Detail",filters={"parent":doc.customer,"shift":doc.shift},fields=["salary_component","expatriate_only","amount"])
            years = 0
            service_details = {}
            emp_customer,designation, grade = "", "", ""
            emp_data = frappe.db.get_values('Employee', filters={"name":doc.employee}, fieldname=["expatriate", "designation","grade","date_of_joining","experience_years"], as_dict=True)

            if emp_data:
                emp_data=emp_data[0]
                grade = emp_data["grade"]
                expatriate = emp_data["expatriate"]
                date_of_joining = emp_data["date_of_joining"]

                # if not emp_data["date_of_joining"]:
                #     frappe.throw(_("Complete Date of Joinig in Employee ."))
                # else:
                    # service_details = get_dates_diff(date_of_joining,getdate())
                    # years = service_details["years"]
                years = flt(emp_data["experience_years"])

                if not emp_data["designation"]:
                    frappe.throw(_("Complete designation in Employee ."))
                else:
                    designation = emp_data["designation"]
            components = frappe.db.sql("""
                    select shift ,salary_component,TRIM(SUBSTRING_INDEX(component_option,'-',1)) component_option ,
                        case when SUBSTRING_INDEX(component_option,'-',1) in ('Years of Service','Grade') then TRIM(SUBSTRING_INDEX(component_option,'-',-1)) else '' end  val 
                        , amount
                        from `tabSite Visit Fee` S
                            INNER JOIN 
                                `tabComponent Detail` C
                                on S.`name` = C.parent  
                                where S.customer = %s
                                    and S.shift = %s
                                    and S.designation = %s
                                    and S.docstatus = 1
                            order by val desc 
                """,(doc.customer,doc.shift,designation), as_dict=True,debug=False)
            # frappe.throw(str(years))


            workday = {"Day and Half":1.5,"Day and Quarter (1.25)":1.25, "Full Day":1,"Three Half (0.75)":0.75, "Half Day":0.5,"Quarter":0.25}
            day_percentage = flt(workday.get(doc.work_day,1))

            yearsofservicesadmission = False
            years_val = 0
            if components:
                for component in components:
                    if component["component_option"]=="Resident" and expatriate == 1:
                        continue
                    if component["component_option"]=="Expatriate" and expatriate == 0:
                        continue
                    elif component["component_option"]=="Grade" and component["val"]!=grade:
                        continue
                    elif component["component_option"]=="Years of Service":
                        if years == 0:
                            continue
                        elif years < cint(component["val"]):
                            continue
                        elif years >= cint(component["val"]) and years_val == 0:
                            years_val = cint(cint(component["val"]))
                        elif years >= cint(component["val"]) and years_val != cint(component["val"]):
                            continue


                    # frappe.msgprint(str(component["component_option"])+"======"+str(component["val"])+"==="+ str(expatriate)+"======"+str(grade))
                    additional_salary = frappe.new_doc('Additional Salary')
                    additional_salary.employee = doc.employee
                    additional_salary.salary_component = component["salary_component"]
                    additional_salary.amount = flt(component["amount"]) * day_percentage
                    additional_salary.payroll_date = doc.attendance_date
                    additional_salary.from_attendance = doc.name
                    additional_salary.type = "Earning"
                    additional_salary.company = doc.company
                    additional_salary.submit()
            else:
                frappe.throw(_("Please add Site Visit Fee for This <BR> Customer <B> {0} </B>, <BR> designation <B> {1} </B> <BR> and shift <B> {2} ".format(doc.customer,designation,doc.shift)))

        # frappe.throw(str("wait"))


@frappe.whitelist()
def get_additional_salary_component(employee, start_date, end_date, component_type):
    additional_components = frappe.db.sql("""
        select distinct salary_component, sum(amount) as amount, overwrite_salary_structure_amount, deduct_full_tax_on_selected_payroll_date,customer
            from 
                (
                    select salary_component, amount, overwrite_salary_structure_amount, deduct_full_tax_on_selected_payroll_date, 
                    (select customer from tabAttendance where `name` = `tabAdditional Salary`.from_attendance)  customer
                    from `tabAdditional Salary`
                    where employee=%(employee)s
                        and docstatus = 1
                        and payroll_date between %(from_date)s and %(to_date)s
                        and type = %(component_type)s
                )T 
                group by customer, salary_component, overwrite_salary_structure_amount
                order by customer, salary_component, overwrite_salary_structure_amount
         
    """, {
        'employee': employee,
        'from_date': start_date,
        'to_date': end_date,
        'component_type': "Earning" if component_type == "earnings" else "Deduction"
    }, as_dict=1,debug=True)

    additional_components_list = []
    component_fields = ["depends_on_payment_days", "salary_component_abbr", "is_tax_applicable", "variable_based_on_taxable_salary", 'type']
    for d in additional_components:
        struct_row = frappe._dict({'salary_component': d.salary_component})
        component = frappe.get_all("Salary Component", filters={'name': d.salary_component}, fields=component_fields)
        if component:
            struct_row.update(component[0])

        struct_row['deduct_full_tax_on_selected_payroll_date'] = d.deduct_full_tax_on_selected_payroll_date
        struct_row['is_additional_component'] = 1
        struct_row['customer'] = d.customer

        additional_components_list.append(frappe._dict({
            'amount': d.amount,
            'type': component[0].type,
            'struct_row': struct_row,
            'overwrite': d.overwrite_salary_structure_amount,
        }))
    return additional_components_list

def get_dates_diff(a, b):
	a = getdate(a)
	b = getdate(b)
	diff_dict = {}
	a = datetime(a.year, a.month, a.day)
	b = datetime(b.year, b.month, b.day)
	delta = relativedelta.relativedelta(b, a)
	diff_dict["years"] = delta.years
	diff_dict["months"] = delta.months
	diff_dict["days"] = delta.days

	return diff_dict
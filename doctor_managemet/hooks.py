# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "doctor_managemet"
app_title = "doctor-managemet"
app_publisher = "MiM"
app_description = "doctor-managemet"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "mismail@datavaluenet.net"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/doctor_managemet/css/doctor_managemet.css"
# app_include_js = "/assets/doctor_managemet/js/doctor_managemet.js"

# include js, css files in header of web template
# web_include_css = "/assets/doctor_managemet/css/doctor_managemet.css"
# web_include_js = "/assets/doctor_managemet/js/doctor_managemet.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}
doctype_js = {
        "Attendance Request" : "public/js/attendance_request.js",
        "Employee" : "public/js/employee.js",
        "Attendance" : "public/js/attendance.js"
    }
# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "doctor_managemet.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "doctor_managemet.install.before_install"
# after_install = "doctor_managemet.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "doctor_managemet.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }
doc_events = {
	# "Attendance Request": {
	# 	"on_submit": "doctor_managemet.utils.utils.create_additional_salaries"
	# },
	"Attendance": {
		"on_submit": "doctor_managemet.utils.utils.create_additional_salary"
	}
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"doctor_managemet.tasks.all"
# 	],
# 	"daily": [
# 		"doctor_managemet.tasks.daily"
# 	],
# 	"hourly": [
# 		"doctor_managemet.tasks.hourly"
# 	],
# 	"weekly": [
# 		"doctor_managemet.tasks.weekly"
# 	]
# 	"monthly": [
# 		"doctor_managemet.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "doctor_managemet.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"erpnext.hr.doctype.additional_salary.additional_salary.get_additional_salary_component": "doctor_managemet.utils.utils.get_additional_salary_component"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "doctor_managemet.task.get_dashboard_data"
# }

fixtures = [
    {
    "dt": "Custom Field",
    "filters": [["name", "in", [
        "Customer-cost_center",
        "Attendance Request-customer",
        "Attendance-customer",
        "Additional Salary-from_attendance",
        "Salary Detail-customer",
        "Salary Component Account-payable_account",
        "Journal Entry Account-customer",
        "Employee-expatriate",
        "Attendance Request-shift",
        "Employee-experience_years",
        "Attendance-work_day"
    ]]]
    },
    {
    "dt": "Property Setter",
    "filters": [["name", "in", [
        "Attendance Request-reason-options",
        "Salary Component Account-default_account-label",
        "Attendance-status-options",
        "Attendance-early_exit-hidden",
        "Attendance-late_entry-hidden"
    ]]]
    }
]
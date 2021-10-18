from __future__ import unicode_literals
from frappe import _
import frappe


def get_data():
	return [
		{
			"label": _("Medical Crew Management"),
			"icon": "fa fa-table",
			"items": [
				{
					"type": "doctype",
					"label": _("Site Visit Fee"),
					"name": "Site Visit Fee",
					"description": _("Site Visit Fee")
				},
				{
					"type": "doctype",
					"label": _("Site Visit Fee Component"),
					"name": "Component",
					"description": _("Site Visit Fee Component")
				},
				{
					"type": "doctype",
					"label": _("Daily Overtime Request"),
					"name": "Daily Overtime Request",
					"description": _("Daily Overtime Request")
				},
				{
					"type": "doctype",
					"label": _("Visit Form"),
					"name": "Visit Form",
					"description": _("Visit Form")
				},
			]
		}
	]
# -*- coding: utf-8 -*-
# Copyright (c) 2021, MiM and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class ComponentOption(Document):
	def autoname(self):
		self.name = self.type
		if self.type=="Years of Service":
			self.name+=" - "+str(self.number_of_years)
		if self.type=="Grade":
			self.name+=" - "+str(self.grade)


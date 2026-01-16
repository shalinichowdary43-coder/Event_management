# Copyright (c) 2026, Shalini Dondeti and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Events(Document):
    def validate(self):
        self.tickets_sold = self.tickets_sold or 0
        self.capacity = self.capacity or 0
        self.ticket_price = self.ticket_price or 0
        self.availability = self.capacity - self.tickets_sold
        self.revenue = self.tickets_sold * self.ticket_price
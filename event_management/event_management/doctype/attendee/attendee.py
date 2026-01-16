# Copyright (c) 2026, Shalini Dondeti and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Attendee(Document):
    def after_insert(self):
        
        event = frappe.get_doc("Events", self.event)

        if not event.capacity:
            frappe.throw("Event capacity is not set")

        if (event.tickets_sold or 0) >= event.capacity:
            frappe.throw("Event capacity exceeded")

        event.append("attendees", {
            "attendee_name": self.attendee_name,
            "email": self.email
        })

        event.tickets_sold = (event.tickets_sold or 0) + 1

        event.availability = event.capacity - event.tickets_sold

        event.save(ignore_permissions=True)

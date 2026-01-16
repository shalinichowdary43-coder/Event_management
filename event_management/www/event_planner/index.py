import frappe

def get_context(context):
    context.title = "Event Planner Dashboard"
    context.no_cache = 1
    context.show_sidebar = False

    context.events = frappe.get_all(
        "Events",
        fields=[
            "name",
            "title",
            "event_date",
            "location",
            "capacity",
            "tickets_sold",
            "availability",
            "ticket_price",
            "revenue",
        ],
        order_by="event_date asc",
    )


@frappe.whitelist(allow_guest=True)
def create_event(title, event_date, location, capacity, ticket_price):
    doc = frappe.get_doc({
        "doctype": "Events",
        "title": title,
        "event_date": event_date,
        "location": location,
        "capacity": int(capacity),
        "ticket_price": float(ticket_price)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return {"ok": True, "name": doc.name}


@frappe.whitelist(allow_guest=True)
def update_event(name, title, event_date, location, capacity, ticket_price):
    doc = frappe.get_doc("Events", name)
    doc.title = title
    doc.event_date = event_date
    doc.location = location
    doc.capacity = int(capacity)
    doc.ticket_price = float(ticket_price)
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return {"ok": True}


@frappe.whitelist(allow_guest=True)
def delete_event(name):
    frappe.delete_doc("Events", name, force=1)
    frappe.db.commit()
    return {"ok": True}


@frappe.whitelist(allow_guest=True)
def get_attendees(event_name):
    return frappe.get_all(
        "Attendee",
        filters={"event": event_name},
        fields=["name", "attendee_name", "email", "event"],
        order_by="creation desc"
    )


@frappe.whitelist(allow_guest=True)
def register_attendee(event_name, attendee_name, email):
    doc = frappe.get_doc({
        "doctype": "Attendee",
        "event": event_name,
        "attendee_name": attendee_name,
        "email": email
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return {"ok": True, "attendee": doc.name}


@frappe.whitelist(allow_guest=True)
def delete_attendee(attendee_id):
    frappe.delete_doc("Attendee", attendee_id, force=1)
    frappe.db.commit()
    return {"ok": True}

@frappe.whitelist(allow_guest=True)
def get_revenue_chart_data():
    events = frappe.get_all(
        "Events",
        fields=["title", "revenue"],
        order_by="event_date asc",
    )

    labels = []
    values = []

    for e in events:
        labels.append(e.get("title"))
        values.append(float(e.get("revenue") or 0))

    return {"labels": labels, "values": values}

import csv
import io

@frappe.whitelist(allow_guest=True)
def import_events_csv():
    try:
        file = frappe.request.files.get("file")
        if not file:
            return {"ok": False, "error": "No file received"}

        content = file.stream.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(content))

        required_columns = ["Title", "Event Date", "Capacity", "Ticket Price", "Location"]

        if not reader.fieldnames:
            return {"ok": False, "error": "CSV file has no header row"}

        missing = [c for c in required_columns if c not in reader.fieldnames]
        if missing:
            return {"ok": False, "error": f"Missing columns: {', '.join(missing)}"}

        created_count = 0

        for row in reader:
            title = (row.get("Title") or "").strip()
            event_date = (row.get("Event Date") or "").strip()
            location = (row.get("Location") or "").strip()
            capacity = row.get("Capacity") or 0
            ticket_price = row.get("Ticket Price") or 0

            if not title or not event_date:
                continue

            doc = frappe.get_doc({
                "doctype": "Events",
                "title": title,
                "event_date": event_date,
                "location": location,
                "capacity": int(float(capacity)) if capacity else 0,
                "ticket_price": float(ticket_price) if ticket_price else 0
            })

            doc.insert(ignore_permissions=True)
            created_count += 1

        frappe.db.commit()
        return {"ok": True, "created": created_count}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "CSV Import Failed")
        return {"ok": False, "error": str(e)}
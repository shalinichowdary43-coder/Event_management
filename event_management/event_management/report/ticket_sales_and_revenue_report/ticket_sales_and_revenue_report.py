import frappe

def execute(filters=None):
    columns = [
        {
            "label": "Event",
            "fieldname": "event",
            "fieldtype": "Link",
            "options": "Events",
            "width": 200
        },
        {
            "label": "Event Date",
            "fieldname": "event_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": "Location",
            "fieldname": "location",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Capacity",
            "fieldname": "capacity",
            "fieldtype": "Int",
            "width": 90
        },
        {
            "label": "Tickets Sold",
            "fieldname": "tickets_sold",
            "fieldtype": "Int",
            "width": 110
        },
        {
            "label": "Available",
            "fieldname": "availability",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": "Ticket Price",
            "fieldname": "ticket_price",
            "fieldtype": "Currency",
            "width": 110
        },
        {
            "label": "Revenue",
            "fieldname": "revenue",
            "fieldtype": "Currency",
            "width": 120
        }
    ]

    data = frappe.db.sql("""
        SELECT
            name AS event,
            event_date,
            location,
            capacity,
            tickets_sold,
            availability,
            ticket_price,
            revenue
        FROM `tabEvents`
        ORDER BY event_date ASC
    """, as_dict=True)

    total_revenue = sum((row.get("revenue") or 0) for row in data)

    chart = {
        "data": {
            "labels": [row.get("event") for row in data],
            "datasets": [
                {
                    "name": "Revenue",
                    "values": [(row.get("revenue") or 0) for row in data]
                }
            ]
        },
        "type": "donut"
    }

    report_summary = [
        {
            "label": "Total Revenue",
            "value": total_revenue,
            "indicator": "Green",
            "datatype": "Currency"
        }
    ]

    return columns, data, None, chart, report_summary
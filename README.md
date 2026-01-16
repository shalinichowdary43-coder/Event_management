Event Management System (Frappe + ERPNext)
Overview

This project is a web-based Event Management System built using the Frappe Framework.
It allows event planners to create, view, update, delete events, manage attendees, track ticket sales & availability, display revenue analytics, and import events via CSV.

Features Implemented:
-Event Management (CRUD)
-Create new events from the website
-View events in a dashboard table
-Update event details
-Delete events
-Ticket Sales & Availability Tracking

Shows:
Tickets Sold
Available Tickets
Revenue

Attendee Management:
Register attendee for a selected event
View attendees for selected event
Delete attendee
Revenue Analytics (Chart)
Donut chart showing Revenue by Event

CSV Import (Web UI):
Upload CSV file and import events into the system

Tech Stack:
Frappe Framework
Python
JavaScript
HTML / Jinja Templates
Chart.js (for donut chart)

Project Pages:
Event Planner Dashboard

URL:
http://127.0.0.1:8000/event_planner

Includes:
Event CRUD section
Events table
Attendee management section
Summary cards (events, sold tickets, available tickets)
Revenue donut chart

CSV import section
CSV Import Format
Required Columns (Header Row)
CSV must contain these columns exactly:
Title,Event Date,Capacity,Ticket Price,Location
Date Format:
format for Event Date:
YYYY-MM-DD
Example: 2026-03-04
Setup Instructions (Local)
1) Install & Start Frappe
2) Get the App
Clone repository into your frappe-bench/apps folder:
cd frappe-bench/apps
3) Install App on Site
cd ../
bench --site dite name install-app event_management
4) Start Server
bench start

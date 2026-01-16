let revenueChart = null;

function resetForm() {
  document.getElementById("form_title").innerText = "Create New Event";
  document.getElementById("event_name").value = "";
  document.getElementById("title").value = "";
  document.getElementById("event_date").value = "";
  document.getElementById("location").value = "";
  document.getElementById("capacity").value = "";
  document.getElementById("ticket_price").value = "";
}

function editEvent(name, title, date, location, capacity, ticket_price) {
  document.getElementById("form_title").innerText = "Update Event";
  document.getElementById("event_name").value = name;
  document.getElementById("title").value = title;
  document.getElementById("event_date").value = date;
  document.getElementById("location").value = location;
  document.getElementById("capacity").value = capacity;
  document.getElementById("ticket_price").value = ticket_price;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function submitEvent() {
  const name = document.getElementById("event_name").value;
  const title = document.getElementById("title").value;
  const event_date = document.getElementById("event_date").value;
  const location = document.getElementById("location").value;
  const capacity = document.getElementById("capacity").value;
  const ticket_price = document.getElementById("ticket_price").value;

  if (!title || !event_date || !location || !capacity || !ticket_price) {
    frappe.msgprint("Please fill all fields");
    return;
  }

  const method = name
    ? "event_management.www.event_planner.index.update_event"
    : "event_management.www.event_planner.index.create_event";

  const args = name
    ? { name, title, event_date, location, capacity, ticket_price }
    : { title, event_date, location, capacity, ticket_price };

  frappe.call({
    method: method,
    args: args,
    callback: function (r) {
      if (r.message && r.message.ok) {
        frappe.msgprint("Saved successfully");
        window.location.reload();
      }
    }
  });
}

function deleteEvent(name) {
  frappe.confirm("Are you sure you want to delete this event?", () => {
    frappe.call({
      method: "event_management.www.event_planner.index.delete_event",
      args: { name },
      callback: function (r) {
        if (r.message && r.message.ok) {
          frappe.msgprint("Deleted");
          window.location.reload();
        }
      }
    });
  });
}

function loadAttendees() {
  const event_name = document.getElementById("selected_event").value;
  const tbody = document.getElementById("attendees_table_body");

  tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;">Loading...</td></tr>`;

  frappe.call({
    method: "event_management.www.event_planner.index.get_attendees",
    args: { event_name: event_name },
    callback: function (r) {
      const data = r.message || [];
      if (data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;">No attendees found</td></tr>`;
        return;
      }

      tbody.innerHTML = "";

      data.forEach(row => {
        tbody.innerHTML += `
          <tr>
            <td>${row.attendee_name || ""}</td>
            <td>${row.email || ""}</td>
            <td>${row.event || ""}</td>
            <td>
              <button class="btn btn-sm btn-danger" onclick="deleteAttendee('${row.name}')">
                Delete
              </button>
            </td>
          </tr>
        `;
      });
    }
  });
}

function registerAttendee() {
  const event_name = document.getElementById("selected_event").value;
  const attendee_name = document.getElementById("attendee_name").value;
  const email = document.getElementById("attendee_email").value;

  if (!attendee_name || !email) {
    frappe.msgprint("Please enter attendee name and email");
    return;
  }

  frappe.call({
    method: "event_management.www.event_planner.index.register_attendee",
    args: {
      event_name: event_name,
      attendee_name: attendee_name,
      email: email
    },
    callback: function (r) {
      if (r.message && r.message.ok) {
        frappe.msgprint("Attendee Registered");
        document.getElementById("attendee_name").value = "";
        document.getElementById("attendee_email").value = "";
        loadAttendees();
      }
    }
  });
}

function deleteAttendee(attendee_id) {
  frappe.confirm("Delete this attendee?", () => {
    frappe.call({
      method: "event_management.www.event_planner.index.delete_attendee",
      args: { attendee_id: attendee_id },
      callback: function (r) {
        if (r.message && r.message.ok) {
          frappe.msgprint("Deleted");
          loadAttendees();
        }
      }
    });
  });
}

function renderDonutChartFromAPI() {
  const canvas = document.getElementById("revenueDonutChart");
  if (!canvas) return;

  frappe.call({
    method: "event_management.www.event_planner.index.get_revenue_chart_data",
    callback: function (r) {
      const msg = r.message || {};
      const labels = msg.labels || [];
      const values = msg.values || [];

      if (revenueChart) revenueChart.destroy();

      revenueChart = new Chart(canvas, {
        type: "doughnut",
        data: {
          labels: labels,
          datasets: [{
            label: "Revenue",
            data: values
          }]
        }
      });
    }
  });
}


function uploadCSV() {
  const fileInput = document.getElementById("csv_file");
  if (!fileInput || !fileInput.files.length) {
    frappe.msgprint("Please select a CSV file");
    return;
  }

  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append("file", file);

  fetch("/api/method/event_management.www.event_planner.index.import_events_csv", {
    method: "POST",
    body: formData,
    headers: {
      "X-Frappe-CSRF-Token": frappe.csrf_token
    }
  })
    .then(res => res.json())
    .then(data => {
      console.log("CSV Import Response:", data);

      if (data.message && data.message.ok) {
        frappe.msgprint(`Imported ${data.message.created} Events`);
        window.location.reload();
      } else {
        frappe.msgprint("Import failed: " + (data.message?.error || "Unknown error"));
      }
    })
    .catch(err => {
      console.log(err);
      frappe.msgprint("Import failed (check console)");
    });
}



window.addEventListener("load", function () {
  if (document.getElementById("selected_event")) {
    loadAttendees();
  }
  renderDonutChartFromAPI();
});

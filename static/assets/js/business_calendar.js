document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
  
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      selectable: true,
      select: function(info) {
        // Handle date click - open modal for creating an appointment
        window.location.href = '{% url "appointment_create" %}?date=' + info.startStr;
      },
      eventClick: function(info) {
        // Handle event click - open modal for viewing/updating/deleting appointment
        window.location.href = '{% url "appointment_detail" appointment_id=0 %}'.replace('0', info.event.id);
      },
      events: '{% url "get_appointments" %}',
    });
  
    calendar.render();
  });
  
document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
      },
      events: '{% url "get_events" %}',
  
      eventClick: function(info) {
        // Handle event editing
        $('#title').val(info.event.title);
        $('#start').val(info.event.start.toISOString().slice(0, 16));
        $('#end').val(info.event.end.toISOString().slice(0, 16));
        $('#eventModal').modal('show');
  
        // Update event when Save button is clicked
        $('#saveEventButton').off('click').on('click', function () {
          info.event.setProp('title', $('#title').val());
          info.event.setStart($('#start').val());
          info.event.setEnd($('#end').val());
          $('#eventModal').modal('hide');
          // Send an AJAX request to update the event on the server
          $.ajax({
            url: '{% url "update_event" eventt_id=info.event.id %}',
            type: 'POST',
            data: {
              title: $('#title').val(),
              start_time: $('#start').val(),
              end_time: $('#end').val(),
              csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
              // Handle success
            },
            error: function (xhr, status, error) {
              // Handle error
            }
          });
        });
      },
      dateClick: function(info) {
        // Populate the modal with the clicked date for event creation
        $('#title').val('');
        $('#start').val(info.dateStr);
        $('#end').val(info.dateStr);
        $('#eventModal').modal('show');
  
        // Create a new event when Save button is clicked
        $('#saveEventButton').off('click').on('click', function () {
          calendar.addEvent({
            title: $('#title').val(),
            start: $('#start').val(),
            end: $('#end').val()
          });
          $('#eventModal').modal('hide');
          // Send an AJAX request to create the event on the server
          $.ajax({
            url: '{% url "create_event" %}',
            type: 'POST',
            data: {
              title: $('#title').val(),
              start_time: $('#start').val(),
              end_time: $('#end').val(),
              csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
              // Handle success
            },
            error: function (xhr, status, error) {
              // Handle error
            }
          });
        });
      }
    });
  
    calendar.render();
  });
  
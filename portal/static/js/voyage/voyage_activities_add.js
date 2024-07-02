$(document).ready(function () {

  $("#activityDate").datepicker({ dateFormat: 'dd-mm-yy' });

  $(".calendarIcon").click(function () {
    $("#activityDate").focus();
  });

  $("#startTime").timepicker({});
    
});

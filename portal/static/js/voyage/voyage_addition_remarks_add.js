$(document).ready(function () {

  $("#activityDate").datepicker({ dateFormat: 'dd-mm-yy' });
  $("#calendarIcon1").click(function () {
    $("#activityDate").focus();
  });

  $("#endDate").datepicker({ dateFormat: 'dd-mm-yy' });
  $("#calendarIcon2").click(function () {
    $("#endDate").focus();
  });

  $("#startTime").timepicker({});
  $("#endTime").timepicker({});
});

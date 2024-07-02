$(document).ready(function () {
  const addEmployeeData = {
    employeeRegion: [
      {
        id: 1,
        text: "Indonesia",
      },
      {
        id: 2,
        text: "Japan",
      },
    ],
    employeeDivision: [
      {
        id: 1,
        text: "Fleet",
      },
      {
        id: 2,
        text: "Boat",
      },
    ],
    employeeRole: [
      { id: 1, text: "Ops Admin" },
      { id: 2, text: "Support" },
    ],
  };

  $("#employeeHiredDate").datepicker({});
  $(".calendarIcon").click(function () {
    $("#employeeHiredDate").focus();
  });

  for (const prop in addEmployeeData) {
    $(`.${prop}`).select2({
      placeholder: "Please Choose",
      width: "100%",
      data: addEmployeeData[prop],
    });
  }
});

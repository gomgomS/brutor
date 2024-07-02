$(document).ready(function () {
  $("#joinDate").datepicker();
  $(".customerCommodity").select2({
    width: "100%",
    data: ["test1", "test2"],
    placeholder: "Choose Commodity",
  });
  $(".hoCity").select2({
    width: "100%",
    data: ["test1", "test2"],
    placeholder: "Choose HO City",
  });
  $(".operationalArea").select2({
    width: "100%",
    data: ["test1", "test2"],
    placeholder: "Operational Area",
  });

  $(".calendarIcon").click(function () {
    $("#joinDate").focus();
  });
});

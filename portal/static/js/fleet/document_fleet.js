$(document).ready(function () {
  $("#docExpiredDate").datepicker();

  $("#calendarIcon").click(function () {
    $("#docExpiredDate").focus();
  });

  $("#documentList").DataTable({
    dom:
      "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'<'btn-flex'f <'#searchBtnContainer'>> > >" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'><'col-sm-12 col-md-7 d-flex align-items-center justify-content-end'<'page-text'> p>>",

    language: {
      searchPlaceholder: "Search",
      search: "",
    },
    pagingType: "numbers",
    scrollY: "200px",
    scrollCollapse: true,
  });

  $("<button/>")
    .addClass("btn btn-primary search-btn")
    .text("Search")
    .appendTo("#searchBtnContainer");

  $("<span/>").text("Page:").appendTo(".page-text");

  $("#documentName").select2({
    data: ["Surat Izin Layar"],
    width: "100%",
    placeholder: "Choose Doc Name",
  });
});

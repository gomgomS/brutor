$(document).ready(function () {
  const data = [
    { id: 1, text: "View Voyage", html: "./voyages_activities_view.html" },
    { id: 2, text: "Drop Voyage" },
  ];

  $(".inventoryListAction").select2({
    theme: "classic",
    width: "90%",
    data: data,
    placeholder: "Choose Action",
  });

  $(".inventoryListAction").on("select2:select", function (e) {
    self.location = e.params.data.html;
  });

  $("#inventoryListTable").DataTable({
    dom:
      "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'<'btn-flex'f <'#searchBtnContainer'>> > >" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'><'col-sm-12 col-md-7 d-flex align-items-center justify-content-end'<'page-text'> p>>",

    language: {
      searchPlaceholder: "Search",
      search: "",
    },
    pagingType: "numbers",
  });

  $("<button/>")
    .addClass("btn btn-primary search-btn")
    .text("Search")
    .appendTo("#searchBtnContainer");

  $("<span/>").text("Page:").appendTo(".page-text");
});

$(document).ready(function () {

  $("#portList").DataTable({
    "aaSorting": [],

    language: {
      searchPlaceholder: 'Search...',
      sSearch: '',
      // lengthMenu: 'MENU items/page',
    },
    dom:
      "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'<'d-flex justify-content-end'f <'#searchBtnContainer'>> > >" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'><'col-sm-12 col-md-7 d-flex align-items-center justify-content-end'<'page-text'> p>>",
    ordering: false
  });

  $("<button/>")
    .addClass("btn pd-y-5 btn-primary search-btn")
    .text("Search")
    .appendTo("#searchBtnContainer");
});

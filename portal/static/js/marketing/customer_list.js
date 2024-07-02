$(document).ready(function () {
  const customerActions = [
    {
      id: 1,
      text: "Edit Customer",
      html: "./edit_customer_marketing.html",
    },
  ];

  $(".customerListAction").select2({
    placeholder: "Choose Actions",
    width: "100%",
    data: customerActions,
    theme: "classic",
  });

  $(".customerListAction").on("select2:select", function (e) {
    self.location = e.params.data.html;
  });

  $("#customerLists").DataTable({
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
});

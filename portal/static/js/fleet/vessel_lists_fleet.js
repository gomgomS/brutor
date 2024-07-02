$(document).ready(function () {
  const vesselData = [
    {
      id: 1,
      text: "Edit Vessel",
      html: "./edit_vessel_fleet.html",
    },
    {
      id: 2,
      text: "View Vessel",
      html: "./view_vessel_fleet.html",
    },
    {
      id: 3,
      text: "Documents",
      html: "./documents_fleet.html",
    },
  ];

  $(".vesselActions").select2({
    placeholder: "Choose Action",
    data: vesselData,
    theme: "classic",
  });

  $(".vesselActions").on("select2:select", function (e) {
    self.location = e.params.data.html;
  });

  $("#vesselList").DataTable({
    dom:
      "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'<'btn-flex'f <'#searchBtnContainer'>> > >" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'><'col-sm-12 col-md-7 d-flex align-items-center justify-content-end'<'page-text'> p>>",

    language: {
      searchPlaceholder: "Search",
      search: "",
    },
    pagingType: "numbers",
    scrollY: "80%",
    scrollCollapse: true,
    initComplete: function () {
      var input1 = $(".dataTables_filter input");
      var input = $(".dataTables_filter input").unbind(),
        self = this.api();
      $("<button/>")
        .addClass("btn btn-primary search-btn")
        .attr("id", "searchBtn")
        .text("Search")
        .appendTo("#searchBtnContainer")
        .click(function () {
          self.search(input.val()).draw();
        });

      input1.on("keyup change", function () {
        if (input1.val().length === 0) {
          self.search(input.val()).draw();
        }
      });
    },
  });

  $("<span/>").text("Page:").appendTo(".page-text");
});

$(document).ready(function () {
  $("#employeeList").DataTable({
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

  const employeeActions = [
    {
      id: 1,
      text: "Edit Profile",
      html: "./update_employee.html",
    },
    {
      id: 2,
      text: "Update Username",
      html: "./change_user.html",
    },
    {
      id: 3,
      text: "Update Password",
      html: "./change_password.html",
    },
  ];

  $(".employeeActions").select2({
    theme: "classic",
    width: "100%",
    data: employeeActions,
    placeholder: "Choose Action",
  });

  $(".employeeActions").on("select2:select", function (e) {
    self.location = e.params.data.html;
  });
});

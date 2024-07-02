$(document).ready(function () {
  // const psnData = {
  //   psnVessel: [],
  //   psnCustomer: [],
  //   psnOrgCity: [],
  //   psnOrgPort: [],
  //   psnDestCity: [],
  //   psnDestPort: [],
  //   psnCargo: []
  // };

  // for (const prop in psnData) {
  //   $(`.${prop}`).select2({
  //     width: "100%"
  //   });
  // }

  $('#checkKontrak').change(function () {
    if (this.checked) {
      $("#kontrak_payung option[value='']").remove();
      $('#kontrak_payung').prop('disabled', false);
    }
    else {
      $('#kontrak_payung').append($('<option>').val("").text("Empty Kontrak Payung").attr('selected', true))
      $('#kontrak_payung').prop('disabled', 'disabled');
    }
  });

  $("#psnCustomer").change(function () {
    var customer_name = $("#psnCustomer option:selected").text();
    $("#company_name").val(customer_name)
  });


  // INITIAL VALUE FOR ORIGIN PORT
  var fk_origin_city_id = $('#psnOrgCity').find(":selected").val();
  $.ajax({
    url: '/marketing/find_port?fk_city_id=' + fk_origin_city_id,
    type: "GET",
    success: function (data) {
      $("#psnOrgPort").find('option').remove().end();

      $("#psnOrgPort").append('<option value="" disabled selected hidden>Please Choose...</option>');
      $.each(data.port_list, function () {
        $("#psnOrgPort").append($("<option />").val(this.pkey).text(this.name));
      });

    },
    error: function (data) {
      console.log(data)
      alert("Find Origin Port Failed!");
    }
  });

  // INITIAL VALUE FOR DESTINATION PORT
  var fk_destination_city_id = $('#psnDestCity').find(":selected").val();
  $.ajax({
    url: '/marketing/find_port?fk_city_id=' + fk_origin_city_id,
    type: "GET",
    success: function (data) {
      $("#psnDestPort").find('option').remove().end();

      $("#psnDestPort").append('<option value="" disabled selected hidden>Please Choose...</option>');
      $.each(data.port_list, function () {
        $("#psnDestPort").append($("<option />").val(this.pkey).text(this.name));
      });

    },
    error: function (data) {
      console.log(data)
      alert("Find Destination Port Failed!");
    }
  });


  // ORIGIN CITY SELECT ON CHANGE
  $('#psnOrgCity').change(function () {
    var fk_origin_city_id = $('#psnOrgCity').find(":selected").val();
    $.ajax({
      url: '/marketing/find_port?fk_city_id=' + fk_origin_city_id,
      type: "GET",
      success: function (data) {
        $("#psnOrgPort").find('option').remove().end();
        $("#psnOrgPort").append('<option value="" disabled selected hidden>Please Choose...</option>');
        $.each(data.port_list, function () {
          $("#psnOrgPort").append($("<option />").val(this.pkey).text(this.name));
        });

      },
      error: function (data) {
        console.log(data)
        alert("Find Origin Port Failed!");
      }
    });
  });


  // DESTINATION CITY SELECT ON CHANGE
  $('#psnDestCity').change(function () {
    var fk_destination_city_id = $('#psnDestCity').find(":selected").val();
    $.ajax({
      url: '/marketing/find_port?fk_city_id=' + fk_destination_city_id,
      type: "GET",
      success: function (data) {
        $("#psnDestPort").find('option').remove().end();
        $("#psnDestPort").append('<option value="" disabled selected hidden>Please Choose...</option>');
        $.each(data.port_list, function () {
          $("#psnDestPort").append($("<option />").val(this.pkey).text(this.name));
        });

      },
      error: function (data) {
        console.log(data)
        alert("Find Destination Port Failed!");
      }
    });
  });

 
});


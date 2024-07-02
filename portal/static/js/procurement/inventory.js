$(document).ready(function () {
  const role = form_data.role
  const mode = form_data.mode
  const addInventoryData = {
    category: form_data.category_list,
    type: form_data.type_list,
    unitSatuan: [
      {
        id: "pcs",
        text: "pcs",
      },
      {
        id: "ltr",
        text: "ltr",
      },
      {
        id: "m",
        text: "m",
      },
      {
        id: "cm",
        text: "cm",
      },
      {
        id: "roll",
        text: "roll",
      },
      {
        id: "set",
        text: "set",
      },
    ],
    lifeTimeOpt: [
      {
        id: "Year(s)",
        text: "Year(s)",
      },
      {
        id: "Month(s)",
        text: "Month(s)",
      },
      {
        id: "Running_hour(s)",
        text: "Running hour(s)",
      },
    ],
    status:[
      {
        id: "APPROVED",
        text: "APPROVED",
      },
      {
        id: "RECHECK",
        text: "RECHECK",
      },
    ]
  };
  if (mode == "edit" || mode == "edit_fm") {
    if (role == "SUPER_USER") {

      $(".form-control").prop("disabled", false);
  
      $("#status").prop("disabled", false);


    } else if (role == "FLEET_MANAGER") {

      $(".form-control").prop("disabled", true);
  
      $("#status").prop("disabled", false);
      $("#notes").prop("disabled", false);

    } else {
      $(".fm-only").hide();
      $("#status").prop("disabled", false);
    }

  } else {

    if (role == "SUPER_USER") {

      $(".form-control").prop("disabled", false);
  
      $("#status").prop("disabled", false);


    } else if (role == "FLEET_MANAGER") {

      $(".form-control").prop("disabled", true);
  
      $("#status").prop("disabled", false);
      $("#notes").prop("disabled", false);

    } else {
      $(".fm-only").hide();
      $("#status").prop("disabled", false);

    }

  }
  for (const prop in addInventoryData) {
    $(`#${prop}`).select2({
      width: "100%",
      data: addInventoryData[prop],
      placeholder: "Please Choose",
    });
  }

  $('#form_insert').submit(function (event) {

    const obj  = new Object();
    obj.mode = form_data.mode;
    u        = form_data.u
    if (u != null) { obj.u = u; }

    $(this).attr('action', "/process/admin/procurement/inventory?" + $.param(obj) ); 

  });


});

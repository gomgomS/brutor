$(document).ready(function () {
  const vesselOptions = {
    flags: [
      {
        id: 1,
        text: "Indonesia",
      },
      {
        id: 2,
        text: "Japan",
      },
      {
        id: 3,
        text: "Philippines",
      },
    ],
    portOfOrigin: [
      {
        id: 1,
        text: "Indonesia",
      },
      {
        id: 2,
        text: "Japan",
      },
      {
        id: 3,
        text: "Philippines",
      },
    ],
    builder: [
      {
        id: 1,
        text: "CV. Hutama Mandala Putra",
      },
    ],
    yearOfBuild: [
      { id: 1, text: "2003" },
      { id: 2, text: "2004" },
      { id: 3, text: "2005" },
    ],
    mtpMii: [
      { id: 1, text: "MTP" },
      { id: 2, text: "MII" },
    ],
    ownerShipStats: [
      { id: 1, text: "Owned" },
      { id: 2, text: "Charter" },
    ],
    vesselOwner: [{ id: 1, text: "CV Anugrah Amartha" }],
    tugBoat: [{ id: 1, text: "TB. Blue Dragon 48" }],
    vesselStatus: [
      { id: 1, text: "Active" },
      { id: 2, text: "Inactive" },
    ],
    facilities: [
      { id: 1, text: "Side Board" },
      { id: 2, text: "Upper" },
    ],
  };

  for (const prop in vesselOptions) {
    const optionName = vesselOptions[prop];
    $(`.${prop}`).select2({
      placeholder: "Please choose",
      data: optionName,
      width: "100%",
    });
  }

  $("#onhireDate").datepicker({ dateFormat: 'dd-mm-yy' });

  $("#onhireDateIcon").click(function () {
    $("#onhireDate").focus();
  });

  $("#offhireDate").datepicker({ dateFormat: 'dd-mm-yy' });

  $("#offhireDateIcon").click(function () {
    $("#offhireDate").focus();
  });

  $("#onHireStartTime").timepicker({});

  $("#onHireStartTime").timepicker({
    timeFormat:  "HH:mm",
      controlType: 'select'
    });

  $("#offHireStartTime").timepicker({
    timeFormat: "HH:mm",
    controlType: 'select'
  });





});

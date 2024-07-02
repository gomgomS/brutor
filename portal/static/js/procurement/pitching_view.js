function set_item_onlocal() {
  var i_reason = document.getElementById("request_reason").value;
  localStorage.setItem('request_reason', JSON.stringify(i_reason));
  var i_requested_by = document.getElementById("requested_by").value;
  localStorage.setItem('requested_by', JSON.stringify(i_requested_by));
  return true;
}

function set_quantity(table, idx) {

  var tbl = table.rows([idx]).data();

  tbl.each(function(i, val) {

    var qty_val = document.getElementById("lbl+" + idx).value; 

    var quantity = document.getElementById("quan+" + idx).value;

    if (parseInt(quantity) > parseInt(qty_val)) {

      alert("number of quantity must be less than " + qty_val)

      document.getElementById("quan+" + idx).value = parseInt(qty_val)
      i.quantity = parseInt(qty_val)

    } else {
      i.quantity = quantity
    }

  }); 
  return true;
}

function readURL(input) {

  if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.fileName = input.files[0].name
      reader.onload = function (e) {

          $('#profile-img-lbl').text(e.target.fileName);
          // $('#profile-img-tag').attr('src', e.target.result);
      }
      reader.readAsDataURL(input.files[0]);
  }
}

$(document).ready(function () {

  const role = form.role
  const mode = form.mode

  const inventoryData = {
    inventory_items: form.inventory_list,
    category: form.category_list,
    terms:[
      {
        id: "CASH",
        text: "CASH",
      },
      {
        id: "CREDIT",
        text: "CREDIT",
      },
    ],
    vendor: form.vendor_list
  };

  for (const prop in inventoryData) {
    $(`#${prop}`).select2({
      width: "100%",
      data: inventoryData[prop],
      placeholder: "Please Choose",
    });
  }

  $("#purchase_order_preview").DataTable({
    dom:
      "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'<'btn-flex'f <'#searchBtnContainer'>> > >" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'><'col-sm-12 col-md-7 d-flex align-items-center justify-content-end'<'page-text'> p>>",

    language: {
      searchPlaceholder: "Search",
      search: "",
    },
    data: form.purchase_items.items,
    columns: [

      {data: "category"},
      {data: "part_no"},
      {data: "item_name"},
      {data: "quantity"},
      {data: "request_reason"}
    ]
  });


  var table = $("#purchase_order_items_table").DataTable({
    dom:
      "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'<'btn-flex'f <'#searchBtnContainer'>> > >" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'><'col-sm-12 col-md-7 d-flex align-items-center justify-content-end'<'page-text'> p>>",

    language: {
      searchPlaceholder: "Search",
      search: "",
    },
    data: form.purchase_items.items,
    "columns": [
      {}, 
      {data: "category"},
      {data: "part_no"},
      {data: "item_name"},
      {data: "quantity"},
      {data: "uom"},
      {data: "request_reason"}
    ],

    columnDefs: [
      {
          targets: 0,
          render: function (data, type, row, meta) {
              var r
              if (row.quantity <= 0) { r = " disabled" }

              return ' <input type="hidden" id="lbl+' + meta.row + '"  value=' + row.quantity + ' > \
              <input type="checkbox" class="checkboxes" id="' + meta.row + '"  value=' + row.pkey + r + '>';
          },
          className: "dt-body-center",
          orderable: false,
          searchable: false
      },
      {
          targets: 1,
          visible: true
      }                          
  ]

  });

  $(document).on('click', "#cbo_select_all", (e)=>{
    
    $(".checkboxes").prop( "checked", $(e.target).prop("checked") );

  })

  
  $(document).on('click', ".checkboxes:checked", (e)=>{
    var id      = $(e.target).attr("id");
    var rowData = table.rows([id]).data();
  })

  $(document).on('focusout', ".quan", (e)=>{
    var id   = $(e.target).attr("id")
    var idx  = id.split("+")[1]
    set_quantity(table, idx)
  });

  $('#form_create_tender').submit(function (event) {

    var matches = [];
    var checkedcollection = table.$(".checkboxes:checked", { "page": "all" });

    checkedcollection.each(function (index, elem) {
      var tblData = table.row($(elem).attr("id")).data();
      matches.push(tblData);
    });

    if (matches.length == 0) {

      alert("At least one checkbox must be selected")
      
      event.preventDefault()
      
    } else {

      var params = [
        {
          name: "url",
          value: window.location.pathname
        },
        {
            name: "time",
            value: new Date().getTime()
        },
        {
            name: "items",
            value: JSON.stringify(matches)
        }
      ];
  
      $(this).append($.map(params, function (param) {
      return   $('<input>', {type: 'hidden', name: param.name, value: param.value })
      }))

      const obj  = new Object();
      obj.mode = "create_tender";
      u        = form.u
      if (u != null) { obj.u = u; }
  
      $(this).attr('action', "/process/admin/procurement/tenders?" + $.param(obj) ); 

    }

  });

 if (role != "FLEET_ADMIN"){
    if (role == "SUPER_USER" && form.u != "fa") {
      // table.columns([5]).visible( false );
    }
  }

  $('.quan').on("keypress keyup blur",function (event) {    
    $(this).val($(this).val().replace(/[^\d].+/, ""));
     if ((event.which < 48 || event.which > 57)) {
         event.preventDefault();
     }
  });
  $('#po_amount').on("keypress keyup blur",function (event) {    
    $(this).val($(this).val().replace(/[^0-9\.]/g,''));
    if ((event.which != 46 || $(this).val().indexOf('.') != -1) && (event.which < 48 || event.which > 57)) {
        event.preventDefault();
    }
  });


});

var getParams = function (url) {
    var params = {};
    var parser = document.createElement('a');
    parser.href = url;
  var query = parser.search.substring(1);
    var vars = query.split('&');
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        params[pair[0]] = decodeURIComponent(pair[1]);
    }
    return params;
};
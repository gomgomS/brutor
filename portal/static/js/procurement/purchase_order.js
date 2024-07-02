
function readURL(input) {

  if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.fileName = input.files[0].name
      reader.onload = function (e) {

          $('#profile-img-lbl').text(e.target.fileName);
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
      {
        data: {"quantity" : "quantity"},
        mRender: function (data, type, row, meta) {
          var r
          if (row.quantity <= 0) { r = " disabled" }
          return "<div class='form-group row'> \
              <div class='col-sm-3'> \
                <input class='form-control quan' name='quantity' id='quan+"+ meta.row +"' type='text' value='" + data.quantity + "' " + r + "  /> \
              </div> \
            </div>";

        },
      },
      {
        data: {"quantity" : "quantity"},
        mRender: function (data, type, row, meta) {

          return "<div class='form-group row'> \
              <div class='col-sm-3'> \
              <label type=''hidden' id='lbl+"+ meta.row +"'>" + data.quantity + " </label> \
              </div> \
            </div>";

        },
      },
      {data: "request_reason"}
    ],

    columnDefs: [
      {
          targets: 0,
          render: function (data, type, row, meta) {
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
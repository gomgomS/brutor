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



  $('.mod').append('<div class="table-responsive">\
    <table class="table table-bordered" id="dataTables-example">'+
    '<thead>'+
        '<tr>'+
            '<th>Pr No</th>'+
            '<th>PO/WO No</th>'+
            '<th>PO/WO Date</th>'+
            '<th>Quantity</th>'+
        '</tr>'+
    '</thead>'+

    '<tbody>'+
      '<div class="mg-l-0 mg-t-5">' +
      '<div class="form-group row"> \
      <div class="col-sm-4"> \
      <h5 class="mg-l-0 col-sm-0 text-left col-form-label">Item Purchase/Work Order</h5> \
      </div> \
      </div>' +


      '<div class="mg-l-0 mg-t-5">' +
      '<div class="form-group row"> \
        <div class="col-sm-2"> \
        <h5 class="mg-l-0 col-sm-0 text-left col-form-label">PO/WO List</h5> \
        </div> \
        <div class="col-sm-6"> \
        <input type="hidden" name="pkey" id="pkey_modal"> \
        <h5 class="col-sm-0 text-left col-form-label" id="title_modal" ></h5> \
        </div> \
      </div>' +

      '</div>' +
    '</tbody>'+

    
    '</table>\
    </div>'
    
    );


  var table = $("#purchase_request_view_tbl").DataTable({
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

      {data: "item_name"},
      {data: "quantity"},
      {data: "request_reason"},
      {data: "qty_supplied"},
      {data: "qty_unsupplied"},
      {
        data: {"pkey" : "pkey"},
        mRender: function (data, type, row) {

         return "<div class='btn-group' > \
            <button class='btn btn-secondary btn-sm dropdown-toggle pr_mdl'  id='pr_modal+" + data.pkey +"' type='button' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>Action</button> \
              <div class='dropdown-menu' > \
              <input  type='hidden' id='lbl+" + data.pkey + "' value='"+JSON.stringify(row) +"'>\
              <a class='dropdown-item prm' href='#exampleModal' id='po_list+" + data.pkey + "' data-toggle='modal'>View</a> \
            </div> \
          </div>";

        },
      }
    ]
  });

  $("#total_requested_val").text(form.purchase_items.total_requested);
  $("#total_supplied_val").text(form.purchase_items.total_supplied_val);
  $("#total_unsupplied_val").text(form.purchase_items.total_unsupplied_val);

  $('.pr_mdl').on('click', (e)=>{

    var id     = $(e.target).attr("id");
    var id_str = id.split("+")[1]

    $("#pkey_modal").val(id_str);

  })


  $('#exampleModal').on('shown.bs.modal', function () {

    var pkey = document.getElementById("pkey_modal").value
    const item = JSON.parse(document.getElementById("lbl+" + pkey).value)
    var name = item.item_name
    var part_no = item.part_no
    
    $("#title_modal").text(name + "( " + part_no + " )");

    $("#dataTables-example").DataTable({
      data: item.po,
      columns: [
        {data: "po.request_no"},
        {data: "po.po_no"},
        {data: "po.created_date"},
        {data: "quantity"}
      ],
      "bFilter": false ,
      "bInfo": false ,
      "bDestroy": true
    });


    $(this).find('.modal-dialog').css({width:'auto', height:'auto', 'max-height':'100%'});

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
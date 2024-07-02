function set_item_onlocal() {
  var i_reason = document.getElementById("request_reason").value;
  localStorage.setItem('request_reason', JSON.stringify(i_reason));
  var i_requested_by = document.getElementById("requested_by").value;
  localStorage.setItem('requested_by', JSON.stringify(i_requested_by));
  return true;
}

function recalculate_row(table, idx) {
  let f_data  = form.purchase_items
  var tbl     = table.rows([idx]).data();
  tbl.each(function(i, val) {

    var qty_val = document.getElementById("lbl+" + idx).value; 

    var quantity = document.getElementById("qu+" + idx).value;

    if (parseFloat(quantity) > parseFloat(qty_val)) {

      alert("number of quantity must be less than " + qty_val)

      document.getElementById("qu+" + idx).value = parseFloat(qty_val)
      i.quantity = parseFloat(qty_val)

    } else {
      i.quantity = quantity
    }
    i.price_unit = document.getElementById("pu+" + idx).value;
    if (!i.price_unit) {
      document.getElementById("pu+" + idx).value = 0
      i.price_unit  = 0.0
    }
    i.sub_total = document.getElementById("st+" + idx).innerHTML;
  }); 

    var total = 0;
    recs_count =  table.rows().count()
    for (i = 0; i < recs_count; i++) {
      total += parseFloat(document.getElementById("st+"+i).innerHTML)
    }

    const charges = parseFloat(0)

    const vat = (is_vat == 1) ? parseFloat((total * 10) / 100)  : parseFloat(0)
    document.getElementById("total").innerHTML = total
    document.getElementById("vat").innerHTML = vat
    document.getElementById("charges").innerHTML = parseFloat(0)
    document.getElementById("grandtotal").innerHTML = total + vat + charges
    document.getElementById("total1").value = total
    f_data.total = total

  return true;
}

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
var is_vat =  form.purchase_items.company == "1" ? 1  : 0
$(document).ready(function () {

  $("#company").change(function () {

    is_vat = (this.value == "1") ? is_vat = 1 : 0
  
    const total = parseFloat(document.getElementById("total").innerHTML)
    const charges = parseFloat(0)
    const vat = (is_vat == 1) ? parseFloat((total * 10) / 100)  : parseFloat(0)

    document.getElementById("total").innerHTML = total
    document.getElementById("vat").innerHTML = vat
    document.getElementById("charges").innerHTML = parseFloat(0)
    document.getElementById("grandtotal").innerHTML = total + vat + charges

  })

  document.getElementById("total").innerHTML = "0.0"

  const slect_component = {
    company:[
      {
        id: "1",
        text: "PT. TRANS MARITIM PRATAMA",
      },
      {
        id: "2",
        text: "PT. BAHARI SEGARA MARITIM",
      },
    ]
  };

  for (const prop in slect_component) {
    $(`#${prop}`).select2({
      width: "100%",
      data: slect_component[prop],
      placeholder: "Please Choose"
    });
  }


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

  var table1 = $('#purchase_order_items_table1').DataTable({
    data: form.purchase_items.items,
    columns: [  
      {},
      {data: "item_name"},
      {data: "part_no"},
      {data: "uom", className:"tt "},
      {
        data: {"quantity" : "quantity"},
        mRender: function (data, type, row, meta) {
          var r
          if (row.quantity <= 0) { r = " disabled" }
          return "<input type='hidden' id='lbl+"+ meta.row +"' value='"+data.qty_requested+"'><input class='tt text-right float_inp' name='qu+"+ meta.row +"' id='qu+"+ meta.row +"' type='text' value='" + data.quantity + "' " + r + "  /> ";

        },
      },
 
    {
      data: {"pkey" : "pkey"},
      mRender: function (data, type, row, meta) {

        var price_unit = data.price_unit ? data.price_unit : 0
        return " <input class='tt text-right float_inp' name='pu+"+ meta.row +"' id='pu+"+ meta.row +"' style='width:200px;height:30px;' type='text' value='"+price_unit+"'/>";

      }
    },
    {
      data: {"pkey" : "pkey"},
      mRender: function (data, type, row, meta) {
        var subtotal = 0
        return " <label class='tt text-right' name='st+"+ meta.row +"' id='st+"+ meta.row +"' style='width:200px;height:30px'/>"+subtotal+"</label>";

      }
    }
    
  ],

      scrollY: 400,
      scrollCollapse: true,
      paging:         false,
      bSort: false,
      order: [],
      columnDefs: [
        {
          targets: 0,
          render: function (data, type, row, meta) {
              var r
              if (row.quantity <= 0) { r = " disabled" }
              
              return ' <input type="hidden" id="lbl+' + meta.row + '"  value=' + row.qty_requested + ' > \
              <input type="checkbox" class="checkboxes" id="' + meta.row + '"  value=' + row.pkey + r + '>';
          },
          className: "dt-body-center",
          orderable: false,
          searchable: false
      },
      {width: 50, targets: [0], orderable: false},
      {width: 300, targets: [1], orderable: false},
      {width: 100, targets: [2], orderable: false},
      {width: 100, targets: [3], orderable: false},
      {className: "dt-right", width: 100, targets: [4], orderable: false},
      {className: "dt-right", width: 200, targets: [5], orderable: false},
      {className: "dt-right", width: 200, targets: [6], orderable: false}
      ],
      fixedColumns: false, bFilter: false, bInfo: false, orderClasses: false,
      footerCallback: function ( row, data, start, end, display ) {
          var api = this.api(), data;

          var intVal = function ( i ) {
              return typeof i === 'string' ?
                  i.replace(/[\$,]/g, '')*1 :
                  typeof i === 'number' ?
                      i : 0;
          };
          var total = api.column( 6 ).data().reduce( function (a, b) {
                return intVal(a) + intVal(b);
            }, 0 );


          $( api.column( 6 ).footer() ).html(total);

      }
      
 });
  
 $('.float_inp').on("keypress keyup blur",function (event) {    
  $(this).val($(this).val().replace(/[^0-9\.]/g,''));
  if ((event.which != 46 || $(this).val().indexOf('.') != -1) && (event.which < 48 || event.which > 57)) {
      event.preventDefault();
  }
});

$('.float_inp').focus()
$('.float_inp').focusout((e)=>{

  var id        = $(e.target).attr("id")
  var rowIndex  = id.split("+")[1]

  var qty       = document.getElementById("qu+"+rowIndex).value;
  var price_unit = document.getElementById("pu+"+rowIndex).value;
  var sub_total = parseFloat(qty * price_unit)
  document.getElementById("st+"+rowIndex).innerHTML  = sub_total
  if (!qty) {
     document.getElementById(id).value = 0
  }
  recalculate_row(table1, rowIndex)
});

$(document).on('click', ".checkboxes:checked", (e)=>{
  var id      = $(e.target).attr("id");
  recalculate_row(table1, id)
})


$(document).on('click', "#cbo_select_all", (e)=>{
    
  $(".checkboxes").prop( "checked", $(e.target).prop("checked") );

})

$('#form_msg').submit(function (event) {

  event.preventDefault()
  var formData = new FormData();
  var other_data = $(this).serializeArray();
  var csrf 
  $.each(other_data,function(key,input){
    if (input.name == '_csrf_token') {
      csrf = input.value
    }
    formData.append(input.name,input.value);
  });

  formData.append('csrf_token', csrf);
  formData.append('url', form.api_url + '/v1/api/procurements/quotations/send-msg');
  formData.append('method', "POST");
  let resp = call_api1(formData)
  var data = resp['data']
  $("#notes").val('');
  note = ""
  $('#modal7').modal('hide');

  var x = document.getElementById("snackbar");
  x.innerHTML = "Message sent"
  x.className = "show";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);

});

$('#form_create_po').submit(function (event) {

  var matches = [];
  var checkedcollection = table1.$(".checkboxes:checked", { "page": "all" });

  var j = 0
  checkedcollection.each(function (index, elem) {
    var tblData = table1.row($(elem).attr("id")).data();
    if (parseFloat(tblData.price_unit) == 0) {
      j++
    }
      matches.push(tblData);

  });

  if (j > 0){

    alert("Price unit must be greater than 0")
      
    event.preventDefault()

  } else {

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
            name: "amount",
            value: form.purchase_items.total
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
      obj.mode = "recreate_po";
      u        = form.u
      if (u != null) { obj.u = u; }
  
      $(this).attr('action', "/process/admin/procurement/purchase-orders?" + $.param(obj) ); 

    }

  }
    
});

if (role != "FLEET_ADMIN"){
  if (role == "SUPER_USER" && form.u != "fa") {
    table.columns([5]).visible( false );
  }
}


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
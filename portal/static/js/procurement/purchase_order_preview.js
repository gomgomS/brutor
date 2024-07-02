$(document).ready(function () {

  const total = parseFloat(form.purchase_items.amount)
  const charges = parseFloat(0)
  const vat = form.purchase_items.company == "1" ? parseFloat((form.purchase_items.amount * 10) / 100)  : parseFloat(0)
  document.getElementById("total").innerHTML = total
  document.getElementById("vat").innerHTML = vat
  document.getElementById("charges").innerHTML = 0.0
  document.getElementById("grandtotal").innerHTML = total + vat + charges

  const role = form.role
  const mode = form.mode

  var table = $('#purchase_order_items_table').DataTable({
    data: form.purchase_items.items,
    columns: [  
      {},
      {data: "item_name"},
      {data: "part_no"},
      {data: "uom", className:"tt "},
      {data: "quantity"},
      {data: "price_unit"},
      {data: "sub_total"}
    
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
              return row.no;
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


 $('#po_status').on('change', function()
 {
   if (this.value == "REJECT") {
    $('#notice_of_rejection').attr('required', true);
    $('#nor').show()
   } else {
    $('#notice_of_rejection').removeAttr('required');
    $('#nor').hide()
   }
 
 })
 
 $('#form_approval').submit(function (event) {

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
              name: "role",
              value: form.role
           }
         ];
  var u = form.u

  if (u != null) {
    params.push({ name: "u", value: u })
  }

  $(this).append($.map(params, function (param) {
      return   $('<input>', {type: 'hidden', name: param.name, value: param.value })
  }))

  const obj  = new Object();
  obj.mode = "update_po_status";
  u        = form.u
  if (u != null) { obj.u = u; }

  $(this).attr('action', "/process/admin/procurement/purchase-orders/update-status?" + $.param(obj) ); 
  
});

$('#form_pa_approval').submit(function (event) {

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
              name: "role",
              value: form.role
           }
         ];
  var u = form.u

  if (u != null) {
    params.push({ name: "u", value: u })
  }

  $(this).append($.map(params, function (param) {
      return   $('<input>', {type: 'hidden', name: param.name, value: param.value })
  }))

  const obj  = new Object();
  obj.mode = "update_po_status_pa";
  u        = form.u
  if (u != null) { obj.u = u; }

  $(this).attr('action', "/process/admin/procurement/purchase-orders/update-status?" + $.param(obj) ); 
  
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
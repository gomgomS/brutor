function initiateTable(source){
    var table = $("#tender_list_table").DataTable({

      data: source,
      columns: [ 
        {
          data: {"pkey" : "pkey"},
          mRender: function (data, type, row) {
            let title = row.title ? row.title : ""
            return title;
          },
        }, 
        {data: "po_no"},
        {data: "tender_no"},
        {data: "vendor_name"},
        {data: "sum_of_qty"},
        {data: "amount"},
        {data: "last_cd"},
        {
          data: {"pkey" : "pkey"},
          mRender: function (data, type, row) {
            
            return "<div class='btn-group'> \
              <a href='/menu/procurement/purchase-orders/done?key="+data.pkey+"&u="+u+"' class='btn btn-xs btn-light mg-l-0' id='opl+" + data.pkey + "'><i class='fa fa-pencil' style='width:30px'></i>  </a> \
              </div>";
          },
        }
      ],
      destroy: true,
      scrollY: 400,
      scrollCollapse: true,
      paging:         false,
      bSort: false,
      order: [],
      columnDefs: [],
      fixedColumns: false, bFilter: false, bInfo: false, orderClasses: false,
    });
  return table
  }

$(document).ready(function () {
 var table = initiateTable(tender_list)
  

  $(`.${tab_active}`).addClass('active');

  $('#form_search').submit(function (event) {
    event.preventDefault()

    var formData = new FormData();
    var obj = new Object()
    var other_data = $(this).serializeArray();
    var csrf 
    $.each(other_data,function(key,input){

      if (input.name == '_csrf_token') {
        csrf = input.value
      } else {
        if (input.value ) {
          obj[input.name] = input.value
        }
      }
    });

    formData.append('_csrf_token', csrf);
    formData.append('url', api_url + '/v1/api/procurements/purchase-orders?');
    formData.append('args', JSON.stringify(obj))
    formData.append('mode', 1)
    initiateTable(call_api1(formData)['data'])
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
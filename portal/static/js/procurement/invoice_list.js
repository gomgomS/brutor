
$(document).ready(function () {
  $(`.${tab_active}`).addClass('active');
  var table = $("#invoice_list_tbl").DataTable({
    dom:
      "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'<'btn-flex'f <'#searchBtnContainer'>> > >" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'><'col-sm-12 col-md-7 d-flex align-items-center justify-content-end'<'page-text'> p>>",

    language: {
      searchPlaceholder: "Search",
      search: "",
    },
    data: fData,
    columns: [  
      {data: "po_no"},
      {data: "tender_no"},
      {data: "vendor_name"},
      {
        data: {"pkey" : "pkey"},
        mRender: function (data, type, row) {
          
          return "<div class='btn-group'> \
            <a href='/menu/procurement/invoice/jobs?key="+data.pkey+"' class='btn btn-xs btn-light mg-l-0' id='opl+" + data.pkey + "'><i class='fa fa-pencil' style='width:30px'></i>  </a> \
            </div>";
        },
      }
    ],

    pagingType: "numbers",
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

$(document).ready(function () {

  var table = $("#tender_list_table").DataTable({
    dom:
      "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'<'btn-flex'f <'#searchBtnContainer'>> > >" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'><'col-sm-12 col-md-7 d-flex align-items-center justify-content-end'<'page-text'> p>>",

    language: {
      searchPlaceholder: "Search",
      search: "",
    },
    data: tender_list,
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
      {
        data: {"pkey" : "pkey"},
        mRender: function (data, type, row) {
          
          return "<div class='btn-group'> \
            <a href='/menu/procurement/purchase-orders/jobs?key="+data.pkey+"&u="+u+"' class='btn btn-xs btn-light mg-l-0' id='opl+" + data.pkey + "'><i class='fa fa-pencil' style='width:30px'></i>  </a> \
            </div>";
        },
      }
    ],

    pagingType: "numbers",
  });

  $("<button/>")
    .addClass("btn btn-primary search-btn")
    .text("Search")
    .appendTo("#searchBtnContainer");

  $("<span/>").text("Page:").appendTo(".page-text");

  $(`.${tab_active}`).addClass('active');

  $(document).on('click', ".trp", (e)=>{

    var id     = $(e.target).attr("id");
    var id_str = id.split("+")[1]

    const viewObj = new Object();
    viewObj.key   = id_str
    viewObj.mode  = "preview_po"
    const docObj  = new Object();
    docObj.key    = id_str
    docObj.mode   = "view_po_doc_list"
    var u       = form.u;
    if (u != null) { viewObj.u = u; };
    var view_url  = '/menu/procurement/purchase-orders?' + $.param(viewObj);
    var po_doc_url  = '/menu/procurement/purchase-orders?' + $.param(docObj);
   
    if (document.getElementById("po_pitch+"+id_str) == null) {
        
      $("#"+id_str).append(`<a href="${view_url}" class="dropdown-item pol" id="po_view+${id_str}">View</a>`);
      $("#"+id_str).append(`<a href="${po_doc_url}" class="dropdown-item doc" id="po_doc_view+${id_str}">Documents</a>`);
    }
  })



  $(document).on('click', "a.pol", (e)=>{

    var id     = $(e.target).attr("id");
    var href   = $(e.target).attr("href");
    var url    = href.split('?')[0];

    const obj  = new Object(getParams(href));
  
    var   u    = form.u;
    if (u != null) { obj.u = u; };

    var link = document.getElementById(id);
    link.setAttribute('href',  url + "?" + $.param(obj));
 
    // if ((role != "SUPER_USER" && role == "PURCHASE_ADMIN") || (role == "SUPER_USER" && form.u == "pa")) {
    //   alert("Under construction ... !!! we are currently working on this page")
    //   e.preventDefault();
    // }
  })

  $(document).on('click', "a.doc", (e)=>{

    var id     = $(e.target).attr("id");
    var href   = $(e.target).attr("href");
    var url    = href.split('?')[0];

    const obj  = new Object(getParams(href));
  
    var   u    = form.u;
    if (u != null) { obj.u = u; };

    var link = document.getElementById(id);
    link.setAttribute('href',  url + "?" + $.param(obj));
 
  })


  
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
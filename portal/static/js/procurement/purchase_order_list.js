$(document).ready(function () {
  const role = form.role

  var table = $("#purchase_list_table").DataTable({
    dom:
      "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'<'btn-flex'f <'#searchBtnContainer'>> > >" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'><'col-sm-12 col-md-7 d-flex align-items-center justify-content-end'<'page-text'> p>>",

    language: {
      searchPlaceholder: "Search",
      search: "",
    },
    data: purchaseListData,
    columns: [  
      {data: "created_date"},
      {data: "po_no"},
      {data: "request_no"},
      {data: "request_type"},
      {data: "quantity"},
      {
        data: {"pkey" : "pkey"},
        mRender: function (data, type, row) {
          if (data.status == 'REQOMAPP') {
            return "PENDING";
          } else if (data.status == 'OMAPP') {
            return "APPROVED";
          } else if (data.status == 'REJECTED') {
            return "REJECTED";
          }
          return data.status;

        },
      },
      {
        data: {"pkey" : "pkey"},
        mRender: function (data, type, row) {
          
          return "<div class='btn-group'> \
              <button class='btn btn-secondary btn-sm dropdown-toggle trp' id='action_btns+" + data.pkey +"' type='button' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>Action</button> \
                <div class='dropdown-menu dmenu' id='" + data.pkey + "' ></div> \
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

  $(`.${form.tab_active}`).addClass('active');

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
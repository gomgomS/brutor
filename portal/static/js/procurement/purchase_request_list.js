$(document).ready(function () {
  const role = form.role

  var table = $("#purchase_request_list_table").DataTable({
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
      {data: "request_no"},
      {data: "request_type"},
      {data: "quantity"},
      {
        data: {"pkey" : "pkey"},
        mRender: function (data, type, row) {
  
          return "<div class='btn-group'> \
              <button class='btn btn-secondary btn-sm dropdown-toggle trd' id='action_btns+" + data.pkey +"' type='button' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>Action</button> \
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
 
  if (form.role == "CHIEF_MECHANIC" || form.role == "FLEET_MANAGER" || form.u == "cm" || form.u == "fm" ){

    if (form.tab_active == "REQCMAPP" || form.tab_active == "CMAPP"){
      form.tab_active = "REQAPP"
    }
  }

  $(`.${form.tab_active}`).addClass('active');

  $(document).on('click', ".trd", (e)=>{
    var id     = $(e.target).attr("id");
    var id_str = id.split("+")[1]
    const viewObj = new Object();
    viewObj.key   = id_str
    var u       = form.u;
    if (u != null) { viewObj.u = u; };
    var view_url  = '/menu/procurement/purchase-request?' + $.param(viewObj);

    const delObj = new Object();
    delObj.key   = id_str
    var u       = form.u;
    if (u != null) { delObj.u = u; };
    var del_url   = '/process/admin/procurement/purchase-request?' + $.param(delObj);

      if ((role != "SUPER_USER" && role != "PURCHASE_ADMIN") || (role == "SUPER_USER" && form.u != "pa")) {

        var anchor_id = "pr_view+"+id_str;
        var del_anchor_id = "pr_delete+"+id_str;

        if ( (role != "SUPER_USER" && role == "FLEET_ADMIN") || (role == "SUPER_USER" && form.u == "fa") ) {

          if (form.tab_active == 'FMAPP' || form.tab_active == 'REJECTED') {
            anchor_id = "po_view+"+id_str;
            del_anchor_id = "po_delete+"+id_str;
          }

        }

        if (document.getElementById("pr_view+"+id_str) == null) {

          $("#"+id_str).append(`<a href="${view_url}" class="dropdown-item prl" id="${anchor_id}">View</a>`);
        }

        if (form.tab_active == 'PARTIAL' || form.tab_active == 'FMAPP') {

          if ((role != "SUPER_USER" && role == "FLEET_ADMIN") || (role == "SUPER_USER" && form.u == "fa")) {
            if (document.getElementById("pr_delete+"+id_str) == null) {
              $("#"+id_str).append(`<a href="${del_url}" class="dropdown-item prl" id="${del_anchor_id}" >Delete</a>`);
            }
          }

        }
      } else {

        if (document.getElementById("po_pitch+"+id_str) == null) {
          $("#"+id_str).append(`<a href="${view_url}" class="dropdown-item prl" id="po_pitch+${id_str}">View</a>`);
        }

      }
  })


  $(document).on('click', "a.prl", (e)=>{

    var id     = $(e.target).attr("id");
    var href   = $(e.target).attr("href");
    var url    = href.split('?')[0];

    var id_str = id.split("+")[0]
    var mode  

    if (id_str == "pr_view"){ 
      mode = "edit"  
    } else if (id_str == "po_view"){
      mode = "view_po"
    }else if (id_str == "po_delete"){
      mode = "del_po"
    }else if (id_str == "po_pitch"){
      mode = "pitch_po"
    }else { mode = "delete" }
    const obj  = new Object(getParams(href));
    obj.mode   = mode
    var   u    = form.u;
    if (u != null) { obj.u = u; };

    var link = document.getElementById(id);
    link.setAttribute('href',  url + "?" + $.param(obj));

    // if (status != "PARTIAL" && (mode == "view_po" && (form.u == 'fa' || role == 'FLEET_ADMIN') ) || (mode == "del_po" && (form.u == 'fa' || role == 'FLEET_ADMIN')) ) {
    //   alert("Under construction ... !!! we are currently working on this page")
    //   e.preventDefault();
    // }
    // if ((role != "SUPER_USER" && role == "PURCHASE_ADMIN") || (role == "SUPER_USER" && form.u == "pa")) {
    //   alert("Under construction ... !!! we are currently working on this page")
    //   e.preventDefault();
    // }
  })

  var url_params = getParams(window.location)
  if ("status" in url_params) {
    status = url_params.status

    var arr = ["REQCMAPP", "CMAPP"];
    if (( (role != "SUPER_USER" && role == "FLEET_ADMIN") || (role == "SUPER_USER" && form.u == "fa") ) && arr.includes(status) ) {
      table.columns([4]).visible( false );
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
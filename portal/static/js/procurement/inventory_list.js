$(document).ready(function () {
  const role = form.role

  var table = $("#inventoryListTable").DataTable({
    dom:
      "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'<'btn-flex'f <'#searchBtnContainer'>> > >" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'><'col-sm-12 col-md-7 d-flex align-items-center justify-content-end'<'page-text'> p>>",

    language: {
      searchPlaceholder: "Search",
      search: "",
    },
    data: inventoryListData,
    columns: [
      {data: "category"},
      {data: "part_no"},
      {data: "item_name"},
      {data: "unit"},
      {
        data: {"pkey" : "pkey"},
        mRender: function (data, type, row) {
  
          return "<div class='btn-group'> \
              <button class='btn btn-secondary btn-sm dropdown-toggle trd-inv' id='action_btns_inv+" + data.pkey +"' type='button' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>Action</button> \
                <div class='dropdown-menu dmenu-inv' id='" + data.pkey + "' ></div> \
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

  $(document).on('click', ".trd-inv", (e)=>{

    var id     = $(e.target).attr("id");
    var id_str = id.split("+")[1]
    const viewObj = new Object();
    viewObj.key   = id_str
    var u       = form.u;
    if (u != null) { viewObj.u = u; };
    var view_url  = '/menu/procurement/inventory?' + $.param(viewObj);

    const delObj = new Object();
    delObj.key   = id_str
    var u       = form.u;
    if (u != null) { delObj.u = u; };
    var del_url   = '/process/admin/procurement/inventory?' + $.param(delObj);


    if ( (role != "FLEET_MANAGER" && form.u == null) || (role == "SUPER_USER" && form.u != "fm") ){
    if (document.getElementById("inv_view+"+id_str) == null) {
      $("#"+id_str).append(`<a href="${view_url}" class="dropdown-item" id="inv_view+${id_str}">View</a>`);
    }
    }
    if (role == "FLEET_ADMIN" || form.u == "fa") {
      if (document.getElementById("inv_delete+"+id_str) == null) {
        $("#"+id_str).append(`<a href="${del_url}" class="dropdown-item" id="inv_delete+${id_str}" >Delete</a>`);
      }
    }

    if (role == "FLEET_MANAGER" || form.u == "fm") {
      if (document.getElementById("inv_delete+"+id_str) == null) {
        $("#"+id_str).append(`<a href="${view_url}" class="dropdown-item" id="inv_view_fm+${id_str}" >Update Status</a>`);
      }
    }

  })


  $(document).on('click', "a.dropdown-item", (e)=>{
    var id     = $(e.target).attr("id");
    var href   = $(e.target).attr("href");
    var url    = href.split('?')[0];

    var id_str = id.split("+")[0]
    var mode  
    if (id_str == "inv_view"){ 
      mode = "edit"  
    } else if (id_str == "inv_view_fm") {
      mode = "edit_fm"  
    } else { mode = "delete" }

    const obj  = new Object(getParams(href));
    obj.mode   = mode
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
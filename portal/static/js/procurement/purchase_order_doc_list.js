function set_item_onlocal() {
  var i_reason = document.getElementById("request_reason").value;
  localStorage.setItem('request_reason', JSON.stringify(i_reason));
  var i_requested_by = document.getElementById("requested_by").value;
  localStorage.setItem('requested_by', JSON.stringify(i_requested_by));
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
    request_type:[
      {
        id: "PO",
        text: "PO",
      },
      {
        id: "WO",
        text: "WO",
      },
    ],
    status:[
      {
        id: "APPROVED",
        text: "APPROVED",
      },
      {
        id: "REJECTED",
        text: "REJECTED",
      },
    ]
  };

  for (const prop in inventoryData) {
    $(`#${prop}`).select2({
      width: "100%",
      data: inventoryData[prop],
      placeholder: "Please Choose",
    });
  }


  $('.img_mod_body').append('<div class="table-responsive" > <img id="img-modal-xl" class="rounded img-default" /> </div>');


  var table = $("#purchase_order_docs_tbl").DataTable({
    dom:
      "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'<'btn-flex'f <'#searchBtnContainer'>> > >" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'><'col-sm-12 col-md-7 d-flex align-items-center justify-content-end'<'page-text'> p>>",

    language: {
      searchPlaceholder: "Search",
      search: "",
    },
    data: form.purchase_items.doc_list,
    columns: [  
      {
        data: {"pkey" : "pkey"},
        mRender: function (data, type, row, meta) {

          return meta.row + 1;

        }
      },
      {
        data: {"doc_url" : "doc_url"},
        mRender: function (data, type, row) {
          var href = 'http://storage.tenarin.com/v1/cfs/get-file?' + data.doc_url
          return "<a class='dropdown-item pr'  href='" + href + "'>"+ row.filename +"</a>";

        }
      },
      {data: "upload_time"},
      {
        data: {"pkey" : "pkey"},
        mRender: function (data, type, row) {

          return "<div class='btn-group' > \
            <button class='btn btn-secondary btn-sm dropdown-toggle' type='button' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>Action</button> \
              <div class='dropdown-menu' > \
              <a class='dropdown-item doc' id='doc_delete+" + data.pkey + "' href='/process/admin/procurement/purchase-orders?w=" + form.mode + "&mode=delete_doc&pkey=" + row.fk_purchase_order_id + "&key=" + data.pkey + "'>Remove</a> \
            </div> \
          </div>";

        }
      }
      
    ],

    pagingType: "numbers",
    "bPaginate": true,
    "bFilter": false,
    "bInfo": false
  });
        
  $(document).on('click', "a.doc", (e)=>{

    var id     = $(e.target).attr("id");
    var href   = $(e.target).attr("href");

    var url    = href.split('?')[0];

    var id_str = id.split("+")[0]
    
    const obj  = new Object(getParams(href));
    var   u    = form.u;
    if (u != null) { obj.u = u; };

    var link = document.getElementById(id);
    link.setAttribute('href',  url + "?" + $.param(obj));

    // e.preventDefault();
  })
  $('#form_upload_po').submit(function (event) {
  
    const obj  = new Object();
    obj.mode = "insert_doc";
    u        = form.u
    if (u != null) { obj.u = u; }

    $(this).attr('action', "/process/admin/procurement/purchase-orders?" + $.param(obj) ); 

  });


  $("#profile-img").change(function(){
    readURL(this);
  });

  $("<span/>").text("Page:").appendTo(".page-text");


  $("#pkey").val(form.pkey);
  $("#pkey1").val(form.pkey);
  $("#requested_by").val(JSON.parse(localStorage.getItem('requested_by')));
  $("#request_reason").val(JSON.parse(localStorage.getItem('request_reason')));

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
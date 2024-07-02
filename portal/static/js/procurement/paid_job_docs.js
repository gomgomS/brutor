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
      }
      reader.readAsDataURL(input.files[0]);
  }
}

$(document).ready(function () {

  const job  = form.job

  $('#form_upload_payment_receipts').submit(function (event) {

      const obj  = new Object();
      obj.mode = "insert_paid_docs";
  
      $(this).attr('action', "/process/admin/procurement/purchase-orders?" + $.param(obj) ); 
  
    });

  $("#profile-img").change(function(){
    readURL(this);
  });

  
  var table = $("#paid_job_docs_tbl").DataTable({
    dom:
      "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'<'btn-flex'f <'#searchBtnContainer'>> > >" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'><'col-sm-12 col-md-7 d-flex align-items-center justify-content-end'<'page-text'> p>>",

    language: {
      searchPlaceholder: "Search",
      search: "",
    },
    data: job.paid_docs,
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
              <a class='dropdown-item doc' id='doc_delete+" + data.pkey + "' href='/process/admin/procurement/purchase-orders?mode=delete_paid_job_doc&pkey=" + data.fk_purchase_order_job_id + "&key=" + data.pkey + "'>Remove</a> \
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

  })
 
  $("<span/>").text("Page:").appendTo(".page-text");

});

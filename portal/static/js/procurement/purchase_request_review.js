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

  var table = $("#purchase_request_review").DataTable({
    dom:
      "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'<'btn-flex'f <'#searchBtnContainer'>> > >" +
      "<'row'<'col-sm-12'tr>>" +
      "<'row'<'col-sm-12 col-md-5'><'col-sm-12 col-md-7 d-flex align-items-center justify-content-end'<'page-text'> p>>",

    language: {
      searchPlaceholder: "Search",
      search: "",
    },
    data: form.purchase_items.items,
    columns: [  
      {data: "category"},
      {data: "part_no"},
      {data: "item_name"},
      {data: "quantity"},
      {data: "request_reason"},
      {
        data: {"image" : "image"},
        mRender: function (data, type, row, meta) {
          var img_src = 'http://storage.tenarin.com/v1/cfs/get-file?' + data.image

          return "<div class='avatar avatar-small col-sm-0 img-preview' id='imgPreview3'> \
          <input  type='hidden' id='imgtag+"+ meta.row + "' value='"+ img_src +"'>\
          <img  src='" + img_src + "' class='preview'  /> \
          </div>";

        },
      }
    ],

    pagingType: "numbers",
    "bPaginate": true,
    "bFilter": false,
    "bInfo": false
  });

  $('.img_mod_body').append('<div class="table-responsive" > <img id="img-modal-xl" class="rounded img-default" /> </div>');

  $('.dataTable').on( 'click', 'tbody td', function () {
    var col_index = table.cell( this ).index().columnVisible
    var row_index = $(this).closest('tr').index();
    // 5 WITHOUT Lsdate and qty in list else 7
    if (col_index == 5) {

      var img_src = document.getElementById("imgtag+" + row_index).value;
      $('#img-modal-xl').width(760)
      $('#img-modal-xl').height(600)
      $('#img-modal-xl').attr('src', img_src);

      $('#myModal').modal('show');
    }
  });

  $("<span/>").text("Page:").appendTo(".page-text");

  var href   = document.getElementById('intenal_buy_btn').href;
  var url    = href.split('?')[0];

  const obj  = new Object(getParams(href));
  var   u    = form.u;
  if (u != null) { obj.u = u; };

  var link = document.getElementById('intenal_buy_btn');
  link.setAttribute('href',  url + "?" + $.param(obj));

  var href   = document.getElementById('pitching_btn').href;
  var url    = href.split('?')[0];

  const obj1  = new Object(getParams(href));
  var   u    = form.u;
  if (u != null) { obj1.u = u; };

  var link = document.getElementById('pitching_btn');
  link.setAttribute('href',  url + "?" + $.param(obj1));

  
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
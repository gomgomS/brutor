function set_item_onlocal() {
  var i_request_type = document.getElementById("request_type").value;
  localStorage.setItem('request_type', JSON.stringify(i_request_type));
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
let category_id
$(document).ready(function () {

  const role = form.role
  const mode = form.mode

  const inventoryData = {
    category: form.category_list,
    requested_by: form.tugboat_list,
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
      placeholder: "Please Choose"
    });
  }


  $("#category").on('change', (e)=>{
    var params  = new Object()
    var data    = new Object()
    var arr     = [];
    params.category_id = $(e.target).val()
    params.status = "APPROVED"
    data.url      = form.api_url + '/v1/api/procurements/inventory-items?' + $.param(params)
    data.m        = 1
    $.each(call_api(data), function (index, itemData) {
      arr.push({"id": itemData.pkey, "text": itemData.item_name });
    })

    $('#inventory_items').empty().append('<option value="" ></option>');
    $('#inventory_items').select2({
      width: "100%",
      placeholder: "Please Choose",
      data: arr
    });
  })
    

  var table = $("#purchase_request_items_table").DataTable({
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
      {data: "request_date"},
      {data: "category"},
      {data: "item_name"},
      {
        data: {"quantity" : "quantity"},
        mRender: function (data, type, row) {

          return "<div class='form-group row'> \
              <div class='col-sm-6'> \
                <input class='form-control quan' name='quantity' id='quan+"+ form.purchase_items.pkey +"+"+ data.pkey +"' type='text' value='" + data.quantity + "' /> \
              </div> \
            </div>";

        },
      },
      {data: "request_reason"},
      // {data: "ls_date"},
      // {data: "ls_qty"},
      {
        data: {"image" : "image"},
        mRender: function (data, type, row, meta) {
          var img_src = 'http://storage.tenarin.com/v1/cfs/get-file?' + data.image
 
          return "<div class='avatar avatar-small col-sm-0 img-preview' id='imgPreview3'> \
          <input  type='hidden' id='imgtag+"+ meta.row + "' value='"+ img_src +"'>\
          <img  src='" + img_src + "' class='preview'  /> \
          </div>";

        }
      },
      {
        data: {"pkey" : "pkey"},
        mRender: function (data, type, row) {

          return "<div class='btn-group' > \
            <button class='btn btn-secondary btn-sm dropdown-toggle' type='button' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>Action</button> \
              <div class='dropdown-menu' > \
              <a class='dropdown-item pr' id='item_delete+" + data.pkey + "' href='/process/admin/procurement/purchase-request?w=" + form.mode + "&mode=delete_item&pkey=" + row.fk_purchase_request_id + "&key=" + data.pkey + "'>Remove</a> \
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



  if (role != "FLEET_ADMIN"){
    if (role == "SUPER_USER" && form.u != "fa") {
      // HIDE ACTION COL EXCEPT FA
      table.columns([6]).visible( false );
    }
  }
              

  $('.img_mod_body').append('<div class="table-responsive" > <img id="img-modal-xl" class="rounded img-default" /> </div>');
  
  $('.dataTable').on( 'click', 'tbody td', function () {
    var col_index = table.cell( this ).index().columnVisible
    var row_index = $(this).closest('tr').index();
    // 5 without Lsdate and qty in list else 7
    if (col_index == 5) {
      var img_src = document.getElementById("imgtag+" + row_index).value;
      $('#img-modal-xl').width(760)
      $('#img-modal-xl').height(600)
      $('#img-modal-xl').attr('src', img_src);

      $('#myModal').modal('show');
    }
  });

  $('.quan').on("keypress keyup blur",function (event) {    
    $(this).val($(this).val().replace(/[^\d].+/, ""));
     if ((event.which < 48 || event.which > 57)) {
         event.preventDefault();
     }
  });
  $('#quantity').on("keypress keyup blur",function (event) {    
    $(this).val($(this).val().replace(/[^\d].+/, ""));
     if ((event.which < 48 || event.which > 57)) {
         event.preventDefault();
     }
  });

  $('.quan').focusout((e)=>{
    var id                      = $(e.target).attr("id")
    var fk_purchase_request_id  = id.split("+")[1]
    var pkey                    = id.split("+")[2]

    var quantity = document.getElementById(id).value;
    
    if (!quantity ){
      document.getElementById(id).value = 0
    }
   
    var form_data = new FormData();
    form_data.append('role', role);
    form_data.append('quantity', quantity);

    $.ajax({
      url: form.api_url + '/v1/api/procurements/purchase-requests/' + fk_purchase_request_id + "/items/" + pkey,
      data        : form_data,
      processData : false,
      contentType : false,
      type: 'POST'
    })

  });

  let inventory_type 
  var i = (typeof form.purchase_items.items !== 'undefined') ? form.purchase_items.items : "";
  if (Object.keys(i).length > 0) {
    $('.item_type').attr('value', i[0].item_type)
  }

  $('#inventory_items').on('select2:select', function (e) {
    var data = e.params.data;
    var id   = data['id']
    
    var data    = new Object()
    data.m      = 1
    data.url    = form.api_url + '/v1/api/procurements/inventory-items/' + id

    let item = call_api(data)
    inventory_type = item.type

});
 

  $(document).on('click', "a.pr", (e)=>{

    var id     = $(e.target).attr("id");
    var href   = $(e.target).attr("href");
    var url    = href.split('?')[0];

    var id_str = id.split("+")[0]

    const obj  = new Object(getParams(href));

    if (id_str != 'item_delete') {
      obj.mode   = mode
    }
    var   u    = form.u;
    if (u != null) { obj.u = u; };

    var link = document.getElementById(id);
    link.setAttribute('href',  url + "?" + $.param(obj));
  })

  $('#form_insert').submit(function (event) {
    var type = document.getElementById('item_type').value

    if (type && inventory_type != type) {
      alert('Sorry .. ! only items of the "'+ type +'" type are allowed'); 
      event.preventDefault()
    } else {

      const obj  = new Object();
      obj.mode = form.mode;
      u        = form.u
      if (u != null) { obj.u = u; }

      $(this).attr('action', "/process/admin/procurement/purchase-request?" + $.param(obj) ); 

    }
  });

  $('#form_pub').submit(function (event) {

    const obj  = new Object();
    obj.mode = "pub";
    u        = form.u
    if (u != null) { obj.u = u; }

    $(this).attr('action', "/process/admin/procurement/purchase-request?" + $.param(obj) ); 

  });

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
    obj.mode = "approval_req";
    u        = form.u
    if (u != null) { obj.u = u; }

    $(this).attr('action', "/process/admin/procurement/purchase-request?" + $.param(obj) ); 
    
  });

  $("#profile-img").change(function(){
    readURL(this);
  });
 
  $("<span/>").text("Page:").appendTo(".page-text");

  $("#pkey").val(form.pkey);
  $("#pkey1").val(form.pkey);
 
  $('#request_type').val(JSON.parse(localStorage.getItem('request_type'))).change();
  $('#requested_by').val(JSON.parse(localStorage.getItem('requested_by'))).change();
  $("#request_reason").val(JSON.parse(localStorage.getItem('request_reason')));

});

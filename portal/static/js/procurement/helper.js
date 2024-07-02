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

var call_api = function (data) {
  let result = {}

  $.ajaxSetup({
    beforeSend: function(x, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            x.setRequestHeader("X-CSRFToken", csrf_token)
        }
        if (x && x.overrideMimeType) {
          x.overrideMimeType("application/j-son;charset=UTF-8");
        }
    }
  })

  $.ajax({
    type: 'POST',
    url: '/api/helper',
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    async: false,
    success:function(e) {
      resp = JSON.parse(e)
      data = resp.data
      result = data
    }
  })

  return result
}

var call_api1 = function (data) {
  let result = {}
  var csrf_token 
  var url
  for(var pair of data.entries()){
    if (pair[0] == '_csrf_token') {
      csrf_token =  pair[1]
    }
    if (pair[0] == 'url') {
      url = pair[1]
    }
  }
  $.ajaxSetup({
    beforeSend: function(x, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            x.setRequestHeader("X-CSRFToken", csrf_token)
        }
    }
  })
  $.ajax({
    type: 'POST',
    url: '/api/helper?type=form-data',
    data: data,
    cache: false,
    contentType: false,
    processData: false,
    async: false,
    success:function(e) {
      result = e
    }
  })

  return result
}
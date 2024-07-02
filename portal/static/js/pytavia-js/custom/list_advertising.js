$(document).ready(
	function()
	{
		
	}
);

relaodJs = function(src){
    src = $('script[src$="' + src + '"]').attr("src");
    $('script[src$="' + src + '"]').remove();
    $('<script/>').attr('src', src).appendTo('body');
}

view_advertising = function(params)
{
   if(params){
        var path ;
        var name ;
        var description ;
        var imgMain = "" ; 
        var imgList = "" ;
        sizePrms = params.length;
        var i = 0 ;
        for(i;i<sizePrms;i++){          
            data = params[i]
            console.log("***** data ");
            console.log(data);
            name  = data["name"          ]
            path  = data["document_path" ]
            description  = data["description"]
            if(i < 1 ){
                imgMain += "<li><a class='ns-img' href='/user/get-file/merchant-advertising?"+ path +"'></a></li>" ;
            }
            imgList +=  "<li><a class='thumb' href='/user/get-file/merchant-advertising?"+ path +"'></a></li>" ; 
        }
        document.getElementById("imgMain").innerHTML = imgMain ;
        document.getElementById("imgList").innerHTML = imgList ;
        relaodJs("/static/js/pytavia-js/thumbnail-slider.js");
        relaodJs("/static/js/pytavia-js/ninja-slider.js");
   }     
}


advertising = function(pkey)
{
    //alert("test")
    $("#pkey").val( pkey );
}



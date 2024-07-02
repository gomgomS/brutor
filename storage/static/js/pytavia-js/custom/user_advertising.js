$(document).ready(function() {

    $('#table-list-advertising').DataTable( {
        dom: 'Bfrtip',
        buttons: [
                        'copy', 'csv', 'excel','pdf'
                ]
    });

    "use strict";

    $(".popup img").click(function () {
            var $src = $(this).attr("src");
            $(".show").fadeIn();
            $(".img-show img").attr("src", $src);
    });

    $("span, .overlay").click(function () {
            $(".show").fadeOut();
    });

});

advertising = function(pkey)
{
        //alert("test")
	$("#pkey").val( pkey );
}
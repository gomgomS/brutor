$(document).ready(function(){
    var msg_exist = $("#msg_exist").val();
    if(msg_exist === "YES"){
        $("#dialog_message").modal("show");
    }
});    

SHOW_DIALOG = function(msg_title,msg_desc)
{
    $("#msg_title").html(msg_title);
    $("#msg_desc").html(msg_desc);
    $("#dialog_message").modal("show");
}

$(document).ready(function () {
    $("#route").change(function () {
        var distance = $(this).find(':selected').data('dist');
        $("#dist").val(distance)
    });
});
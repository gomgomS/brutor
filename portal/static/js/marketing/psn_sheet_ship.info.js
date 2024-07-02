$(document).ready(function () {
    $("#get_price").click(function () {
        var month   = $('#month').find(":selected").val();
        var city    = $('#city').find(":selected").val();
        var period  = $('#period').find(":selected").val();

        $.ajax({
            url: '/operational/find_fuel_price_list?month=' + month + '&city=' + city + '&period=' + period,
            type: "GET",
            success: function (data) {
                $("#table_price_list").find("tr.fuel_price_item").remove();

                var trHTML = '';
                
                $.each( data.fuel_list, function (i, item) {
                    trHTML += '<tr class="fuel_price_item"><td>' + item["month"] + '</td><td>' + item["period"] + '</td><td>' + item["city"] + '</td><td>' + item["supplier"] + '</td><td>' + item["price"] + '</td><td>' + item["terms"] + '</td><td><button type="button" class="btn btn-primary btn-sm" id="' + item["pkey"] + '">Select Price</button></td></tr>' ;
                    
                });
                $('#table_body_price_list').append(trHTML);

                $.each(data.fuel_list, function (i, item) {
                    $("#" + item["pkey"]).on("click", function () {
                        $("#fuel_price").val(item["price"])
                    });
                });
                
                
            },
            error: function (data) {
                console.log(data)
                alert("error!");
            }
        });
    });
});

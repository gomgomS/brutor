var labels = "";
var charts = "";
var length = "";

$(document).ready(function() {
	fn_floating_fund_chart(labels, charts, length);
    fn_floating_fund_get_data();
});

fn_floating_fund_get_data = function()
{
        var http_params = {};
        AJAX_SERVER_call(
                fn_floating_fund_get_data_CALLBACK,
                "GET",
                "/api/floating-fund/chart/get-data",
                http_params,
                true
         );
}

fn_floating_fund_get_data_CALLBACK = function(msg_data)
{
    console.log(msg_data);
    var message_action = msg_data.message_action;
    if (message_action == "GET_FLOATING_FUND_CHART_API_SUCCESS")
    {
        var charts = msg_data.message_data.charts;
        var labels = msg_data.message_data.labels;

        length = labels.length; 
        fn_floating_fund_chart(labels, charts, length);
    }
}

fn_floating_fund_chart = function(labels, charts, length)
{
    var xlive_float      = []
    var xmerchant_float  = []
    var xmoney_supply    = []
    var xuser_float      = []
    var xroot_float      = []
    var date_label       = []

    var live_float      = charts.live_float;
    var merchant_float  = charts.merchant_float;
    var money_supply    = charts.money_supply;
    var root_float      = charts.root_float;
    var user_float      = charts.user_float;
    for (var idx=0; idx<length; idx++)
    {
        var float_item    = live_float[idx];
        xlive_float.push(float_item.amount); 

        var mrcnt_fl_item = merchant_float[idx]
        xmerchant_float.push(mrcnt_fl_item.amount); 

        var money_supply_item = money_supply[idx]
        xmoney_supply.push(money_supply_item.amount); 

        var user_float_item = user_float[idx]
        xuser_float.push(user_float_item.amount); 

        var root_float_item = root_float[idx]
        xroot_float.push(root_float_item.amount); 

        var label      = labels[idx];
        date_label.push(label.label); 
    }
    var data = {
            labels: date_label,
            datasets: [{
                fill: false,
                label: 'User Float',
                data: xlive_float,
                borderColor: '#2130c6',
                backgroundColor: '#2130c6',
                pointBackgroundColor: 'transparent',
                pointBorderColor: 'transparent',
                pointBorderWidth:1,
                pointHoverBackgroundColor: "#2130c6",
                lineTension: 0,
            },
            {
                fill: false,
                label: 'Merchant Float',
                data: xmerchant_float,
                borderColor: '#b721c6',
                backgroundColor: '#b721c6',
                pointBackgroundColor: 'transparent',
                pointBorderColor: 'transparent',
                pointBorderWidth:1,
                pointHoverBackgroundColor: "#b721c6",
                lineTension: 0,
            },
            {
                fill: false,
                label: 'Money Supply',
                data: xmoney_supply,
                borderColor: '#c62182',
                backgroundColor: '#c62182',
                pointBackgroundColor: 'transparent',
                pointBorderColor: 'transparent',
                pointBorderWidth:1,
                pointHoverBackgroundColor: "#c62182",
                lineTension: 0,
            },
            {
                fill: false,
                label: 'User Float',
                data: xuser_float,
                borderColor: '#2182c6',
                backgroundColor: '#2182c6',
                pointBackgroundColor: 'transparent',
                pointBorderColor: 'transparent',
                pointBorderWidth:1,
                pointHoverBackgroundColor: "#2182c6",
                lineTension: 0,
            },
            {
                fill: false,
                label: 'Root Float',
                data: xroot_float,
                borderColor: '#21C6B7',
                backgroundColor: '#21C6B7',
                pointBackgroundColor: 'transparent',
                pointBorderColor: 'transparent',
                pointBorderWidth:1,
                pointHoverBackgroundColor: "#21C6B7",
                lineTension: 0,
            },
            ]
        }

    // chart
	if ($('#chartJs').length ){
		var ctx = document.getElementById("chartJs");
		var mybarChart = new Chart(ctx, {
			type: 'line',
            data: data,
			options: {
				legend: {
					display: true,
					position: 'bottom',
					labels: {
						fontColor: '#666666'
					}
				},
				scales: {
					xAxes: [{
						// type: 'time',
                        ticks: {
                          autoSkip: false,
                        },
                        display: true,
                        scaleLabel: {
                            display: true,
                        },
                        gridLines: {
                          display: false
                        },
            		 }],
                     yAxes: [{
                        ticks: {
                           beginAtZero: true,
                        },
                        display: true,
                        scaleLabel: {
                           display: false,
                           labelString: "view",
                            },
                        }],
            		}

		    }
		});

	}
		// /end  chart
}


// Ajax Call Server
AJAX_SERVER_call = function(callback_func, method, wservice, uri, bool)
{
        _g_jqxhr = $.ajax(
        {
                url      : wservice ,
                method   : method   ,
                data     : uri      ,
                dataType : "json"
        }).done(
                function(msg_json)
                {
                        callback_func(msg_json);
                }
        ).fail(
                function(msg_json)
                {
                        callback_func(msg_json);
                }
        ).always(
                function()
                {
                }
        );
};

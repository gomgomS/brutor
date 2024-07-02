var g_logout_time    = 30 * (24 * 60 * 60); // 30 days 
var g_settime_handle = null;

$(document).ready(
    function()
    {
	idle_logout();
    }
);

init_logout_time = function()
{
    var ctime = new Date().getTime();
    AJAX_SERVER_call(
        init_logout_time_CALLBACK,
        "GET",
        "/api_get_autologout_proc",
        { ctime : ctime },
        true
    );
};

init_logout_time_CALLBACK  = function(msg_data)
{
    console.log( msg_data );

    var message_action = msg_data.message_action
    if ( message_action == "GET_AUTO_LOGOUT_PROC_SUCCESS")
    {
        var message_data = msg_data.message_data;
        g_logout_time    = parseInt(message_data.logout_time_required);
        idle_logout();
    }
}

idle_logout = function()
{
    window.onload       = reset_timer;
    window.onmousemove  = reset_timer;
    window.onmousedown  = reset_timer;
    window.ontouchstart = reset_timer;
    window.onclick      = reset_timer;
    window.onkeypress   = reset_timer;
    window.addEventListener(
            'scroll', reset_timer , true
    );
}

reset_timer = function()
{
    clearTimeout(g_settime_handle);
    g_settime_handle = setTimeout(
        action_func,
        g_logout_time  * 1000
    );
}

action_func = function()
{
    window.location = "/auth/logout";
}


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
}

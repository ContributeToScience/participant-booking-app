$(document).ready(function () {
    $("a[data-target='#loginSignupModal']").on("click", function () {
        var next = $(this).data("next");
        var params = "?next=" + next;
        $.colorbox({
            href: "/accounts/ajax/login_signup/" + params,
            fastIframe: false,
            opacity: 0.8,
            width: 600
        });
        return false;
    });

    $("#ajax_login").on("click", function () {
        $.ajax({
            url: "/accounts/ajax/login_signup/",
            dataType: "json",
            type: "POST",
            data: $("#login_form").serialize(),
            async: true,
            success: function (data) {
                if (data.status == "success") {
                    $.colorbox.close();
                    window.location.reload();
                } else if (data.error) {
                    var errors = "";
                    $.each(data.error, function (key, value) {
                        errors += value + "<br/>";
                    });
                    $("#login_error").html(errors);
                    $("#login_error").show();
                }
            }
        });
        return false;
    });

    $("#ajax_signup").on("click", function () {
        $.ajax({
            url: "/accounts/ajax/login_signup/",
            dataType: "json",
            type: "POST",
            data: $("#signup_form").serialize(),
            async: true,
            success: function (data) {
                if (data.status == "success") {
                    $.colorbox.close();
                    window.location.reload();
                } else if (data.error) {
                    var errors = "";
                    $.each(data.error, function (key, value) {
                        errors += value + "<br/>";
                    });
                    $("#signup_error").html(errors);
                    $("#signup_error").show();
                }
            }
        });
        return false;
    });
});
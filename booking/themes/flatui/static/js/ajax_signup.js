$(document).ready(function () {
    $("a[data-target='#signupModal']").on("click", function () {
        var next = $(this).data("next") ? $(this).data("next") : "";
        var user_type = $(this).data("user-type") ? $(this).data("user-type") : "";
        var params = "?next=" + next + "&user_type=" + user_type;
        $.colorbox({
            href: "/accounts/ajax/signup/" + params,
            fastIframe: false,
            opacity: 0.8
        });
        return false;
    });

    $("#ajax_signup").on("click", function () {
        $.ajax({
            url: "/accounts/ajax/signup/",
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
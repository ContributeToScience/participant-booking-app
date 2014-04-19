$(document).ready(function () {
    $("a[data-target='#loginModal']").on("click", function () {
        var next = $(this).data("next");
        var params = "?next=" + next;
        $.colorbox({
            href: "/accounts/ajax/login/" + params,
            fastIframe: false,
            opacity: 0.8
        });
        return false;
    });

    $("#ajax_login").on("click", function () {
        $.ajax({
            url: "/accounts/ajax/login/",
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
                        errors += value + "<br/>";;
                    });
                    $("#login_error").html(errors);
                    $("#login_error").show();
                }
            }
        });
        return false;
    });
});
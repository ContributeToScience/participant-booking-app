$(document).ready(function () {
    $("a.btn-contact-message").bind("click", function () {
        var content_object_id = $(this).data("content-object-id");
        var recipient_id = $(this).data("recipient-id");
        var type = $(this).data("type");
        var message_id = $(this).data("message-id");
        var url = $(this).attr("href") + "?recipient_id=" + recipient_id + "&type=" + type;
        if (content_object_id) {
            url += "&content_object_id=" + content_object_id;
        }
        if (message_id) {
            url += "&message_id=" + message_id;
        }
        $.colorbox({
            href: url,
            iframe: true,
            fastIframe: false,
            width: "50%",
            height: "44%",
            opacity: 0.8,
            speed: 500
        });
        return false;
    });

    $("div.contact-message").find(".table-mail > tbody > tr").bind("click", function(e){
        if (e.target.type != "checkbox") {
            var url = $(this).closest("tr").data("message-detail-url");
            $.colorbox({
                href: url,
                iframe: true,
                fastIframe: false,
                width: "50%",
                height: "44%",
                opacity: 0.8,
                speed: 500
            });
            $(this).closest("tr").removeClass("unread");
        }
    });

    $(".btn-message-delete").bind("click", function (e) {
        var $this = $(this);
        var message_ids = [];
        $this.closest(".tab-pane").find(".table").find("input.selectable:checked").each(function () {
            message_ids.push($(this).val());
        });
        if(message_ids.length == 0){
            alert("Please select at least one");
        }else{
            $.ajax({
                url: "/message/delete/",
                type: "POST",
                dataType: "json",
                data: {message_ids: message_ids},
                async: true,
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", $.cookie("csrftoken"));
                },
                success: function (result) {
                    if(result.status == "success"){
                        $this.closest(".tab-pane").find(".table").find("input.selectable:checked").each(function () {
                            $(this).closest("tr").remove();
                        });
                    }
                }
            });
        }
        e.preventDefault();
    });

    $(".btn-message-undo").bind("click", function (e) {
        var $this = $(this);
        var message_ids = [];
        $this.closest(".tab-pane").find(".table").find("input.selectable:checked").each(function () {
            message_ids.push($(this).val());
        });
        if(message_ids.length == 0){
            alert("Please select at least one");
        }else{
            $.ajax({
                url: "/message/undo/",
                type: "POST",
                dataType: "json",
                data: {message_ids: message_ids},
                async: true,
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", $.cookie("csrftoken"));
                },
                success: function (result) {
                    if(result.status == "success"){
                        $this.closest(".tab-pane").find(".table").find("input.selectable:checked").each(function () {
                            $(this).closest("tr").remove();
                        });
                    }
                }
            });
        }
        e.preventDefault();
    });

    $("#btn_bulk_feedback").bind("click", function () {
        var recipient_id = [];
        var count = 0;
        $("#choose_form input[name='participant_id']").each(function () {
            if ($(this).parent().hasClass("checked")) {
                recipient_id.push($(this).data("recipient-id"));
                count++;
            }
        });
        if (count <= 0) {
            alert("Please select at least one");
            return false;
        } else {
            var content_object_id = $(this).data("content-object-id");
            var type = $(this).data("type");
            var url = $(this).attr("href") + "?recipient_id=" + recipient_id.toString() + "&type=" + type;
            if (content_object_id) {
                url += "&content_object_id=" + content_object_id;
            }
            $.colorbox({
                href: url,
                iframe: true,
                fastIframe: false,
                width: "50%",
                height: "44%",
                opacity: 0.8,
                speed: 500
            });
        }
        return false;
    });
});
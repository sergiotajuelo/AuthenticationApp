$("form[name=register_form").submit(function(e) {
    var $form = $(this) 
    var data = $form.serialize(); //Send the variables as a pack to the backend
    var $error = $form.find(".error")

    $.ajax({
        url: "/user/register",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/dashboard"
        },
        error: function(resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden")
        }
    })

    e.preventDefault(); //Avoid leaving the page when submit the form
});
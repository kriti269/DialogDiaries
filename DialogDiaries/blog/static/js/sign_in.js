function getQueryString() {
	var result = {};
	if(!window.location.search.length) return result;
	var qs = window.location.search.slice(1);
	var parts = qs.split("&");
	for(var i=0, len=parts.length; i<len; i++) {
		var tokens = parts[i].split("=");
		result[tokens[0]] = decodeURIComponent(tokens[1]);
	}
	return result;
}

function addFields(self) {
    var qs = getQueryString();
    for(var key in qs) {
        var val = $("#" + key).val();
        if(val == null  || val == '') {
            $("#" + key).val(qs[key]);
            //var field = $(document.createElement("input"));
            //field.attr("name", key).attr("type","hidden");
            //field.val(qs[key]);
            //self.append(field);
        }
    }
}

$(document).ready(function(){
    $(".isa_error").delay(1000).fadeOut(5000);
    $(".isa_success").delay(1000).fadeOut(5000);
    if( document.getElementsByClassName("validation-error")[0] != null) {
        document.getElementsByClassName("validation-error")[0].innerHTML = '';
    }
    $(".validation-error").hide();
    var $form = $(".contact-form");
    addFields($form);

    if($("#register").val()!=''){
        if($(".first-name-container, .last-name-container, .email-container, .password2-container").is(":visible")==false){
            $(".first-name-container, .last-name-container, .email-container, .password2-container").css({'display':'flex'});
            $(".sign-in-bg").css("height","725px");
        }
    }

    $(".btn-login").click(function(){
        if($(".first-name-container, .last-name-container, .email-container, .password2-container").is(":visible")==true){
            $(".first-name-container, .last-name-container, .email-container, .password2-container").css({'display':'none'});
            $(".sign-in-bg").css("height","500px");
        }
        else{
            $form.submit();
        }
    });

    $(".btn-register").click(function(){
        if($(".first-name-container, .last-name-container, .email-container, .password2-container").is(":visible")==false){
            $(".first-name-container, .last-name-container, .email-container, .password2-container").css({'display':'flex'});
            $(".sign-in-bg").css("height","725px");
        }
        else{
            var error_message = "";
            var firstname = $(".first-name-container input").val();
            var lastname = $(".last-name-container input").val();
            var email = $(".email-container input").val();
            var password2 = $(".password2-container input").val();
            var password1 = $(".password-container input").val();
            var username = $(".user-name-container input").val();
            if(firstname!="" && lastname!="" && email!="" && password1!="" && password2!="" && username!=""){
                if(password2==password1){
                    $form.submit();
                }
                else{
                    error_message = "Password does not match!"
                }
            }
            else{
                error_message = "Please fill out the entire form!"
            }
            if(error_message!=""){
                var child = document.createTextNode(error_message);
                document.getElementsByClassName("validation-error")[0].appendChild(child);
                $(".validation-error").show();
                $(".validation-error").delay(1000).fadeOut(5000, function(){
                    document.getElementsByClassName("validation-error")[0].innerHTML = '';
                });
            }
        }
    });

});
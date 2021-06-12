$(document).ready(function(){
    $("#addLike, #addComment").click(function(e){
        e.preventDefault();
        var slug = $('#post').val();
        var isAuthenticated = $("#is_authenticated").val();
        if(isAuthenticated == "True"){
            $.ajax({
              type: "POST",
              url: $(this).data('url') + '?post=' + slug,
              data: {
                        content: '',
                        'csrfmiddlewaretoken': $('#token').val()
                    },
              success: function(data) {
                $("#likes").text(data.total_likes);
                $("#comments").text(data.total_comments);
              }
            });
        }
        else{
            window.location.href = "sign-in.html?next=" + $(this).data('url') + '&post='+ slug;
        }
    });

    $("#addUserComment").click(function(e){
        $(".isa_error").delay(1000).fadeOut(2000);
        e.preventDefault();
        var slug = $('#post').val();
        var comment_url = $("#comment_url").val();
        var isAuthenticated = $("#is_authenticated").val();
        if(isAuthenticated == "True"){
            var value = $("#comment").val().trim();
            if(value == "") {
                $("#commentErrorEmpty").css("display", "block");
            }
            else if(value.length > 200) {
                 $("#commentErrorGreater").css("display", "block");
                 $("#comment").val("");
            }
            else {
                $.ajax({
                  type: "POST",
                  url: $(this).data('url') + '?post=' + slug,
                  data: {
                            content: value,
                            'csrfmiddlewaretoken': $('#token').val()
                        },
                  success: function(data) {
                    debugger;
                    $(".empty-comments").hide();
                    $("#likes").text(data.total_likes);
                    $("#comments").text(data.total_comments);
                    if($("#commentCount").length == 0) {
                        $(".response").append("(" + data.total_comments + ")");
                    }
                    else {
                        $("#commentCount").text(data.total_comments);
                    }
                    $("#comment").hide();
                    $("#addUserComment").hide();
                    var obj = JSON.parse(data.comment_list);
                    const monthNames = ["January", "February", "March", "April", "May", "June",
                          "July", "August", "September", "October", "November", "December"
                        ];
                    var date = new Date(obj[0].fields["posted_on"]);
                    var minutesDiff = date.getTimezoneOffset() % 60;
                    var minutes = date.getMinutes() + minutesDiff;
                    var hours = date.getHours() + date.getTimezoneOffset() / 60;
                    var end = hours > 12 ? 'p.m.' : 'a.m.';
                    hours = hours % 12;
                    hours = hours ? hours : 12;
                    var convertedDate = monthNames[date.getMonth()] + " " + date.getDate() +
                                ", " + date.getFullYear() + ", " + hours + ":" +
                                minutes + " " + end;
                    //Add Comment
                    var commentHTML = "<div id='commentSection' class='mb-4'>" +
                            "<div class='card-body details'>" +
                            "<div class='detail'><p class='card-text'>" +
                            obj[0].fields["content"] + "</p>" +
                            "<p class='card-text text-muted h6'>" +
                            "<a href='" + comment_url + "'>" +
                            $("#username").val() +
                            "</a> | " + convertedDate +"</p></div></div></div>";
                    if($("#commentSection").length != 0) {
                        commentHTML += "<hr style='width: 90%;'>";
                    }
                    $("#allCommentsDiv").prepend(commentHTML);
                  }
                });
            }
        }
        else{
            window.location.href = "sign-in.html?next=" + $(this).data('url') + '&post='+ slug;
        }
    });

    var val = $("#showCommentBar").val();
    if(val != null && val == "True") {
        openNav();
    }
});

$(document).click(function(event) {
    var box = $('#myNav');
    var id = event.target.id;
    var container = document.getElementById('myNav');
    var parentid = event.target.parentElement.id;
    var width = Math.round(box.width() / box.parent().parent().width() * 100);
    if ("myNav" != id && container != null && !container.contains(event.target) && width == "28") {
        box.css("width", "0%");
    }
    else if("comment_btn" == parentid) {
        box.css("width", "28%");
        $('#comment').val("");
        setTimeout(function(){
            $('#comment').focus();
        },200);
    }
    else if("comment" == id) {
        if($("#is_authenticated").val() == 'False') {
            window.location.href = $("#signIn_url").val() + "?next=" + $("#comments_url").val() + "&post=" + $("#post").val();
        }
    }
});

function closeNav() {
    var box = $('#myNav');
    box.css("width", "0%");
}

function openNav() {
    var box = $("#myNav");
    box.css("width", "28%");
    $('#comment').val("");
    setTimeout(function(){
      $('#comment').focus();
    },200);
}
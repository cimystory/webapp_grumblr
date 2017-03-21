function populateList() {
    var userfield = $("#user-field");
    var user = userfield.val();
    console.log(user);
    $.get("/grumblr/get-follow-items/" + user)
        .done(function(data) {
            var list = $("#todo-list");
            list.data('max-time', data['max-time']);
            list.html('');
            for (var i = 0; i < data.items.length; i++) {
                item = data.items[i];
                var new_item = $(item.html);
                new_item.data("item-id", item.id);
                list.prepend(new_item);
                populateComments(item.id);
            }
        });
}

function populateComments(id) {
    $.get("/grumblr/get-comments/" + id)
        .done(function(data) {
            var list = $("#comment-list" + id);
            list.data('max-time', data['max-time']);
            list.html('');
            for (var i = 0; i < data.comments.length; i++) {
                comment = data.comments[i];
                var new_comment = $(comment.html);
                new_comment.data("comment-id", comment.id);
                // console.log(item.id);
                list.append(new_comment);
            }
        });
}

function addComment (post_id) {
    var commentField = $("#comment-field" + post_id);
    $.post("/grumblr/add-comment/" + post_id, {comment: commentField.val()})
        .done(function(data) {
            console.log(post_id);
            getUpdates();
            commentUpdates(post_id);
            commentField.val("").focus();
        });
}

// Update comment here
function commentUpdates(id) {
    var list = $("#comment-list" + id);
    var max_time = list.data("max-time");
    $.get("/grumblr/get-comment-changes/"+ id + "/" + max_time)
        .done(function(data) {
            // console.log("update comments successfully");
            list.data('max-time', data['max-time']);
            for (var i = 0; i < data.comments.length; i++) {
                var comment = data.comments[i];
                if (comment.deleted) {
                  $("#comment_" + comment.id).remove();
                } else {
                  var new_comment = $(comment.html);
                  new_comment.data("comment-id", comment.id);
                  list.append(new_comment);
                }
            }
        });
}

// Update posts here
function getUpdates() {
    var list = $("#todo-list");
    var max_time = list.data("max-time");
    $.get("/grumblr/get-changes/"+ max_time)
        .done(function(data) {
            list.data('max-time', data['max-time']);
            for (var i = 0; i < data.items.length; i++) {
                var item = data.items[i];
                if (item.deleted) {
                  $("#item_" + item.id).remove();
                } else {
                  var new_item = $(item.html);
                  console.log(new_item);
                  new_item.data("item-id", item.id);
                  list.prepend(new_item);
                }
            }
        });
}

$(document).ready(function () {
  // Add event-handlers

  // Set up to-do list with initial DB items and DOM data
  populateList();
  $("#item-field").focus();

  // Periodically refresh to-do list
  window.setInterval(getUpdates, 5000);

  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});

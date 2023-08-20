function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.getElementById("save-comment-button").addEventListener("click", () => {
  const commentInput = document.getElementById("new_comment");
  const commentContent = commentInput.value.trim();

  if (commentContent === "") {
    alert("Please enter a comment.");
    return;
  }

  const button = document.getElementById("save-comment-button");
  const post_id = button.value;
  const apiUrl = `/api-post-save/${post_id}/`;
  const apiUrlcomments = `/api-post/${post_id}/`;

  const formData = new FormData();
  formData.append("content", commentContent);

  fetch(apiUrl, {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(
          `Network response was not ok. Status: ${response.status} ${response.statusText}`
        );
      }
      return response.json();
    })
    .then((data) => {
      // console.log(data);
      // Update the comments list
      fetch(apiUrlcomments)
        .then((response) => {
          if (!response.ok) {
            throw new Error(
              `Network response was not ok. Status: ${response.status} ${response.statusText}`
            );
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
          data.comments.forEach((comment) => {
            console.log(`Author: ${comment.author}`);
            console.log(`Content: ${comment.content}`);
            console.log(`Created: ${comment.created}`);

            if (
              comment.reply_comments &&
              Array.isArray(comment.reply_comments) &&
              comment.reply_comments.length > 0
            ) {
              console.log("Reply Comments:");
              comment.reply_comments.forEach((reply) => {
                console.log(`  Author: ${reply.author}`);
                console.log(`  Content: ${reply.content}`);
                console.log(`  Created: ${reply.created}`);
              });
            }

            console.log("-----------------------------------");
          });
          
          // const comment = document.getElementById("new_comment").value;
          // console.log(new_comment);
          // const comments = document.getElementById("comments_list");
          // comments.innerHTML = JSON.stringify(comment, null, 2);
        })
        .catch((error) => console.error("Error:", error));
      const comment = document.getElementById("new_comment").value;
      console.log(data.comments);
      const comments = document.getElementById("comments_list");
      comments.innerHTML = JSON.stringify(comment, null, 2);
      commentInput.value = "";
    })
    .catch((error) => console.error("Error:", error));
});



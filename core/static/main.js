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
let csrftoken = getCookie("csrftoken");

// SHOW all comments/reply-comments of post
const detailsPost = document.querySelector("#show_data");
const add_comment = document.querySelector("#add_comment");
const edit_comment = document.querySelector("#edit_comment");
const delete_reply_comment = document.querySelector("#delete_reply_comment");
const edit_reply_comment = document.querySelector("#edit_reply_comment");
const comments_box = document.getElementById("comments_box");
const like_unlike_button = document.getElementById("like_unlike_button")
const commentForm = document.getElementById("comment-form");




show_details_post()
// show details of post
function show_details_post() {
  comments_box.innerHTML = "";
  const post_id = detailsPost.dataset.postId;
  const postsUrl = `/api-post/${post_id}/`;
  fetch(postsUrl)
    .then((resp) => resp.json())
    .then(function (data) {
      console.log("Data:", data);
      if (data.user_authenticated){
        if (data.user_has_liked === 1){
          likes=`<i class="fa-solid fa-thumbs-up"></i> Liked <span class="total-likes">${data.total_likes}</span>`
        }else {
          likes=`<i class="fa-regular fa-thumbs-up"></i> Like <span class="total-likes">${data.total_likes}</span>`
        }
        if (data.user_has_unliked === 1){
          unlikes=`<i class="fa-solid fa-thumbs-down"></i> Unliked <span class="total-unlikes">${data.total_unlikes}</span>`
        }else {
          unlikes=`<i class="fa-regular fa-thumbs-down"></i> Unlike <span class="total-unlikes">${data.total_unlikes}</span>`
        }
        likes_unlikes=`<form>
                      <button class="btn btn-light like-btn mx-2" data-comment-id="${data.post_id}" name="like-button">${likes}</button>
                      <button class="btn btn-light unlike-btn mx-2" data-comment-id="${data.post_id}" name="unlike-button">${unlikes}</button>
                    </form>`
      }else{
        likes_unlikes=`<button class="btn btn-light like-btn mx-2" data-comment-id="${data.post_id}">
                          <i class="fa-regular fa-thumbs-up"></i> Like <span class="total-likes">${data.total_likes}</span>
                      </button>
                      <button class="btn btn-light unlike-btn mx-2" data-comment-id="${data.post_id}">
                          <i class="fa-regular fa-thumbs-down"></i> Unlike <span class="total-unlikes">${data.total_unlikes}</span>
                      </button>`
      }
      like_unlike_button.innerHTML=likes_unlikes;

      for (let i = 0; i < data.comments.length; i++) {
        let replies = "";
        if (
          data.user_authenticated === data.post_Author_Profile.author ||
          data.user_authenticated === data.comments[i].comment_Author_Profile.author
        ) {
          three_dot_button = `<button class="btn btn-light" data-bs-toggle="dropdown" aria-haspopup="true"
                                        aria-expanded="false" data-comment-id="${data.comments[i].id}">
                                        <i class="bi bi-three-dots-vertical"></i>
                                    </button>`;
        } else {
          three_dot_button = ``;
        }

        if (
          data.user_authenticated === data.comments[i].comment_Author_Profile.author
        ) {
          edit_comment_button = `<button class="btn btn-light text-start" data-bs-toggle="modal"
                                        data-bs-target="#editCommentModal-${data.comments[i].id}"
                                        data-comment-id="${data.comments[i].id}"><i class="bi bi-pencil"> </i> Edit
                                        Comment
                                  </button>`;
        } else {
          edit_comment_button = ``;
        }

        if (
          data.user_authenticated === data.post_Author_Profile.author ||
          data.user_authenticated === data.comments[i].comment_Author_Profile.author
        ) {
          delete_comment_form = `<form >                  
                                        <button type="button" class="btn btn-light text-start delete_comment_form" data-bs-toggle="modal" data-bs-target="#confirmDeleteModal-${data.comments[i].id}">
                                            <i class="bi bi-trash"></i> Delete Comment
                                        </button>
                                    </form>`;
        } else {
          delete_comment_form = ``;
        }

        if (data.user_authenticated) {
          reply_button = `<div class="col-2 mb-3">  
                              <div class="d-flex justify-content-end">
                                <button class="btn btn-light reply-button my-2 text-muted" data-bs-toggle="modal"
                                    data-bs-target="#replyCommentModal-${data.comments[i].id}"
                                    data-comment-id="${data.comments[i].id}"><i class="bi bi-reply"></i> Reply
                                </button>
                              </div> 
                          </div>`;
        } else {
          reply_button = ``;
        }
        
        if (data.comments[i].replyComments.length > 0) {
          for (let j = 0; j < data.comments[i].replyComments.length; j++) {
            if (
              data.user_authenticated === data.post_Author_Profile.author ||
              data.user_authenticated === data.comments[i].replyComments[j].author
            ) {
              r_three_dot_button = `<button class="btn btn-light" data-bs-toggle="dropdown" aria-haspopup="true"
                                        aria-expanded="false">
                                        <i class="bi bi-three-dots-vertical"></i>
                                    </button>`;
            } else {
              r_three_dot_button = ``;
            }
            if (
              data.user_authenticated === data.comments[i].replyComments[j].author
            ) {
              r_edit_comment_button = `<button class="btn btn-light text-start" data-bs-toggle="modal"
                                            data-bs-target="#editRCommentModal-${data.comments[i].replyComments[j].id}"
                                            data-comment-id="${data.comments[i].replyComments[j].id}"><i class="bi bi-pencil"> </i> Edit
                                            Comment
                                        </button>`;
            } else {
              r_edit_comment_button = ``;
            }

            if (
              data.user_authenticated === data.post_Author_Profile.author ||
              data.user_authenticated === data.comments[i].replyComments[j].author
            ) {
              r_delete_comment_form = `<form>
                                            <button type="button" class="btn btn-light text-start" data-bs-toggle="modal" data-bs-target="#confirmDeleteModal-${data.comments[i].replyComments[j].id}"
                                                ><i class="bi bi-trash"> </i> Delete
                                                Comment</button>
                                        </form>`;
            } else {
              r_delete_comment_form = ``;
            }

            replies += `
                <div class="d-flex col mb-1">
                        <div class="flex-shrink-0"><img class="rounded-circle mx-auto d-block"
                            src="${data.comments[i].replyComments[j].author_profile_image_url}" alt="..." width="50" height="50">
                        </div>
                    <div class="ms-2">
                        <div class="d-flex">
                            <strong class="me-1">${data.comments[i].replyComments[j].author_username}</strong>
                            <small class="text-muted fst-italic mb-2 me-1"> | ${data.comments[i].replyComments[j].created}</small>
                            ${r_three_dot_button}
                            <div class="dropdown-menu dropdown-menu-lg-end p-2 ">
                                ${r_edit_comment_button}
                                ${r_delete_comment_form}
                            </div>
                            <!-- Confirmation Modal for Delete reply Comment -->
                            <div class="modal fade" id="confirmDeleteModal-${data.comments[i].replyComments[j].id}" tabindex="-1" aria-labelledby="confirmDeleteModalLabel" aria-hidden="true">
                                <div class="modal-dialog modal-dialog-centered">
                                    <div class="modal-content">
                                        <div class="modal-body my-2">
                                            Are you sure you want to delete this comment?
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                            <form >
                                                <button type="submit" id="delete_reply_comment" class="btn btn-danger" data-reply_comment-id="${data.comments[i].replyComments[j].id}" name="delete_reply_comment"
                                                    ><i class="bi bi-trash"> </i> Delete </button>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- Edit form for the Reply comment -->
                            <div class="modal fade" id="editRCommentModal-${data.comments[i].replyComments[j].id}" tabindex="-1"
                                aria-labelledby="editRCommentModalLabel" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" id="editRCommentModalLabel">Edit Comment</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <form id="editCommentForm_${data.comments[i].replyComments[j].id}">
                                                <textarea class="form-control" name="content" rows="3">${data.comments[i].replyComments[j].content}</textarea>
                                                <button type="submit" class="btn btn-primary mt-2" name="edit_reply_comment">Update</button>
                                                <button type="button" class="btn btn-secondary mt-2" data-bs-dismiss="modal">Cancel</button>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        ${data.comments[i].replyComments[j].content}
                    </div>
                </div>`;
          }
        } else {
          replies = ``;
        }
        const item = `
        <div class="container comment_container py-2 bg-light rounded-3">
            <!-- parent comments section -->
            <div class="d-flex mb-1">
            <div class="flex-shrink-0"><img class="rounded-circle mx-auto d-block" 
                                    src="${data.comments[i].author_profile_image_url}" alt="..." width="50" height="50"></div>
                <div class="ms-3">
                    <div class="d-flex ">
                        <strong class="me-2">${data.comments[i].author_username}</strong>
                        <small class="text-muted fst-italic mb-2 me-2"> | ${data.comments[i].created} </small>

                        ${three_dot_button}
                        <div class="dropdown-menu dropdown-menu-lg-end p-2 ">
                            ${edit_comment_button}
                            ${delete_comment_form}
                        </div>
                        <!-- Confirmation Modal for Delete Comment -->
                        <div class="modal fade" id="confirmDeleteModal-${data.comments[i].id}" tabindex="-1" aria-labelledby="confirmDeleteModalLabel" aria-hidden="true">
                            <div class="modal-dialog modal-dialog-centered">
                                <div class="modal-content">
                                    <div class="modal-body my-2">
                                        Are you sure you want to delete this comment?
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                        <form id="delete-comment-form">
                                            <button type="submit" class="btn btn-danger"
                                                name="delete_comment" id="delete_comment" data-comment-id="${data.comments[i].id}"><i class="bi bi-trash"> </i> Delete
                                                </button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- Edit form for the comment -->
                        <div class="modal fade" id="editCommentModal-${data.comments[i].id}" tabindex="-1"
                            aria-labelledby="editCommentModalLabel" aria-hidden="true">
                            <div class="modal-dialog">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title" id="editCommentModalLabel">Edit Comment</h5>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal"
                                            aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body">
                                        <form id="editCommentForm_${data.comments[i].id}" method="post"
                                            
                                            <textarea class="form-control" name="content"
                                                rows="3">${data.comments[i].content}</textarea>
                                            <button type="submit" class="btn btn-primary mt-2"
                                                name="edit_comment" id="edit_comment">Update</button>
                                            <button type="button" class="btn btn-secondary mt-2"
                                                data-bs-dismiss="modal">Cancel</button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                       
                    </div>
                    ${data.comments[i].content}
                </div>
            </div>
            ${reply_button}
            <!-- Reply comments section -->
            <div class="container r_comment_container col-10 mb-3 border-start" id="replies_comment_box-${data.comments[i].id}" value="${data.comments[i].id}">
            ${replies}
            </div>
        </div>
        <!-- Reply comment form for the comment -->
              <div class="modal fade" id="replyCommentModal-${data.comments[i].id}" tabindex="-1"
                  aria-labelledby="replyCommentModalLabel" aria-hidden="true">
                  <div class="modal-dialog">
                      <div class="modal-content">
                          <div class="modal-header">
                              <h5 class="modal-title" id="replyCommentModalLabel">Reply Comment</h5>
                              <button type="button" class="btn-close" data-bs-dismiss="modal"
                                  aria-label="Close"></button>
                          </div>
                          <div class="modal-body">
                              <form id="reply-comment-form-${data.comments[i].id}">
                                  <input type="hidden" id="parent_comment_id" name="parent_comment_id" value="${data.comments[i].id}">
                                  <textarea class="form-control" id="r-comment-content" name="reply_content" rows="3"
                                      placeholder="add reply..." required></textarea>
                                  <button type="submit" class="btn btn-primary mt-2" id="add_reply" value="${data.comments[i].id}">Reply</button>
                                  <button type="button" class="btn btn-secondary mt-2" data-bs-dismiss="modal">Cancel</button>
                              </form>
                          </div>
                      </div>
                  </div>
              </div>
              `;

        // comments_box.innerHTML += item;
        comments_box.insertAdjacentHTML("afterbegin", item);
      }
      // call delete comment function
      const deleteCommentButtons = document.querySelectorAll('#delete_comment')
      deleteCommentButtons.forEach(button => {
        button.addEventListener('click', function (e) {
          e.preventDefault();
          const commentId = button.getAttribute('data-comment-id');
      
          deleteComment(commentId);
        });
      });
      
      // call create reply function
      const replycommentForm = document.querySelectorAll("#add_reply")
      replycommentForm.forEach(button => {
        button.addEventListener('click', function (e) {
          e.preventDefault();
          const parent_comment_id = this.value;
          create_reply(parent_comment_id);
          document.getElementById("r-comment-content").value=''
        });
      });

      // call delete reply comment function
      const deleteReplyCommentButtons = document.querySelectorAll('#delete_reply_comment')
      deleteReplyCommentButtons.forEach(button => {
        button.addEventListener('click', function (e) {
          e.preventDefault();
          const replyCommentId = button.getAttribute('data-reply_comment-id');

          deleteReplyComment(replyCommentId);
        });
      });
    });
}


// Create comment
commentForm.addEventListener("submit", function (e) {
  e.preventDefault();
  const post_id = commentForm.dataset.postId;
  const content = document.getElementById("comment-content").value;
  const author = document.getElementById("auth_user").textContent; 
  const authorID = document.getElementById("auth_user").getAttribute("auth-user-id"); 
  const author_img = document.getElementById("auth_user_img").getAttribute("src");
  // Send an AJAX POST request to create the new comment
  fetch("/api-comments/create/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ 'author_username': author,  "author_profile_image_url": author_img,"content": content,  "post": post_id, "author": authorID }),
  })
    .then((response) => response.json())
    .then((data) => {
      // console.log(data)
      // Clear the comment input field
      document.getElementById("comment-content").value = "";

      // Create HTML for the new comment
      const newComment = `
      <div class="container comment_container py-2 bg-light rounded-3">
          <!-- parent comments section -->
          <div class="d-flex mb-1">
          <div class="flex-shrink-0"><img class="rounded-circle mx-auto d-block" 
                                  src="${author_img}" alt="..." width="50" height="50"></div>
              <div class="ms-3">
                  <div class="d-flex ">
                      <strong class="me-2">${author}</strong>
                      <small class="text-muted fst-italic mb-2 me-2"> | ${data.created} </small>
                      <button class="btn btn-light" data-bs-toggle="dropdown" aria-haspopup="true"
                      aria-expanded="false">
                      <i class="bi bi-three-dots-vertical"></i>
                  </button>
                      <div class="dropdown-menu dropdown-menu-lg-end p-2 ">
                      <button class="btn btn-light text-start" data-bs-toggle="modal"
                      data-bs-target="#editCommentModal-${data.id}"
                      data-comment-id="${data.id}"><i class="bi bi-pencil"> </i> Edit
                      Comment
                  </button>
                  <form>                  
                  <button type="button" class="btn btn-light text-start" data-bs-toggle="modal" data-bs-target="#confirmDeleteModal-${data.id}">
                      <i class="bi bi-trash"></i> Delete Comment
                  </button>
              </form>
                      </div>
                      <!-- Confirmation Modal for Delete Comment -->
                      <div class="modal fade" id="confirmDeleteModal-${data.id}" tabindex="-1" aria-labelledby="confirmDeleteModalLabel" aria-hidden="true">
                          <div class="modal-dialog modal-dialog-centered">
                              <div class="modal-content">
                                  <div class="modal-body my-2">
                                      Are you sure you want to delete this comment?
                                  </div>
                                  <div class="modal-footer">
                                      <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                      <form >
                                         
                                          <button type="submit" class="btn btn-danger"
                                              name="delete_comment" id="delete_comment"><i class="bi bi-trash"> </i> Delete
                                              </button>
                                      </form>
                                  </div>
                              </div>
                          </div>
                      </div>
                      <!-- Edit form for the comment -->
                      <div class="modal fade" id="editCommentModal-${data.id}" tabindex="-1"
                          aria-labelledby="editCommentModalLabel" aria-hidden="true">
                          <div class="modal-dialog">
                              <div class="modal-content">
                                  <div class="modal-header">
                                      <h5 class="modal-title" id="editCommentModalLabel">Edit Comment</h5>
                                      <button type="button" class="btn-close" data-bs-dismiss="modal"
                                          aria-label="Close"></button>
                                  </div>
                                  <div class="modal-body">
                                      <form id="editCommentForm_${data.id}" method="post"
                                          
                                          <textarea class="form-control" name="content"
                                              rows="3">${content}</textarea>
                                          <button type="submit" class="btn btn-primary mt-2"
                                              name="edit_comment" id="edit_comment">Update</button>
                                          <button type="button" class="btn btn-secondary mt-2"
                                              data-bs-dismiss="modal">Cancel</button>
                                      </form>
                                  </div>
                              </div>
                          </div>
                      </div>
                     
                  </div>
                  ${content}
              </div>
          </div>
          <div class="col-2 mb-3">
                
            <div class="d-flex justify-content-end">
            <button class="btn btn-light reply-button my-2 text-muted" data-bs-toggle="modal"
                data-bs-target="#replyCommentModal-${data.id}"
                data-comment-id="${data.id}"><i class="bi bi-reply"></i> Reply
            </button></div>
            
        </div>
      </div>
            `;

      // Append the new comment to the comments_box
      comments_box.insertAdjacentHTML("afterbegin", newComment);
    })
    .catch((error) => {
      console.error("Error creating comment:", error);
    });
});

// Create Reply of comment
function create_reply(parent_comment_id){
    const replycommentsBox = document.getElementById(`replies_comment_box-${parent_comment_id}`);
    const formId = `reply-comment-form-${parent_comment_id}`;
    const post_id = commentForm.dataset.postId;
    const content = document.getElementById(formId).elements.reply_content.value;
    const author = document.getElementById("auth_user").textContent; 
    const authorID = document.getElementById("auth_user").getAttribute("auth-user-id"); 
    const author_img = document.getElementById("auth_user_img").getAttribute("src");
    // Send an AJAX POST request to create the new Reply comment
    fetch("/api-r-comments/create/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({ 'author_username': author,  "author_profile_image_url": author_img, "parent_comment": parent_comment_id, "content": content,  "post": post_id, "author": authorID }),
    })
      .then((response) => response.json())
      .then((data) => {
        // console.log(data)
        // Create HTML for the new Reply comment
        const newReplies = `
                     <div class="d-flex col mb-1">
                          <div class="flex-shrink-0"><img class="rounded-circle mx-auto d-block"
                              src="${author_img}" alt="..." width="50" height="50"></div>
                      <div class="ms-2">
                          <div class="d-flex">
                              <strong class="me-1">${author}</strong>
                              <small class="text-muted fst-italic mb-2 me-1"> | ${data.created}
                              </small>
                              ${r_three_dot_button}
                              <div class="dropdown-menu dropdown-menu-lg-end p-2 ">
                                  ${r_edit_comment_button}
                                  ${r_delete_comment_form}
                              </div>
                              <!-- Confirmation Modal for Delete reply Comment -->
                              <div class="modal fade" id="confirmDeleteModal-${data.id}" tabindex="-1" aria-labelledby="confirmDeleteModalLabel" aria-hidden="true">
                                  <div class="modal-dialog modal-dialog-centered">
                                      <div class="modal-content">
                                          <div class="modal-body my-2">
                                              Are you sure you want to delete this comment?
                                          </div>
                                          <div class="modal-footer">
                                              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                              <form >
                                                  <button type="submit" id="delete_reply_comment" data-reply_comment-id="${data.id}" class="btn btn-danger" name="delete_reply_comment"
                                                      ><i class="bi bi-trash"> </i> Delete </button>
                                              </form>
                                          </div>
                                      </div>
                                  </div>
                              </div>
                              <!-- Edit form for the Reply comment -->
                              <div class="modal fade" id="editRCommentModal-${data.id}" tabindex="-1"
                                  aria-labelledby="editRCommentModalLabel" aria-hidden="true">
                                  <div class="modal-dialog">
                                      <div class="modal-content">
                                          <div class="modal-header">
                                              <h5 class="modal-title" id="editRCommentModalLabel">Edit Comment
                                              </h5>
                                              <button type="button" class="btn-close" data-bs-dismiss="modal"
                                                  aria-label="Close"></button>
                                          </div>
                                          <div class="modal-body">
                                              <form id="editCommentForm_${data.id}">
                                                  <textarea class="form-control" name="content"
                                                      rows="3">${content}</textarea>
                                                  <button type="submit" class="btn btn-primary mt-2"
                                                      name="edit_reply_comment">Update</button>
                                                  <button type="button" class="btn btn-secondary mt-2"
                                                      data-bs-dismiss="modal">Cancel</button>
                                              </form>
                                          </div>
                                      </div>
                                  </div>
                              </div>
                          </div>
                          ${content}
                      </div>
                  </div><br>
                    `;

        // Close the modal
        const modal = document.querySelector(`#replyCommentModal-${parent_comment_id}`);
        if (modal) {
          modal.classList.remove('show');
          modal.style.display = 'none'; 
        }
        // Remove the modal backdrop if it exists
        const modalBackdrop = document.querySelector('.modal-backdrop');
        if (modalBackdrop) {
          modalBackdrop.remove();
        }

        // Append the new Reply comment to the replies_comment_box
        replycommentsBox.insertAdjacentHTML("afterbegin", newReplies);
        // console.log("Reply Comment added successfully")
        document.getElementById(formId).elements.reply_content.value = ''
      })
      .catch((error) => {
        console.error("Error creating comment:", error);
      });
  };


// DELETE comment
function deleteComment(commentId) {
  const url = `/api-comments/delete/${commentId}/`;

  fetch(url, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
  })
    .then(function (response) {
      if (response.ok) {
        // console.log('Comment deleted successfully');
        
        // Close the modal
        const modalId = `#confirmDeleteModal-${commentId}`;
        const modal = document.querySelector(modalId);
        if (modal) {
          const bootstrapModal = new bootstrap.Modal(modal); // Assuming you are using Bootstrap modal
          bootstrapModal.hide();
        }

        // Remove the modal backdrop
        const modalBackdrop = document.querySelector('.modal-backdrop');
        if (modalBackdrop) {
          modalBackdrop.remove();
        }
        show_details_post()
        
      } else {
        console.error('Error deleting comment:', response.status);
      }
    })
    .catch((error) => {
      console.error('Error deleting comment:', error);
    });
}

// DELETE Reply of the comment
function deleteReplyComment(replyCommentId) {
  const url = `/api-r-comments/delete/${replyCommentId}/`;

  fetch(url, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
  })
    .then(function (response) {
      if (response.ok) {
        // console.log('Reply of the comment deleted successfully');
        
        // Close the modal
        const modalId = `#confirmDeleteModal-${replyCommentId}`;
        const modal = document.querySelector(modalId);
        if (modal) {
          const bootstrapModal = new bootstrap.Modal(modal); // Assuming you are using Bootstrap modal
          bootstrapModal.hide();
        }

        // Remove the modal backdrop
        const modalBackdrop = document.querySelector('.modal-backdrop');
        if (modalBackdrop) {
          modalBackdrop.remove();
        }
        show_details_post()
        
      } else {
        console.error('Error deleting reply comment:', response.status);
      }
    })
    .catch((error) => {
      console.error('Error deleting reply comment:', error);
    });
}




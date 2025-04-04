// AJAX Utility Functions
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Generic AJAX request function
async function makeRequest(url, method = "POST", data = null) {
  const csrftoken = getCookie("csrftoken");
  try {
    const headers = {
      "X-CSRFToken": csrftoken,
    };

    let requestBody = null;
    if (data instanceof FormData) {
      requestBody = data;
    } else if (data) {
      headers["Content-Type"] = "application/json";
      requestBody = JSON.stringify(data);
    }

    const response = await fetch(url, {
      method: method,
      headers: headers,
      body: requestBody,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

// Like/Dislike Handler
async function handleLike(noteId, action, event) {
  if (event) event.preventDefault();
  try {
    const response = await makeRequest(`/notes/${noteId}/${action}/`);
    const likeCount = document.querySelector(`#like-count-${noteId}`);
    const dislikeCount = document.querySelector(`#dislike-count-${noteId}`);
    const likeButton = document.querySelector(`#like-button-${noteId}`);
    const dislikeButton = document.querySelector(`#dislike-button-${noteId}`);

    if (likeCount) likeCount.textContent = response.likes;
    if (dislikeCount) dislikeCount.textContent = response.dislikes;

    if (response.user_has_liked) {
      likeButton.classList.add("active");
      dislikeButton.classList.remove("active");
    } else if (response.user_has_disliked) {
      dislikeButton.classList.add("active");
      likeButton.classList.remove("active");
    } else {
      likeButton.classList.remove("active");
      dislikeButton.classList.remove("active");
    }
  } catch (error) {
    console.error("Error handling like/dislike:", error);
  }
}

// Comment Handler
async function handleComment(noteId, commentForm, event) {
  event.preventDefault();
  try {
    const formData = new FormData(commentForm);
    const commentData = {
      content: formData.get("content"),
    };
    const response = await makeRequest(
      `/notes/${noteId}/comment/`,
      "POST",
      commentData
    );

    // Create new comment element with proper structure
    const commentHtml = `
      <div class="comment" id="comment-${response.id}">
        <div class="comment-header">
          <img src="${
            response.user_avatar || "/static/images/default-avatar.png"
          }" alt="Commenter Avatar" class="commenter-avatar">
          <span class="commenter-name">${response.author}</span>
        </div>
        <p class="comment-content">${response.content}</p>
        <form method="POST" action="/notes/${noteId}/comment/${
      response.id
    }/reply/" class="reply-form" data-note-id="${noteId}" data-comment-id="${
      response.id
    }">
          <div class="reply-input-container">
            <textarea name="content" placeholder="Write a reply..." required class="reply-input"></textarea>
            <button type="submit" class="submit-reply">Reply</button>
          </div>
        </form>
      </div>
    `;

    // Add new comment to the comments section
    const commentsContainer = document.querySelector(".comments-list");
    commentsContainer.insertAdjacentHTML("afterbegin", commentHtml);

    // Clear the form
    commentForm.reset();
  } catch (error) {
    console.error("Error posting comment:", error);
  }
}

// Reply Handler
async function handleReply(noteId, commentId, replyForm, event) {
  if (event) event.preventDefault();
  try {
    const formData = new FormData(replyForm);
    const replyData = {
      content: formData.get("content"),
    };

    const response = await makeRequest(
      `/notes/${noteId}/comment/${commentId}/reply/`,
      "POST",
      replyData
    );

    // Create new reply element
    const replyHtml = `
      <div class="reply">
        <div class="reply-header">
          <img src="${
            response.user_avatar || "/static/images/default-avatar.png"
          }" alt="Replier Avatar" class="replier-avatar">
          <span class="replier-name">${response.author}</span>
        </div>
        <p class="reply-content">${response.content}</p>
      </div>
    `;

    // Add new reply after the comment
    const parentComment = replyForm.closest(".comment");
    replyForm.insertAdjacentHTML("afterend", replyHtml);

    // Clear the form
    replyForm.reset();
  } catch (error) {
    console.error("Error posting reply:", error);
  }
}

// Mark Notification as Seen
// async function markNotificationAsSeen(notificationId) {
//   try {
//     await makeRequest(
//       `/notifications/notifications/mark-as-seen/${notificationId}/`,
//       "POST"
//     );
//     const notification = document.querySelector(
//       `#notification-${notificationId}`
//     );
//     if (notification) {
//       notification.classList.remove("unseen");
//       const markSeenButton = notification.querySelector(".mark-seen-button");
//       if (markSeenButton) {
//         markSeenButton.remove();
//       }
//     }
//   } catch (error) {
//     console.error("Error marking notification as seen:", error);
//   }
// }

// Mark All Notifications as Seen
// async function markAllNotificationsAsSeen() {
//   try {
//     await makeRequest("/notifications/notifications/mark-all-as-seen/", "POST");
//     document
//       .querySelectorAll(".notification-item.unseen")
//       .forEach((notification) => {
//         notification.classList.remove("unseen");
//         const markSeenButton = notification.querySelector(".mark-seen-button");
//         if (markSeenButton) {
//           markSeenButton.remove();
//         }
//       });
//     const notificationDot = document.querySelector(".point");
//     if (notificationDot) {
//       notificationDot.style.display = "none";
//     }
//   } catch (error) {
//     console.error("Error marking all notifications as seen:", error);
//   }
// }

// Event Listeners
document.addEventListener("DOMContentLoaded", function () {
  // Like/Dislike buttons
  document.addEventListener("click", function (e) {
    if (e.target.matches('[id^="like-button-"]')) {
      const noteId = e.target.id.split("-")[2];
      handleLike(noteId, "like");
    } else if (e.target.matches('[id^="dislike-button-"]')) {
      const noteId = e.target.id.split("-")[2];
      handleLike(noteId, "dislike");
    }
  });

  // Comment forms - using event delegation for dynamic forms
  document.addEventListener("submit", function (e) {
    if (e.target.classList.contains("comment-form")) {
      e.preventDefault();
      const noteId = e.target.dataset.noteId;
      handleComment(noteId, e.target, e);
    }
  });

  // Reply forms
  document.addEventListener("submit", function (e) {
    if (e.target.classList.contains("reply-form")) {
      e.preventDefault();
      const noteId = e.target.dataset.noteId;
      const commentId = e.target.dataset.commentId;
      handleReply(noteId, commentId, e.target);
    }
  });

  // Mark single notification as seen
  document.querySelectorAll(".mark-seen-button").forEach((button) => {
    button.addEventListener("click", function (e) {
      e.preventDefault();
      const notificationId = this.dataset.notificationId;
      markNotificationAsSeen(notificationId);
    });
  });

  // Mark all notifications as seen
  const markAllSeenButton = document.querySelector(".mark-all-seen");
  if (markAllSeenButton) {
    markAllSeenButton.addEventListener("click", function (e) {
      e.preventDefault();
      markAllNotificationsAsSeen();
    });
  }
});

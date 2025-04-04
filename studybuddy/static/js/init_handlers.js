document.addEventListener("DOMContentLoaded", function () {
  // Handle like/dislike buttons
  document
    .querySelectorAll(".like-button, .dislike-button")
    .forEach((button) => {
      if (!button.hasEventListener) {
        button.hasEventListener = true;
        button.addEventListener("click", function (event) {
          const noteId = this.id.split("-")[2];
          const action = this.classList.contains("like-button")
            ? "like"
            : "dislike";
          handleLike(noteId, action, event);
        });
      }
    });

  // Handle comment forms
  document.querySelectorAll(".comment-form").forEach((form) => {
    if (!form.hasEventListener) {
      form.hasEventListener = true;
      form.addEventListener("submit", async function (event) {
        event.preventDefault();
        event.stopPropagation();
        const noteId = this.getAttribute("data-note-id");
        await handleComment(noteId, this, event);
        return false;
      });
    }
  });

  // Handle reply forms
  document.querySelectorAll(".reply-form").forEach((form) => {
    if (!form.hasEventListener) {
      form.hasEventListener = true;
      form.addEventListener("submit", function (event) {
        const noteId = this.getAttribute("data-note-id");
        const commentId = this.getAttribute("data-comment-id");
        handleReply(noteId, commentId, this, event);
      });
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  // Remove event listeners from init-handlers.js to prevent duplicate bindings
  document
    .querySelectorAll(".like-button, .dislike-button")
    .forEach((button) => {
      const clone = button.cloneNode(true);
      button.parentNode.replaceChild(clone, button);
    });

  document.querySelectorAll(".comment-form").forEach((form) => {
    const clone = form.cloneNode(true);
    form.parentNode.replaceChild(clone, form);
  });

  document.querySelectorAll(".reply-form").forEach((form) => {
    const clone = form.cloneNode(true);
    form.parentNode.replaceChild(clone, form);
  });

  const MAX_VISIBLE_COMMENTS = 2;
  const MAX_VISIBLE_REPLIES = 1;

  function initializeCollapsible() {
    const commentsList = document.querySelector(".comments-list");
    const comments = Array.from(commentsList.querySelectorAll(".comment"));

    if (comments.length > MAX_VISIBLE_COMMENTS) {
      // Hide excess comments
      comments.slice(MAX_VISIBLE_COMMENTS).forEach((comment) => {
        comment.style.display = "none";
      });

      // Create and add 'Show More/Less Comments' button
      const toggleBtn = document.createElement("button");
      toggleBtn.className = "show-more-btn";
      toggleBtn.textContent = `Show More Comments (${
        comments.length - MAX_VISIBLE_COMMENTS
      })`;
      commentsList.appendChild(toggleBtn);

      let isExpanded = false;
      toggleBtn.addEventListener("click", function () {
        isExpanded = !isExpanded;
        comments.slice(MAX_VISIBLE_COMMENTS).forEach((comment) => {
          comment.style.display = isExpanded ? "block" : "none";
        });
        this.textContent = isExpanded
          ? "Show Less Comments"
          : `Show More Comments (${comments.length - MAX_VISIBLE_COMMENTS})`;
      });
    }

    // Handle replies for each comment
    comments.forEach((comment) => {
      const replies = Array.from(comment.querySelectorAll(".reply"));
      if (replies.length > MAX_VISIBLE_REPLIES) {
        // Hide excess replies
        replies.slice(MAX_VISIBLE_REPLIES).forEach((reply) => {
          reply.style.display = "none";
        });

        // Create and add 'Show More/Less Replies' button
        const toggleRepliesBtn = document.createElement("button");
        toggleRepliesBtn.className = "show-more-replies-btn";
        toggleRepliesBtn.textContent = `Show More Replies (${
          replies.length - MAX_VISIBLE_REPLIES
        })`;
        replies[replies.length - 1].insertAdjacentElement(
          "afterend",
          toggleRepliesBtn
        );

        let isRepliesExpanded = false;
        toggleRepliesBtn.addEventListener("click", function () {
          isRepliesExpanded = !isRepliesExpanded;
          replies.slice(MAX_VISIBLE_REPLIES).forEach((reply) => {
            reply.style.display = isRepliesExpanded ? "block" : "none";
          });
          this.textContent = isRepliesExpanded
            ? "Show Less Replies"
            : `Show More Replies (${replies.length - MAX_VISIBLE_REPLIES})`;
        });
      }
    });
  }

  initializeCollapsible();
});

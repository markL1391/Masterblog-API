// Runs once the window is fully loaded
window.onload = function () {
  // Attempt to retrieve the API base URL from local storage
  var savedBaseUrl = localStorage.getItem("apiBaseUrl");

  // If a base URL is found in local storage, load the posts
  if (savedBaseUrl) {
    document.getElementById("api-base-url").value = savedBaseUrl;
    loadPosts();
  }
};

// Fetch all posts from the API and display them on the page
function loadPosts() {
  // Retrieve base URL from input field and save it to local storage
  var baseUrl = document.getElementById("api-base-url").value.trim();
  localStorage.setItem("apiBaseUrl", baseUrl);

  // Read optional search/sort inputs
  const params = new URLSearchParams();

  const searchValue = document.getElementById("search")?.value?.trim();
  const sortValue = document.getElementById("sort")?.value;
  const directionValue = document.getElementById("direction")?.value;

  if (searchValue) params.set("search", searchValue);
  if (sortValue) params.set("sort", sortValue);
  if (directionValue) params.set("direction", directionValue);

  const url = baseUrl + "/posts" + (params.toString() ? `?${params.toString()}` : "");

  // GET request to /posts
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      const postContainer = document.getElementById("post-container");
      postContainer.innerHTML = "";

      data.forEach((post) => {
        const postDiv = document.createElement("div");
        postDiv.className = "post";

        const author = post.author ?? "Unknown";
        const date = post.date ?? "";

        postDiv.innerHTML = `
          <h2>${post.title}</h2>
          <p><small>By ${author}${date ? " • " + date : ""}</small></p>
          <p>${post.content}</p>
          <button onclick="deletePost(${post.id})">Delete</button>
        `;

        postContainer.appendChild(postDiv);
      });
    })
    .catch((error) => console.error("Error:", error));
}

// Send a POST request to add a new post
function addPost() {
  var baseUrl = document.getElementById("api-base-url").value.trim();

  var postTitle = document.getElementById("post-title").value;
  var postContent = document.getElementById("post-content").value;

  // Optional new fields
  var postAuthor = document.getElementById("post-author")?.value;
  var postDate = document.getElementById("post-date")?.value;

  // Build payload (only include optional fields if user typed something)
  const payload = {
    title: postTitle,
    content: postContent,
  };

  if (postAuthor && postAuthor.trim()) payload.author = postAuthor.trim();
  if (postDate && postDate.trim()) payload.date = postDate.trim(); // expected: YYYY-MM-DD

  fetch(baseUrl + "/posts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
    .then((response) => response.json())
    .then((post) => {
      console.log("Post added:", post);

      // Clear inputs
      document.getElementById("post-title").value = "";
      document.getElementById("post-content").value = "";
      if (document.getElementById("post-author")) document.getElementById("post-author").value = "";
      if (document.getElementById("post-date")) document.getElementById("post-date").value = "";

      loadPosts();
    })
    .catch((error) => console.error("Error:", error));
}

// Send a DELETE request to delete a post
function deletePost(postId) {
  var baseUrl = document.getElementById("api-base-url").value.trim();

  fetch(baseUrl + "/posts/" + postId, {
    method: "DELETE",
  })
    .then(() => {
      console.log("Post deleted:", postId);
      loadPosts();
    })
    .catch((error) => console.error("Error:", error));
}

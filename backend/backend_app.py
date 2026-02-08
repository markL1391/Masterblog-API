from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def get_next_id():
    """
    Generate the next integer ID.
    """
    return max(post["id"] for post in POSTS) + 1 if POSTS else 1

@app.route("/api/posts", methods=["GET"])
def get_posts():
    """Return (GET) all blog posts."""
    return jsonify(POSTS)

@app.route("/api/posts", methods=["POST"])
def add_post():
    """Create (POST) a new blog post."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    #Validate required fields.
    missing = []
    if "title" not in data or not str(data["title"]).strip():
        missing.append("title")
    if "content" not in data or not str(data["content"]).strip():
        missing.append("content")

    if missing:
        return jsonify({"error": "Missing required fields.", "missing": missing}), 400

    new_post = {
        "id": get_next_id(),
        "title": data["title"],
        "content": data["content"]
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201

@app.route("/api/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    """
    Delete a blog post.
    """

    # Find the post by ID.
    post_to_delete = None
    for post in POSTS:
        if post["id"] == id:
            post_to_delete = post
            break

    # If not found (error: 404).
    if post_to_delete is None:
        return jsonify({"error": f"Post with ID {id} not found."}), 404

    # Remove the post.
    POSTS.remove(post_to_delete)

    # Success message.
    return jsonify({"message": f"Post with ID {id} has been deleted successfully."}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

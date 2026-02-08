from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Masterblog API"}
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post.", "author": "Mark", "date": "2026-02-08"},
    {"id": 2, "title": "Second post", "content": "This is the second post.", "author": "Mark", "date": "2026-02-07"},
]


def get_next_id():
    """
    Generate the next integer ID.
    """
    return max(post["id"] for post in POSTS) + 1 if POSTS else 1


def find_post_by_id(post_id):
    """
    Find a post by its ID.
    Returns the post if found, otherwise None.
    """
    for post in POSTS:
        if post["id"] == post_id:
            return post
    return None

def is_valid_date(date_str: str) -> bool:
    """
    Validate whether a date string matches the format YYYY-MM-DD.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except (TypeError, ValueError):
        return False

def parse_date(date_str: str):
    """
    Convert a date string (YYYY-MM-DD) into a date object.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None

@app.route("/api/posts", methods=["GET"])
def get_posts():
    """
    Return (GET) all blog posts.
    (Optionally sorted by title/content).
    """
    results = list(POSTS)

    # Search across fields
    search = request.args.get("search", "").strip().lower()
    if search:
        results = [
            p for p in results
            if search in str(p.get("title", "")).lower()
            or search in str(p.get("content", "")).lower()
            or search in str(p.get("author", "")).lower()
            or search in str(p.get("date", "")).lower()
        ]

    # Optional sorting
    sort_field = request.args.get("sort")                   # None, "title", "content"
    direction = request.args.get("direction", "asc")        # "asc" or "desc"

    # If not sort -> keep original order.
    if not sort_field:
        return jsonify(results), 200

    # Validate sort field
    if sort_field not in {"title", "content", "author", "date"}:
        return jsonify({
            "error": "Invalid sort field. Allowed values: title, content, author, date."
        }), 400

    # Validate direction
    if direction not in {"asc", "desc"}:
        return jsonify({
            "error": "Invalid direction. Allowed values: asc, desc."
        }), 400

    reverse = (direction == "desc")

    # Sort a COPY so POSTS stays in original order
    if sort_field == "date":
        results = sorted(
        results,
        key=lambda p: (parse_date(p.get("date")) is None, parse_date(p.get("date"))),
        reverse=reverse
        )
    else:
        results = sorted(
            results,
            key=lambda p: (p.get(sort_field) or "").lower(),
            reverse=reverse
        )

    return jsonify(results), 200


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

    author = str(data.get("author", "Unknown")).strip() or "Unknown"
    date_str = data.get("date")

    if date_str is None:
        date_str = datetime.today().strftime("%Y-%m-%d")
    elif not is_valid_date(date_str):
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    new_post = {
        "id": get_next_id(),
        "title": data["title"],
        "content": data["content"],
        "author": author,
        "date": date_str
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201

@app.route("/api/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    """
    Delete a blog post by its ID.
    """

    # Find the post by ID.
    post = find_post_by_id(id)

    # If not found (error: 404).
    if post is None:
        return jsonify({"error": f"Post with ID {id} not found."}), 404

    # Remove the post.
    POSTS.remove(post)

    # Success message.
    return jsonify({"message": f"Post with ID {id} has been deleted successfully."}), 200


@app.route("/api/posts/<int:id>", methods=["PUT"])
def update_post(id):
    """
    Update an existing blog post by its ID.
    Only provided fields (title and/or content) will be updated.
    """
    post = find_post_by_id(id)

    if post is None:
        return jsonify({"error": f"Post with ID {id} not found."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    # Only update if provided (and not empty).
    if "title" in data and str(data["title"]).strip():
        post["title"] = data["title"]

    if "content" in data and str(data["content"]).strip():
        post["content"] = data["content"]

    if "author" in data and str(data["author"]).strip():
        post["author"] = data["author"]

    if "date" in data:
        if not is_valid_date(data["date"]):
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
        post["date"] = data["date"]

    return jsonify(post), 200


@app.route("/api/posts/search", methods=["GET"])
def search_posts():
    """
    Search posts by title and/or content using query parameters.
    """
    title_query = request.args.get("title", "").strip().lower()
    content_query = request.args.get("content", "").strip().lower()

    results = []

    for post in POSTS:
        title_text = post.get("title", "").lower()
        content_text = post.get("content", "").lower()

        title_match = True
        content_match = True

        # If title query is provided, it must be contained in the post title.
        if title_query:
            title_match = title_query in title_text

        # If content query is provided, it must be contained in the post content.
        if content_query:
            content_match = content_query in content_text

        # If both conditions pass, include the post
        if title_match and content_match:
            results.append(post)

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

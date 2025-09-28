from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_post_data(data):
    if 'title' not in data or 'content' not in data:
        return False
    return True



@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        new_post =  request.get_json()
        if not validate_post_data(new_post):
            return jsonify({'error': 'Invalid post data'}), 400
        #gerenrate new id
        new_id = max(post["id"] for post in POSTS) + 1
        new_post["id"] = new_id

        POSTS.append(new_post)

        return jsonify(new_post), 201

    else:
        return jsonify(POSTS)


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

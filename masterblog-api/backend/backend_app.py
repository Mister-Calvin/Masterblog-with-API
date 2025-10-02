from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "Welcome to My Blog", "content": "This is the beginning of something great."},
    {"id": 2, "title": "Python Tips", "content": "Use list comprehensions to write clean code."},
    {"id": 3, "title": "Flask Routing Explained", "content": "Flask uses decorators to create endpoints."},
    {"id": 4, "title": "JavaScript Basics", "content": "Let’s talk about variables and scope."},
    {"id": 5, "title": "Why APIs Matter", "content": "APIs let software talk to other software."},
    {"id": 6, "title": "Debugging in VS Code", "content": "Breakpoints and watches make your life easier."},
    {"id": 7, "title": "CSS Flexbox Guide", "content": "Align your items like a pro with flexbox."},
    {"id": 8, "title": "The Power of Git", "content": "Version control is essential for teams."},
    {"id": 9, "title": "REST vs. GraphQL", "content": "Two different approaches to API design."},
    {"id": 10, "title": "Handling Errors in Flask", "content": "Use error handlers to manage 404s and more."}
]


def validate_post_data(data):
    if 'title' not in data or 'content' not in data:
        return False
    return True

def find_post_by_id(post_id):
    for post in POSTS:
        if post['id'] == post_id:
            return post
    return None

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

    sort_field = request.args.get('sort')
    direction = request.args.get('direction')

    valid_sort_fields = ['title', 'content']
    valid_directions = ['asc', 'desc']

    posts = POSTS.copy()

    if sort_field:
        if sort_field not in valid_sort_fields:
            return jsonify({"error:" "Invalid sort field"}), 400

        if direction not in valid_directions:
            return jsonify({"error:" "Invalid direction"}), 400

        reverse = direction == 'desc'
        posts = sorted(posts, key=lambda post: post.get(sort_field, '').lower(), reverse=reverse)

    return jsonify(posts)


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = find_post_by_id(id)

    if post is None:
        return jsonify({'error': 'Post not found'}), 404

    POSTS.remove(post)

    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = find_post_by_id(id)
    if post is None:
        return jsonify({'error': 'Post not found'}), 404

    new_data = request.get_json()

    if 'title' in new_data:
        post['title'] = new_data['title']
    if 'content' in new_data:
        post['content'] = new_data['content']

    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title = request.args.get('title')
    content = request.args.get('content')

    filtered_posts = POSTS

    if title:
        filtered_posts = [post for post in filtered_posts if title.lower() in post.get('title', '').lower()]
    if content:
        filtered_posts = [post for post in filtered_posts if content.lower() in post.get('content', '').lower()]

    return jsonify(filtered_posts), 200











@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405







if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

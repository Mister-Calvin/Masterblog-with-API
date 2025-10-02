from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes



def load_data(file_path):
  """ Loads a JSON file """
  try:
      with open(file_path, "r") as handle:
        return json.load(handle)
  except FileNotFoundError:
      print(f"⚠️File {file_path} not found. Starting with empty list.")
      return []
  except json.JSONDecodeError:
      print(f"⚠️File {file_path} contains invalid JSON. Starting with empty list.")
      return []


def save_data(file_path, data):
    """Saves a list of posts to a JSON file."""
    try:
        with open(file_path, "w") as handle:
            json.dump(data, handle, indent=2)
    except Exception as e:
        print(f"❌Error saving data to {file_path}: {e}")



POSTS = load_data("POSTS.json")



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
        save_data("POSTS.json", POSTS)
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
    save_data("POSTS.json", POSTS)
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
    save_data("POSTS.json", POSTS)

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

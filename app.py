from flask import Flask, render_template, request, jsonify, send_from_directory
import markdown
import os

app = Flask(__name__)

VAULT_ROOT = os.environ.get("VAULT_ROOT", "/path/to/your/vault")  # Replace with your vault path

@app.route("/")
def index():
    files = []
    for root, _, filenames in os.walk(VAULT_ROOT):
        for filename in filenames:
            if filename.endswith(".md"):
                relative_path = os.path.relpath(os.path.join(root, filename), VAULT_ROOT)
                files.append(relative_path)
    return render_template("index.html", files=files)

@app.route('/<path:path>')
def serve_file(path=''):
    full_path = os.path.join(VAULT_ROOT, path)

    if os.path.isdir(full_path):
        files = []
        for item in os.listdir(full_path):
            item_path = os.path.join(path, item)
            files.append({
                'name': item,
                'path': item_path,
                'is_dir': os.path.isdir(os.path.join(VAULT_ROOT, item_path))
            })
        return render_template('index.html', files=files, current_path=path)
    elif os.path.isfile(full_path) and full_path.endswith('.md'):
        with open(full_path, 'r') as f:
            content = f.read()
        html_content = markdown.markdown(content)
        return render_template('file.html', content=html_content, file_path=path)
    else:
        return "File not found", 404


if __name__ == "__main__":
    app.run(debug=True)

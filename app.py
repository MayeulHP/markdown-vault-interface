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

@app.route("/file/<path:file_path>")
def serve_file(file_path):
    with open(os.path.join(VAULT_ROOT, file_path), "r") as f:
        content = f.read()
    html_content = markdown.markdown(content)
    return render_template("file.html", content=html_content)


@app.route("/api/save/<path:file_path>", methods=["POST"])
def save_file(file_path):
    content = request.form.get("content")
    file_path = os.path.join(VAULT_ROOT, file_path)
    with open(file_path, "w") as f:
        f.write(content)
    return "File saved successfully!"

@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

@app.route("/note/<path:note_path>", methods=["GET", "PUT", "PATCH"])
def note(note_path):
    """View, edit, or append to a note."""
    note_path = os.path.join(VAULT_ROOT, note_path + ".md")

    if request.method == "GET":
        if os.path.exists(note_path):
            with open(note_path, "r") as f:
                content = f.read()
            return content
        else:
            return "Note not found", 404

    elif request.method == "PUT":
        content = request.json.get("content")
        with open(note_path, "w") as f:
            f.write(content)
        return "Note updated", 200

    elif request.method == "PATCH":
        content = request.json.get("content")
        with open(note_path, "a") as f:
            f.write(content)
        return "Note appended", 200


@app.route("/search", methods=["GET"])
def search_vault():
    """Search across the entire vault."""
    query = request.args.get("q")
    results = []
    for root, _, files in os.walk(VAULT_ROOT):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()
                if query in content:
                    results.append(file_path)
    return jsonify(results)


@app.route("/folder/<path:folder_path>", methods=["GET"])
def folder(folder_path):
    """View folder contents."""
    folder_path = os.path.join(VAULT_ROOT, folder_path)
    if os.path.exists(folder_path):
        items = os.listdir(folder_path)
        return jsonify(items)
    else:
        return "Folder not found", 404


@app.route("/note/<path:note_path>/lines/<int:start_line>-<int:end_line>", methods=["GET", "PATCH"])
def note_lines(note_path, start_line, end_line):
    """View or edit specific lines of a note."""
    note_path = os.path.join(VAULT_ROOT, note_path + ".md")

    if request.method == "GET":
        if os.path.exists(note_path):
            with open(note_path, "r") as f:
                lines = f.readlines()
            if 0 <= start_line <= end_line < len(lines):
                return "".join(lines[start_line:end_line+1])
            else:
                return "Invalid line range", 400
        else:
            return "Note not found", 404

    elif request.method == "PATCH":
        if os.path.exists(note_path):
            with open(note_path, "r") as f:
                lines = f.readlines()
            if 0 <= start_line <= end_line < len(lines):
                new_content = request.json.get("content")
                lines[start_line:end_line+1] = [new_content + "\n"]
                with open(note_path, "w") as f:
                    f.writelines(lines)
                return "Lines updated", 200
            else:
                return "Invalid line range", 400
        else:
            return "Note not found", 404


@app.route("/note/<path:note_path>/search", methods=["GET"])
def search_note(note_path):
    """Search within a note."""
    note_path = os.path.join(VAULT_ROOT, note_path + ".md")
    query = request.args.get("q")

    if os.path.exists(note_path):
        with open(note_path, "r") as f:
            content = f.read()
        if query in content:
            return "Found", 200
        else:
            return "Not found", 404
    else:
        return "Note not found", 404



if __name__ == "__main__":
    app.run(debug=True)

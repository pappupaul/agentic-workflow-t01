from flask import Flask, jsonify, render_template, request
from datetime import datetime, timezone
import platform
import sys
import os

app = Flask(__name__)

# In-memory store for test items
items = []
next_id = 1


@app.route("/")
def index():
    """Serve the main dashboard page."""
    return render_template("index.html")


@app.route("/api/health")
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
    })


@app.route("/api/items", methods=["GET"])
def get_items():
    """Get all items."""
    return jsonify(items)


@app.route("/api/items", methods=["POST"])
def create_item():
    """Create a new item."""
    global next_id
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    item = {
        "id": next_id,
        "name": data["name"],
        "description": data.get("description", ""),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    next_id += 1
    items.append(item)
    return jsonify(item), 201


@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    """Delete an item by ID."""
    global items
    original_len = len(items)
    items = [i for i in items if i["id"] != item_id]
    if len(items) == original_len:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"message": "Item deleted"}), 200


@app.route("/api/echo", methods=["POST"])
def echo():
    """Echo back whatever JSON is sent."""
    data = request.get_json(silent=True)
    return jsonify({"echo": data})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

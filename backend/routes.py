from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all pictures data."""
    if data:
        return jsonify(data), 200
    return jsonify({"message": "No pictures found"}), 404

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<id>", methods=["GET"])
def get_picture_by_id(id):
    """Return a picture by its id."""
    try:
        id = int(id)  # Convert the id from the URL to an integer
    except ValueError:
        return jsonify({"message": "Invalid ID format"}), 400

    for picture in data:
        if picture["id"] == id:
            return jsonify(picture), 200
    return jsonify({"message": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture."""
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), 400

    picture = request.get_json()

    # Check if the picture has an 'id'
    if 'id' not in picture:
        return jsonify({"message": "Picture must have an 'id'"}), 400

    # Check if a picture with the same id already exists
    for existing_picture in data:
        if existing_picture["id"] == picture["id"]:
            return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

    # Append the new picture to the data list
    data.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update an existing picture."""
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), 400

    updated_picture = request.get_json()

    # Find the picture in the data list
    for index, picture in enumerate(data):
        if picture["id"] == id:
            # Update the picture with the incoming request data
            data[index] = {**picture, **updated_picture}
            return jsonify(data[index]), 200

    # If the picture does not exist, return a 404 error
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by its id."""
    # Find the picture in the data list
    for index, picture in enumerate(data):
        if picture["id"] == id:
            # Remove the picture from the data list
            del data[index]
            return '', 204  # Return an empty body with a 204 status code

    # If the picture does not exist, return a 404 error
    return jsonify({"message": "picture not found"}), 404
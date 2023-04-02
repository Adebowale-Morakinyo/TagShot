from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from sqlalchemy.orm import load_only

from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import ScreenshotModel, TagModel
from schemas import ScreenshotSchema, ScreenshotUploadSchema
from datetime import datetime


blp = Blueprint("screenshots", __name__, description="Operations on screenshots.")


@blp.route("/screenshots")
class ScreenshotList(MethodView):
    @blp.response(200, ScreenshotSchema(many=True))
    def get(cls):
        schema = ScreenshotSchema(many=True)
        screenshots = ScreenshotModel.query.all()
        result = schema.dump(screenshots)
        return jsonify({'screenshots': result})
    
    @blp.arguments(ScreenshotUploadSchema)
    @blp.response(201, ScreenshotSchema)
    def post(cls, screenshot_data):
        screenshot_schema = ScreenshotSchema()

        # check if screenshot with the same file_path exists
        existing_screenshot = ScreenshotModel.find_by_file_path(screenshot_data["file_path"])
        if existing_screenshot:
            return jsonify({"message": "Screenshot already exists."}), 400

        # create new screenshot object
        screenshot = ScreenshotModel(file_path=screenshot_data["file_path"])
        screenshot.created_at = datetime.utcnow()
        db.session.add(screenshot)

        # create new tag objects and associate with the screenshot
        for tag_name in screenshot_data["tags"]:
            tag = TagModel(name=tag_name)
            screenshot.tags.append(tag)

        # save the new screenshot to the database
        db.session.commit()

        # serialize and return the saved screenshot
        result = screenshot_schema.dump(screenshot)
        return jsonify(result), 201
    
    
@blp.route("/screenshots/<string:screenshot_id>")
class Screenshot(MethodView):
    @blp.response(200, ScreenshotSchema)
    def get(cls, screenshot_id):
        schema = ScreenshotSchema()
        try:
            screenshot = ScreenshotModel.query.get_or_404(screenshot_id)
        except exc.SQLAlchemyError:
            return jsonify({'message': 'Screenshot not found'}), 404
        result = schema.dump(screenshot)
        return jsonify({'screenshot': result}), 200
    
    
    def delete(cls, screenshot_id):
        try:
            screenshot = ScreenshotModel.query.get_or_404(screenshot_id)
        except exc.SQLAlchemyError:
            return jsonify({'message': 'Screenshot not found'}), 404
        db.session.delete(screenshot)
        db.session.commit()
        return jsonify({'message': 'Screenshot deleted successfully'}), 200

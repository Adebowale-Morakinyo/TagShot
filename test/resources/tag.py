from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from sqlalchemy.orm import load_only

from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import ScreenshotModel, TagModel
from schemas import UpdateTagSchema, ScreenshotSchema, TagSchema

blp = Blueprint("tags", __name__, description="Operations with tags")


@blp.route("/screenshot/<string:screenshot_id>/tags")
class Tag(MethodView):
    @blp.arguments(UpdateTagSchema)
    @blp.response(200, ScreenshotSchema)
    def put(self, screenshot_data, screenshot_id):
        schema = TagSchema(many=True)
        try:
            screenshot = ScreenshotModel.query.get_or_404(screenshot_id)
        except exc.SQLAlchemyError:
            return jsonify({'message': 'Screenshot not found'}), 404
        
        tags = screenshot_data['tags']
        if not tags:
            return jsonify({'message': 'No tags provided'}), 400
        
        screenshot.tags.clear()  # remove all existing tags
        for tag_data in tags:
            try:
                tag = TagModel.query.filter_by(name=tag_data['name']).one()
            except NoResultFound:
                tag = Tag(name=tag_data['name'])
            screenshot.tags.append(tag)
        db.session.commit()
        result = schema.dump(screenshot.tags)
        return jsonify({'tags': result}), 200
    
    
@blp.route("/screenshots/tags")
class TagList(MethodView):
    @blp.response(200, TagSchema)
    def get(self):
        schema = TagSchema(many=True)
        tags = TagModel.query.all()
        result = schema.dump(tags)
        return jsonify({'tags': result}), 200
    
    
@blp.route("/screenshots/tags/<string:tag_name>")
class SearchScreenshot(MethodView):
    @blp.response(200, ScreenshotSchema)
    def get(self, tag_name, date):
        schema = ScreenshotSchema(many=True)
        try:
            tag = TagModel.query.filter_by(name=tag_name).one()
        except NoResultFound:
            return jsonify({'message': 'Tag not found'}), 404
        screenshots = tag.screenshots
        result = schema.dump(screenshots)
        return jsonify({'screenshots': result}), 200
            
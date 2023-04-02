from marshmallow import Schema, fields

class ScreenshotUploadSchema(Schema):
    file_path = fields.String(required=True)
    tags = fields.List(fields.String(), required=True)

class UpdateTagSchema(Schema):
    tags = fields.List(fields.String())


class TagSchema(Schema):
    name = fields.String(required=True)
    count = fields.Integer(required=True)


class ScreenshotSchema(Schema):
    id = fields.Integer(dump_only=True)
    file_path = fields.String(required=True)
    tags = fields.List(fields.String(), required=True)
    created_at = fields.DateTime(dump_only=True)


class ScreenshotListSchema(Schema):
    screenshots = fields.List(fields.Nested(ScreenshotSchema), required=True)
    tags = fields.List(fields.Nested(TagSchema), required=True)

    
from datetime import datetime
from db import db


screenshot_tags = db.Table(
    "screenshot_tags",
    db.Column("screenshot_id", db.Integer, db.ForeignKey("screenshots.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id")),
)


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"<Tag {self.name}>"

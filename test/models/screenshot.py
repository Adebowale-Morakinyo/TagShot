from db import db
from datetime import datetime

from sqlalchemy.orm import backref


class ScreenshotModel(db.Model):
    __tablename__ = "screenshots"

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    tags = db.relationship(
        "TagModel",
        secondary="screenshot_tags",
        backref=backref("screenshots", lazy="dynamic"),
        lazy="dynamic",
    )

    def __repr__(self):
        return f'<Screenshot {self.id}>'
    
    
    @classmethod
    def find_by_file_path(cls, file_path):
        return cls.query.filter_by(file_path=file_path).first()

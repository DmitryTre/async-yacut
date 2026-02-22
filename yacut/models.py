from datetime import datetime, UTC

import random
import string

from yacut import db
from flask import url_for


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(2048))
    short = db.Column(db.String(6), unique=True, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now(UTC))

    def from_dict(self, data, custom_id=None):
        self.original = data['url']
        self.short = custom_id

    def to_dict(self):
        short_link = url_for(
            'redirect_to_url',
            short_link=self.short,
            _external=True
        )
        short_link = short_link.rstrip('/')
        return {
            'url': self.original,
            'short_link': short_link
        }

    @staticmethod
    def get_unique_short_id():
        while True:
            short_id = ''.join(random.choices(
                (string.ascii_letters + string.digits),
                k=6
            )
            )
            if not URLMap.query.filter_by(short=short_id).first():
                return short_id
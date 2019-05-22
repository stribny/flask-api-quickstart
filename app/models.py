from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=False, nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, username, email, password, created_on):
        self.username = username
        self.email = email
        self.password = password
        self.created_on = created_on

    def __repr__(self):
        return f"User(id={self.id},username={self.username})"


class BlacklistToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256))
    blacklisted_on = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, token, blacklisted_on):
        self.token = token
        self.blacklisted_on = blacklisted_on

    def __repr__(self):
        return f"BlacklistToken(id={self.id},token={self.token})"

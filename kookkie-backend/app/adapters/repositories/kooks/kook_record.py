from app import db, Model


class Kook(Model):
    id = db.Column(db.String(40), primary_key=True)
    email = db.Column(db.String(140), index=True)
    name = db.Column(db.String(140))
    is_admin = db.Column(db.Boolean)
    hashed_password = db.Column(db.String(140))
    password_reset_token = db.Column(db.String(140), index=True)
    password_reset_token_created_time = db.Column(db.DateTime())

    def __repr__(self):
        return '<Kook id={} email={}>'.format(self.id, self.email)
        
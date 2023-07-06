from app import db, Model

class KookkieSession(Model):
    id = db.Column(db.String(40), primary_key=True)
    created_at = db.Column(db.DateTime, index=True)
    date = db.Column(db.String(140))
    kook_id = db.Column(db.String(140), index=True)
    kook_name = db.Column(db.String(140))
    name = db.Column(db.String(140))
    open = db.Column(db.Boolean)
    participants = db.relationship('KookkieParticipant', backref='session', lazy=True)

    def __repr__(self):
        return '<KookkieSession {}>'.format(self.id)


class KookkieParticipant(Model):
    id = db.Column(db.String(40), primary_key=True)
    joining_id = db.Column(db.String(40))
    kookkie_session_id = db.Column(db.String(40), db.ForeignKey('kookkie_session.id'), nullable=False)
    email = db.Column(db.String(320))

    def __repr__(self):
        return '<KookkieParticipant {}>'.format(self.email)


from app import db


class BookingTable(db.Model):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.String(100), nullable=True)
    full_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(70), nullable=False)
    cell_number = db.Column(db.String(20), nullable=False)
    selected_service = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    payment_status = db.Column(db.String(50), nullable=False, default='Pending')

    def __repr__(self):
        return f'<BookingTable {self.id}>'
    

class ServiceTable(db.Model):
    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<ServiceTable {self.id}>'
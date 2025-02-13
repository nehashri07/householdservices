from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    pin_code = db.Column(db.Integer, nullable=False)
    phone_no = db.Column(db.String, nullable=True)  # Using String for phone numbers
    services = db.relationship("Service", cascade="all,delete", backref="User", lazy=True)  # Adjusted backref name

  

class Professional(db.Model):
    __tablename__ = "Professional"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    full_name = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    address = db.Column(db.String, nullable=False)
    attachment_url=db.Column(db.String, nullable=True)
    pin_code = db.Column(db.Integer, nullable=False)
    phone_no = db.Column(db.String, nullable=True)
    service_name = db.Column(db.String(32), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    status=db.Column(db.String, nullable=True)
    services = db.relationship("Service", cascade="all,delete", backref="Professional", lazy=True)  # Adjusted backref name

class Service(db.Model):
    __tablename__ = "Service"
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(32), nullable=False)
    base_price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=True)
    pro_id = db.Column(db.Integer, db.ForeignKey("Professional.id"), nullable=True)

class ServiceRequest(db.Model):  
    __tablename__ = "service_request"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum("Pending", "Approved", "Completed", name="status_enum"), nullable=False)
    rating = db.Column(db.Float, nullable=True)  
    date = db.Column(db.Date)
    s_id = db.Column(db.Integer, db.ForeignKey("Service.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    pro_id = db.Column(db.Integer, db.ForeignKey("Professional.id"), nullable=False)





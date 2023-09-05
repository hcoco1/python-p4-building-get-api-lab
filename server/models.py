from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, event
from sqlalchemy_serializer import SerializerMixin

# Define a naming convention for foreign keys
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'
    
    # Serialization rule to avoid circular references
    serialize_rules = ('-baked_goods.bakery',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    baked_goods = db.relationship('BakedGood', backref='bakery', lazy=True)  
    
    def __repr__(self):
        return f'<Bakery {self.name} {self.created_at} {self.updated_at}>'

class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'
    
    # Serialization rule
    serialize_rules = ('-bakery.baked_goods',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))
    
    def __repr__(self):
        return f'<BakedGood {self.name} {self.price} {self.created_at} {self.updated_at}>'

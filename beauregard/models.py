from beauregard import app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#starting that ol database

db = SQLAlchemy(app)

ma = Marshmallow(app)

#create the models for the database. Each table in the ERD
#that was created will be a model below. Each one will need 
#an init and probably no other methods at this point...
#We'll need to create a route page that will do everything that
#we need to show the user/admin/whatever.
#and I think we'll rename id to sp_id etc etc as we go
#Everything with a foreign key has to have a backref relationship
#to the thing it's foreign key-ing from for it to work.
# the backref can be any variable name i want. doesn't matter. 

class Salesperson(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    car = db.relationship('Car', backref='Salesperson', lazy=True)
    invoice = db.relationship('Invoice', backref='Salesperson', lazy=True)

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    #probably you need to create a schema for every model you have. damn.

class SalespersonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name')

#initializing the schema for one or many salespeople to be shown

salesperson_schema = SalespersonSchema(strict=True)
salespeople_schema = SalespersonSchema(many=True, strict=True)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    new_used = db.Column(db.String(4), nullable = False)
    color = db.Column(db.String(50))
    #below i changed the backref from servce_history to car.
    service_history = db.relationship('Service_History', backref='Car', lazy=True)
    invoice_id = db.relationship('Invoice', backref='Car', lazy=True)
    salesperson_id = db.Column(db.Integer, db.ForeignKey('salesperson.id'), nullable=False)
    #service_ticket_id = db.relationship('Service_Ticket', backref='service_ticket', lazy=True)
    service_id = db.relationship('Service', backref='Car', lazy=True)

    def __init__(self, new_used, color, salesperson_id):
        self.new_used = new_used
        self.color = color
        self.salesperson_id = salesperson_id

class CarSchema(ma.Schema):
    class Meta:
        fields = ('id', 'new_used', 'color', 'salesperson_id')

car_schema = CarSchema(strict=True)
cars_schema = CarSchema(many=True, strict=True)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable = False)
    customer = db.relationship('Customer', backref='Invoice', lazy=True)
    #customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    salesperson_id = db.Column(db.Integer, db.ForeignKey('salesperson.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)

    def __init__(self, amount, salesperson_id, car_id):
        self.amount = amount
        self.salesperson_id = salesperson_id
        self.car_id = car_id

class InvoiceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'amount', 'salesperson_id', 'car_id')

invoice_schema = InvoiceSchema(strict=True)
invoices_schema = InvoiceSchema(many=True, strict=True)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=True)
    #service_ticket = db.relationship('Service_Ticket', backref='customer', lazy=True)

    def __init__(self, first_name, last_name, invoice_id, service_id):
        self.first_name = first_name
        self.last_name = last_name
        self.invoice_id = invoice_id
        self.service_id = service_id

class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'invoice_id', 'service_id')

customer_schema = CustomerSchema(strict=True)
customers_schema = CustomerSchema(many=True, strict=True)

class Service_History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)

    def __init__(self, car_id, service_id, customer_id):
        self.car_id = car_id
        self.service_id = service_id
        self.customer_id = customer_id
        return "yo i'm a service history and a service ticket???"

class Service_HistorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'car_id', 'service_id', 'customer_id')

service_history_schema = Service_HistorySchema(strict=True)
service_histories_schema = Service_HistorySchema(many=True, strict=True)


#class Service_Ticket(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
 #   car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
#    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
#    service_name = db.Column(db.String(40), db.ForeignKey('service.service_name'), nullable = False)


class Mechanics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    service = db.relationship('Service', backref='Mechanics', lazy=True)

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

class MechanicsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name')
mechanic_schema = MechanicsSchema(strict=True)
mechanics_schema = MechanicsSchema(many=True, strict=True)

#below is the combo table
#you might not have to add in the relationship between tables that 
#are going through the combo but i'm not sure. i.e. you might have to have
#the one in the mechanics table but maybe not. 

#tags = db.Table('tags',
 #   db.Column('service_id', db.Integer, db.ForeignKey('service.id'), primary_key=True),
 #   db.Column('parts_id', db.Integer, db.ForeignKey('parts.id'), primary_key=True),
 #   db.Column('mechanics_id', db.Integer, db.ForeignKey('mechanics.id'), primary_key=True)
#)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(50))
    service_type = db.Column(db.String(50))
    mechanics_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    customer_id = db.relationship('Customer', backref='Service', lazy=True)
    service_history = db.relationship('Service_History', backref='Service', lazy=True)
    parts = db.relationship('Parts', backref='Service', lazy=True)
    #this next line is the relationship to the combo table
    #after db.Relationship that word in the ' ' needs to be the other
    #table that you're going through the subtable for for a relationship
    
    #tags = db.relationship('Mechanics', secondary=tags, lazy='subquery',
    #    backref=db.backref('service', lazy=True))
   # tags = db.relationship('Parts', secondary=tags, lazy='subquery',
    #    backref=db.backref('service', lazy=True))

    def __init__(self, service_name, service_type, mechanics_id, car_id):
        self.service_name = service_name
        self.service_type = service_type
        self.mechanics_id = mechanics_id
        self.car_id = car_id

class ServiceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'service_name', 'service_type', 'mechanics_id', 'car_id')

service_schema = ServiceSchema(strict=True)
services_schema = ServiceSchema(many=True, strict=True)

class Parts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_name = db.Column(db.String(50))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)

    def __init__(self, part_name, service_id):
        self.part_name = part_name
        self.service_id = service_id

class PartsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'part_name', 'service_id')

part_schema = PartsSchema(strict=True)
parts_schema = PartsSchema(many=True, strict=True)
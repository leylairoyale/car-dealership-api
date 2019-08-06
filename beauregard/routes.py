from beauregard import app
from beauregard.models import db, salesperson_schema, salespeople_schema, Salesperson, Car, car_schema, cars_schema
from beauregard.models import Invoice, invoice_schema, invoices_schema, Customer, customer_schema, customers_schema
from beauregard.models import Service_History, service_history_schema, service_histories_schema, Mechanics, mechanic_schema, mechanics_schema
from beauregard.models import Service, service_schema, services_schema, Parts, part_schema, parts_schema
from flask import request, jsonify

#Routes needed here will include:
# 1. route to show a single car
# 2. route to show all cars
# 3. route to show all used cars
# 4. route to show all new cars
# 5. route to show all services incl. repairs
# 6. route to show repairs only
# 7. route to show services only
# 8. route to pull up single customer info
# 9. route to show all customer info
# 10. route to show single salesperson info
# 11. route to show all sa
# 12. route to pull up an invoice
# 13. route to pull up all invoices

#route creating a salesperson
@app.route('/salesperson', methods=["GET", "POST"])
def add_salesperson():
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]

    new_salesperson = Salesperson(first_name, last_name)
    
    db.session.add(new_salesperson)
    db.session.commit()

    return salesperson_schema.jsonify(new_salesperson)

#route retrieving a single salesperson
@app.route('/salesperson/<id>', methods=["GET"])
def get_salesperson(id):
    salesperson = Salesperson.query.get(id)
    return salesperson_schema.jsonify(salesperson)

#route retrieving all salespeople
@app.route('/salespeople', methods=["GET"])
def get_salespeople():
    all_salespeople = Salesperson.query.all()
    result = salespeople_schema.dump(all_salespeople)
    return jsonify(result.data)

#route updating a salesperson
@app.route('/salesperson/<id>', methods=["PUT"])
def update_salesperson(id):
    salesperson = Salesperson.query.get(id)

    first_name = request.json["first_name"]
    last_name = request.json["last_name"]

    salesperson.first_name = first_name
    salesperson.last_name = last_name

    db.session.commit()
    return salesperson_schema.jsonify(salesperson)

#route deleting a salesperson
#does not work if a salesperson is connected to another table.
@app.route('/salesperson/<id>', methods=["DELETE"])
def delete_salesperson(id):
    salesperson = Salesperson.query.get(id)
    db.session.delete(salesperson)
    db.session.commit()
    return salesperson_schema.jsonify(salesperson)


#route creating a car
@app.route('/car', methods=["GET", "POST"])
def add_car():
    new_used = request.json["new_used"]
    color = request.json["color"]
    salesperson_id = request.json["salesperson_id"]

    new_car = Car(new_used, color, salesperson_id)

    db.session.add(new_car)
    db.session.commit()

    return car_schema.jsonify(new_car)

#route getting 1 car
@app.route('/car/<id>', methods=["GET"])
def get_car(id):
    car = Car.query.get(id)
    return car_schema.jsonify(car)

#route getting all cars
@app.route('/cars', methods=["GET"])
def get_cars():
    all_cars = Car.query.all()
    result = cars_schema.dump(all_cars)
    return jsonify(result.data)

#route updating a car
@app.route('/car/<id>', methods=["PUT"])
def update_car(id):
    car = Car.query.get(id)

    new_used = request.json["new_used"]
    color = request.json["color"]

    car.new_used = new_used
    car.color = color

    db.session.commit()
    return car_schema.jsonify(car)

#route deleting a car
@app.route('/car/<id>', methods=["DELETE"])
def delete_car(id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    return car_schema.jsonify(car)

#route creating an invoice
@app.route('/invoice', methods=["GET", "POST"])
def add_invoice():
    amount = request.json["amount"]
    salesperson_id = request.json["salesperson_id"]
    car_id = request.json["car_id"]

    new_invoice = Invoice(amount, salesperson_id, car_id)

    db.session.add(new_invoice)
    db.session.commit()
    return invoice_schema.jsonify(new_invoice)

#route updating an invoice
@app.route('/invoice/<id>', methods=["PUT"])
def update_invoice(id):
    invoice = Invoice.query.get(id)

    amount = request.json["amount"]
    salesperson_id = request.json["salesperson_id"]
    car_id = request.json["car_id"]

    invoice.amount = amount
    invoice.salesperson_id= salesperson_id
    invoice.car_id = car_id

    db.session.commit()
    return invoice_schema.jsonify(invoice)

#route deleting an invoice
@app.route('/invoice/<id>', methods=["DELETE"])
def delete_invoice(id):
    invoice = Invoice.query.get(id)
    db.session.delete(invoice)
    db.session.commit()
    return invoice_schema.jsonify(invoice)

#route getting an invoice by id
@app.route('/invoice/<id>', methods=["GET"])
def get_invoice(id):
    invoice = Invoice.query.get(id)
    return invoice_schema.jsonify(invoice)

#route getting all invoices
@app.route('/invoices', methods=["GET"])
def get_invoices():
    all_invoices = Invoice.query.all()
    result = invoices_schema.dump(all_invoices)
    return jsonify(result.data)

#route creating a customer
@app.route('/customer', methods=["GET", "POST"])
def create_customer():
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    invoice_id = request.json["invoice_id"]
    service_id = request.json["service_id"]

    new_customer = Customer(first_name, last_name, invoice_id, service_id)

    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer)

#route getting a customer by id
@app.route('/customer/<id>', methods=["GET"])
def get_customer(id):
    customer = Customer.query.get(id)
    return customer_schema.jsonify(customer)

#route getting all customers
@app.route('/customers', methods=["GET"])
def get_customers():
    all_customers = Customer.query.all()
    result = customers_schema.dump(all_customers)
    return jsonify(result.data)

#route updating a customer
@app.route('/customer/<id>', methods=["PUT"])
def update_customer(id):
    customer = Customer.query.get(id)

    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    invoice_id = request.json["invoice_id"]
    service_id = request.json["service_id"]

    customer.first_name = first_name
    customer.last_name = last_name
    customer.invoice_id = invoice_id
    customer.service_id = service_id

    db.session.commit()
    return customer_schema.jsonify(customer)

#route deleting a customer
@app.route('/customer/<id>', methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get(id)
    db.session.delete(customer)
    db.session.commit()
    return customer_schema.jsonify(customer)

#route getting a service history? not sure if this is right.
#@app.route('/service_history', methods=["GET"])
#def get_service_history():
    #i am unsure how to do this. my brain is melting.

#route creating a mechanic
@app.route('/mechanics', methods=["GET", "POST"])
def create_mechanics():
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]

    new_mechanic = Mechanics(first_name, last_name)

    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic)

#route viewing a single mechanic
@app.route('/mechanics/<id>', methods=["GET"])
def get_mechanic(id):
    mechanic = Mechanics.query.get(id)
    return mechanic_schema.jsonify(mechanic)

#route getting all mechanics
@app.route('/mechanicsss', methods=["GET"])
def get_mechanics():
    all_mechanics = Mechanics.query.all()
    result = mechanics_schema.dump(all_mechanics)
    return jsonify(result.data)

#route updating a mechanic
@app.route('/mechanic/<id>', methods=["PUT"])
def update_mechanic(id):
    mechanic = Mechanics.query.get(id)

    first_name = request.json["first_name"]
    last_name = request.json["last_name"]

    mechanic.first_name = first_name
    mechanic.last_name = last_name

    db.session.commit()
    return mechanic_schema.jsonify(mechanic)

#route deleting a mechanic
@app.route('/mechanic/<id>', methods=["DELETE"])
def delete_mechanic(id):
    mechanic = Mechanics.query.get(id)
    db.session.delete(mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic)

#route creating a service
@app.route('/service', methods=["GET", "POST"])
def create_service():
    service_name = request.json["service_name"]
    service_type = request.json["service_type"]
    mechanics_id = request.json["mechanics_id"]
    car_id = request.json["car_id"]

    new_service = Service(service_name, service_type, mechanics_id, car_id)

    db.session.add(new_service)
    db.session.commit()
    return service_schema.jsonify(new_service)

#route getting a service
@app.route('/service/<id>', methods=["GET"])
def get_serviced(id):
    service = Service.query.get(id)
    return service_schema.jsonify(service)

#route getting all services
@app.route('/services', methods=["GET"])
def get_services():
    all_services = Service.query.all()
    result = services_schema.dump(all_services)
    return jsonify(result.data)

#route updating a service
@app.route('/service/<id>', methods=["PUT"])
def update_service(id):
    service = Service.query.get(id)

    service_name = request.json["service_name"]
    service_type = request.json["service_type"]
    mechanics_id = request.json["mechanics_id"]
    car_id = request.json["car_id"]

    service.service_name = service_name
    service.service_type = service_type
    service.mechanics_id = mechanics_id
    service.car_id = car_id

    db.session.commit()
    return service_schema.jsonify(service)

#route deleting a service
@app.route('/service/<id>', methods=["DELETE"])
def delete_service(id):
    service = Service.query.get(id)
    db.session.delete(service)
    db.session.commit()
    return service_schema.jsonify(service)

#route creating a part
@app.route('/part', methods = ["GET", "POST"])
def create_part():
    part_name = request.json["part_name"]
    service_id = request.json["service_id"]

    new_part = Parts(part_name, service_id)

    db.session.add(new_part)
    db.session.commit()
    return part_schema.jsonify(new_part)

#route getting a part
@app.route('/part/<id>', methods=["GET"])
def get_part(id):
    part = Parts.query.get(id)
    return part_schema.jsonify(part)

#route getting all parts
@app.route('/parts', methods=["GET"])
def get_parts():
    all_parts = Parts.query.all()
    result = parts_schema.dump(all_parts)
    return jsonify(result.data)

#route updating a part
@app.route('/part/<id>', methods=["PUT"])
def update_part(id):
    part = Parts.query.get(id)

    part_name = request.json["part_name"]
    service_id = request.json["service_id"]

    parts.part_name = part_name
    parts.service_id = service_id

    db.session.commit()
    return part_schema.jsonify(part)

@app.route('/part/<id>', methods=["DELETE"])
def delete_part(id):
    part = Parts.query.get(id)
    db.session.delete(part)
    db.session.commit()
    return part_schema.jsonify(part)
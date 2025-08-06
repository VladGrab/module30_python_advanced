from flask import Flask, jsonify, request
from module_29_testing.hw.task.__init__ import db

def create_app():
    app = Flask(__name__)
    # app.config["DEBUG"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///hw.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config["SQLALCHEMY_ECHO"] = True
    # app.config["SQLALCHEMY_RECORD_QUERIES"] = True
    db.init_app(app=app)

    from module_29_testing.hw.task.models import Client, Parking, Client_Parking
    # with app.app_context():
    #     db.create_all()
    @app.before_request
    def before_request_func():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route('/hello')
    def hello():
        return "Hello"

    @app.route('/clients', methods=['GET', 'POST'])
    def clients():
        if request.method == 'GET':
            clients = db.session.query(Client).all()
            clients_list = []
            for client in clients:
                client_as_dict = client.to_json()
                clients_list.append(client_as_dict)
            return jsonify(clients_list=clients_list), 200
        if request.method == 'POST':
            json_data = request.get_json()
            new_client = Client.create_client(data=json_data)
            return new_client, 201

    @app.route('/clients/<int:id>')
    def client_info(id):
        client = Client.get_client_by_id(id)
        return client

    @app.route('/parking', methods=['POST'])
    def add_new_parking_place():
        data = request.get_json()
        new_parking = Parking.create_parking_place(data)
        return new_parking, 201

    @app.route('/client_parking', methods=['POST', 'DELETE'])
    def client_parkings():
        if request.method == 'POST':
            data = request.get_json()
            parking_status = Parking.check_free_space_and_opened_parking(data['parking_id'])
            if parking_status == True:
                client_in = Client_Parking.client_in_parking(data)
                Parking.take_parking_space(id=data['parking_id'])
                return client_in, 201
            else:
                return parking_status

        if request.method == 'DELETE':
            data = request.get_json()
            if Client.check_credit_card(data['client_id']) == True:
                client_out = Client_Parking.client_out_parking(data)
                Parking.free_up_parking_space(id=data['parking_id'])
                return client_out
            else:
                return Client.check_credit_card(data['client_id'])
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
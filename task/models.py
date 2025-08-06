import datetime
from typing import Any, Dict

from sqlalchemy import text

from module_29_testing.hw.task.main import db


class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50), nullable=True)
    car_number = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return f"Клиент {self.name} {self.surname}"

    @classmethod
    def get_all_client(cls):
        return db.session.query(Client).all()

    @classmethod
    def get_client_by_id(cls, client_id):
        records = db.session.query(Client).filter(Client.id == client_id).one()
        client = records.to_json()
        return client

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}

    @classmethod
    def create_client(cls, data):
        new_client = Client(name=data['name'], surname=data['surname'], credit_card=data['credit_card'],
                            car_number=data['car_number'])
        db.session.add(new_client)
        db.session.commit()
        return new_client.to_json()

    @classmethod
    def check_credit_card(cls, id):
        try:
            client = db.session.query(Client).filter_by(id=id).first()
            if not client.credit_card == None:
                return True
            else:
                return "Вы не привязали кредитную карту. Привяжите и попробуйте снова", 400
        except AttributeError:
            return 'Данного клиента не существует, проверьте id клиента и повторите попытку', 400



class Parking(db.Model):
    __tablename__ = 'parking'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean, default=True)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Парковка №: {self.id}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}

    @classmethod
    def create_parking_place(cls, data):
        new_parking_place = Parking(address=data['address'], opened=data['opened'], count_places=data['count_places'],
                            count_available_places=data['count_available_places'])
        db.session.add(new_parking_place)
        db.session.commit()
        return new_parking_place.to_json()

    @classmethod
    def take_parking_space(cls, id):
        parking = db.session.query(Parking).filter_by(id=id).first()
        parking.count_available_places -= 1
        db.session.commit()

    @classmethod
    def free_up_parking_space(cls, id):
        parking = db.session.query(Parking).filter_by(id=id).first()
        parking.count_available_places += 1
        db.session.commit()

    @classmethod
    def check_valid_number_parking(cls, id):
        record_parking_for_check = db.session.query(Parking).filter_by(id=id).first()
        if not record_parking_for_check == None:
            return True
        else:
            accessible_parking_raw = db.session.execute(text('SELECT id FROM parking')).fetchall()
            accessible_parking = ', '.join(str(num[0]) for num in accessible_parking_raw)
            return f"""Вы пытаетесь заехать на несуществующую парковку.
             Введите номер существующей парковки: {accessible_parking}""", 400

    @classmethod
    def check_free_space_and_opened_parking(cls, id):
        record_parking_for_check = db.session.query(Parking).filter_by(id=id).first()
        check_valid_number_parking = cls.check_valid_number_parking(id)
        if check_valid_number_parking == True: # проверка на существование данной парковки
            opened_status = record_parking_for_check.opened
            count_free_spaces = record_parking_for_check.count_available_places
            if opened_status == True and count_free_spaces >= 1:
                return True
            else:
                return 'Парковка закрыта, либо нет свободных мест', 400
        else:
            return check_valid_number_parking



class Client_Parking(db.Model):
    __tablename__ = 'client_parking'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id', ondelete='CASCADE'))
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id', ondelete='CASCADE'))
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)

    __table_args__ = (
        db.UniqueConstraint('parking_id', 'client_id', name='unique_client_parking'),
    )

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}

    @classmethod
    def client_in_parking(cls, data):
        parking_entry_time = datetime.datetime.now()
        new_record = Client_Parking(client_id=data['client_id'], parking_id=data['parking_id'],
                                    time_in=parking_entry_time, time_out=None)

        db.session.add(new_record)
        db.session.commit()
        return new_record.to_json()


    @classmethod
    def client_out_parking(cls, data):
        parking_out_time = datetime.datetime.now()
        try:
            client_parking_record = db.session.query(Client_Parking).filter_by(client_id=data['client_id'],
                                                                            parking_id=data['parking_id']).first()
            if parking_out_time > client_parking_record.time_in:
                client_parking_record.time_out = parking_out_time
                db.session.commit()
                refresh_data = db.session.query(Client_Parking).filter_by(client_id=data['client_id'],
                                                                          parking_id=data['parking_id']).first()
                return refresh_data.to_json(), 200
            else:
                return 'Ошибка в логике установки времени въезда/выезда с парковки', 400

        except AttributeError:
            return 'Ошибка ввода данных, проверьте входные данные и повторите попытку', 400


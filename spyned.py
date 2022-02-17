import json

from spyne import Application, rpc, Service, Integer, Iterable, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class VehicleList:
    def __init__(self):
        self.v_list = []


class Vehicle:
    def __init__(self, model, brand, autonomy, refill):
        self.model = model
        self.brand = brand
        self.autonomy = autonomy
        self.refill = refill


def init_list_vehicles():
    v_list = []

    with open('vehicles.json', 'r') as f:
        vehicles = json.load(f)

    for car in vehicles:
        car_info = str(vehicles[car]["brand"]) + ";" + str(vehicles[car]["model"]) + ";" + str(vehicles[car]["autonomy"]) + ";" + str(vehicles[car]["refill"])
        v_list.append(car_info)

    return v_list


def get_names_vehicles(v_list):
    n_list = []

    for vehicle in v_list:
        info = vehicle.split(";")
        name = info[0] + " " + info[1]
        n_list.append(name)

    return n_list


class ServiceVehicles(Service):
    list_vehicles = init_list_vehicles()

    @rpc(_returns=Iterable(Unicode))
    def get_vehicles_info(self):
        for info in ServiceVehicles.list_vehicles:
            yield u'%s' % info

    @rpc(_returns=Iterable(Unicode))
    def get_vehicles_names(self):
        n_list = get_names_vehicles(ServiceVehicles.list_vehicles)
        for info in n_list:
            yield u'%s' % info



application = Application(
    services=[ServiceVehicles],
    tns='spyne.electric.vehicles',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11())

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()

import json

from spyne import Application, rpc, Service, Iterable, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from serviceVehicles import VehicleList, Vehicle


def init_list_vehicles():
    v_list = VehicleList()

    with open('vehicles.json', 'r') as f:
        vehicles = json.load(f)

    for car in vehicles:
        v_list.add_vehicle(Vehicle(car, vehicles[car]["model"], vehicles[car]["brand"], vehicles[car]["autonomy"],
                                   vehicles[car]["refill"]))

    return v_list


class ServiceVehicles(Service):
    list_vehicles = init_list_vehicles()

    # envoie la liste des véhicules et leurs informations
    @rpc(_returns=Iterable(Unicode))
    def get_vehicles(self):
        v_list = ServiceVehicles.list_vehicles.get_all()
        for car in v_list:
            info = car.convert_to_string()
            yield u'%s' % info

    # envoie la liste des noms des véhicules
    @rpc(_returns=Iterable(Unicode))
    def get_vehicles_names(self):
        n_list = ServiceVehicles.list_vehicles.get_all()
        for car in n_list:
            name = car.get_name()
            yield u'%s' % str(name)

    # envoie les informations d'un véhicule, identifié par son nom
    @rpc(Unicode, _returns=Unicode)
    def get_vehicle_info(self, name):
        res = Vehicle("", "", "", "", "")
        v_list = ServiceVehicles.list_vehicles.get_all()

        for car in v_list:
            if car.get_name() == name:
                res = car
                break

        if res.get_name() != "":
            return u'%s' % res.convert_to_string()
        else:
            return u''


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

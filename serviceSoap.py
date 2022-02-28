import json
import logging
import os
from wsgiref.simple_server import make_server

# from spyne import Application, rpc, Service, Iterable, Unicode
# from spyne.protocol.soap import Soap11
# from spyne.server.wsgi import WsgiApplication

from rpclib.application import Application
from rpclib.decorator import srpc
from rpclib.protocol.soap import Soap11
from rpclib.service import ServiceBase
from rpclib.model.complex import Iterable
from rpclib.model.primitive import Integer
from rpclib.model.primitive import String
from rpclib.server.wsgi import WsgiApplication

from serviceVehicles import VehicleList, Vehicle


def init_list_vehicles():
    v_list = VehicleList()

    with open('vehicles.json', 'r') as f:
        vehicles = json.load(f)

    for car in vehicles:
        v_list.add_vehicle(Vehicle(car, vehicles[car]["model"], vehicles[car]["brand"], vehicles[car]["autonomy"],
                                   vehicles[car]["refill"]))

    return v_list


class ServiceVehicles(ServiceBase):
    list_vehicles = init_list_vehicles()

    # envoie la liste des véhicules et leurs informations
    @srpc(_returns=Iterable(String))
    def get_vehicles():
        v_list = ServiceVehicles.list_vehicles.get_all()
        for car in v_list:
            info = car.convert_to_string()
            yield u'%s' % info

    # envoie la liste des noms des véhicules
    @srpc(_returns=Iterable(String))
    def get_vehicles_names():
        n_list = ServiceVehicles.list_vehicles.get_all()
        for car in n_list:
            name = car.get_name()
            yield u'%s' % str(name)

    # envoie les informations d'un véhicule, identifié par son nom
    @srpc(String, _returns=String)
    def get_vehicle_info(name):
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


# application = Application(
#     services=[ServiceVehicles],
#     tns='spyne.electric.vehicles',
#     in_protocol=Soap11(validator='lxml'),
#     out_protocol=Soap11())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    # Config test
    # url = '127.0.0.1'
    # port = 8000

    # Config server
    # url = '127.0.0.1'
    url = '0.0.0.0'
    port = int(os.environ.get('PORT', 35000))


    logging.info(f"listening to http://{url}:{port}")
    logging.info(f"wsdl is at: http://{url}:{port}/?wsdl")

    app = Application([ServiceVehicles], 'spyne.examples.vehicle.http',
                      in_protocol=Soap11(validator='lxml'),
                      out_protocol=Soap11(),
                      )
    wsgi_application = WsgiApplication(app)
    server = make_server(url, port, wsgi_application)
    server.serve_forever()

import json

from lxml.builder import unicode
from spyne import Application, Unicode, rpc, Service, AnyDict
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


def init_list_vehicles():
    v_dict = {}

    with open('vehicles.json', 'r') as f:
        vehicles = json.load(f)

    for car in vehicles:
        car_info = {"model": vehicles[car]["model"],
                "brand": vehicles[car]["brand"],
                "autonomy": vehicles[car]["autonomy"],
                "refill": vehicles[car]["refill"]}
        v_dict[car] = car_info
        # v_dict.append(car)

    return v_dict


class ServiceVehicles(Service):

    # @brief : Return all vehicle of the list
    # @return : list of dictionary
    @rpc(_returns=AnyDict)
    def get_vehicles(self):
        list_vehicles = init_list_vehicles()
        return list_vehicles

    # @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    # def say_hello(self, name, times):
    #     for i in range(times):
    #         yield u'Hello, %s' % name
    #
    # @rpc(Integer, Integer, _returns=Integer)
    # def addition(self, a, b):
    #     return a + b


if __name__ == '__main__':
    application = Application(
        services=[ServiceVehicles],
        tns='http://tests.python-zeep.org/',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11())

    application = WsgiApplication(application)

    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    server = make_server('127.0.0.1', 8000, application)
    server.serve_forever()

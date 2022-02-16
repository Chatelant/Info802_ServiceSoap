from spyne import ServiceBase, rpc, Unicode, Integer, Iterable, Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import os

import json

from wsgiref.simple_server import make_server


# liste de véhicules
class VehicleList:
    def __init__(self):
        self.data = []

    def add_vehicle(self, vehicle):
        self.data.append(vehicle)

    def del_vehicle(self, vehicle):
        self.data.remove(vehicle)

    def get_vehicle(self, index):
        return self.data[index]

    # @brief : return all vehicle of the input "brand"
    def get_vehicle_brand(self, brand):
        res = []
        for vehicle in self.data:
            if vehicle.brand == brand:
                res.append(vehicle)
        return res


# véhicule
class Vehicle:
    def __init__(self, model, brand, autonomy, refill):
        self.model = model
        self.brand = brand
        self.autonomy = autonomy  # en km
        self.refill = refill  # en min

    def get_model(self):
        return self.model

    def get_brand(self):
        return self.brand

    def get_autonomy(self):
        return self.autonomy

    def get_refill(self):
        return self.refill


# Développez et déployez un service SOAP qui propose une liste de véhicules avec ses
# caractéristiques (autonomie, temps de chargement)
# class ServiceVehicles(ServiceBase):
#     # @rpc(VehicleList, _return=Unicode)
#     # def display_vehicles(self, list_vehicles):
#     #     for vehicle in list_vehicles:
#     #         print(vehicle.brand, vehicle.model, vehicle.battery)
#
#     @rpc(Unicode, Integer, _returns=Iterable(Unicode))
#     def say_hello(self, name, times):
#         for i in range(times):
#             yield u'Hello, %s' % name
#
#     @rpc(Integer, Integer, _returns=Integer)
#     def addition(self, a, b):
#         return a + b
#
#
# application = Application([ServiceVehicles], 'spyne.examples.hello.soap',
#                           in_protocol=Soap11(validator='lxml'),
#                           out_protocol=Soap11())
# wsgi_app = WsgiApplication(application)


# def init_list_vehicles():
#     list = VehicleList()
#
#     with open('vehicles.json', 'r') as f:
#         vehicles = json.load(f)
#
#     for car in vehicles:
#         list.add_vehicle(Vehicle(vehicles[car]["model"],
#                                  vehicles[car]["brand"],
#                                  vehicles[car]["autonomy"],
#                                  vehicles[car]["refill"]))
#
#     return list


# if __name__ == '__main__':
#     os.environ.get("PORT", 35000)
#     server = make_server('0.0.0.0', 35000, wsgi_app)
#     server.serve_forever()

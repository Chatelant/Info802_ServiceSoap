import json

from spyne import Iterable, Integer, Unicode, rpc, Application, Service
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument

from serviceVehicles import Vehicle, VehicleList


def init_list_vehicles():
    list = VehicleList()

    with open('vehicles.json', 'r') as f:
        vehicles = json.load(f)

    for car in vehicles:
        list.add_vehicle(Vehicle(vehicles[car]["model"],
                                 vehicles[car]["brand"],
                                 vehicles[car]["autonomy"],
                                 vehicles[car]["refill"]))
    print(list)
    return list


list_vehicles = init_list_vehicles()


class ServiceVehicles(Service):
    # @brief : Return all vehicle of the list
    # @return : list of dictionary
    @rpc(_returns=Unicode)
    def display_vehicles(self):
        data = list_vehicles.get_all()
        for vehicle in data:
            yield vehicle.get_dict()

    # @brief : Return the vehicle if the model is found
    # @return : list of dictionary
    @rpc(Unicode, _returns=Unicode)
    def get_vehicle_bymodel(self, model):
        yield list_vehicles.find_bymodel(model)

    # @brief : Return all vehicle of the input brand
    # @return : list of dictionary
    @rpc(Unicode, _returns=Unicode)
    def get_vehicle_bybrand(self, brand):
        return list_vehicles.find_bybrand(brand)

    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(self, name, times):
        for i in range(times):
            yield u'Hello, %s' % name

    @rpc(Integer, Integer, _returns=Integer)
    def addition(self, a, b):
        return a + b


class UserDefinedContext(object):
    def __init__(self, flask_config):
        self.config = flask_config


def create_app(flask_app):
    """Creates SOAP services application and distribute Flask config into
    user con defined context for each method call.
    """
    application = Application(
        [ServiceVehicles], 'ServiceVehicles',
        # The input protocol is set as HttpRpc to make our service easy to call.
        in_protocol=HttpRpc(validator='soft'),
        out_protocol=JsonDocument(ignore_wrappers=True),
    )

    # Use `method_call` hook to pass flask config to each service method
    # context. But if you have any better ideas do it, make a pull request.
    # NOTE. I refuse idea to wrap each call into Flask application context
    # because in fact we inside Spyne app context, not the Flask one.
    def _flask_config_context(ctx):
        ctx.udc = UserDefinedContext(flask_app.config)

    application.event_manager.add_listener('method_call', _flask_config_context)

    return application

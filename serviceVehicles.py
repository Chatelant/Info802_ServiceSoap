# CLASSE VEHICLELIST : Une liste de véhicules
class VehicleList:
    # initialisations de la liste
    def __init__(self):
        self.data = []

    # ajoute un véhicule de la liste
    def add_vehicle(self, vehicle):
        self.data.append(vehicle)

    # supprime un véhicule de la liste
    def del_vehicle(self, vehicle):
        self.data.remove(vehicle)

    # retourne un véhicule de la liste
    def get_vehicle(self, index):
        return self.data[index]

    # retourne la liste des véhicules
    def get_all(self):
        return self.data

    # retourne les véhicules d'un modèle précis
    def find_bymodel(self, model):
        for vehicle in self.data:
            if vehicle.model == model:
                return vehicle.get_dict()

    # retourne les véhicules d'une marque précise
    def find_bybrand(self, brand):
        for vehicle in self.data:
            if vehicle.brand == brand:
                yield vehicle.get_dict()

    # retourne les marques d'un véhicule
    def get_vehicle_brand(self, brand):
        res = []
        for vehicle in self.data:
            if vehicle.brand == brand:
                res.append(vehicle)
        return res


# CLASSE VEHICULE : Un véhicule et ses informations
class Vehicle:
    # initialise le véhicule
    def __init__(self, name, model, brand, autonomy, refill):
        self.name = name
        self.model = model
        self.brand = brand
        self.autonomy = autonomy  # en km
        self.refill = refill  # en min

    # retourne le nom du véhicule
    def get_name(self):
        return self.name

    # retourne le modèle du véhicule
    def get_model(self):
        return self.model

    # retourne la marque du véhicule
    def get_brand(self):
        return self.brand

    # retourne l'autonomie du véhicule
    def get_autonomy(self):
        return self.autonomy

    # retourne la recharge du véhicule
    def get_refill(self):
        return self.refill

    # retourne le véhicule sous forme de chaîne de caractères
    def convert_to_string(self):
        car_info = str(self.brand) + ";" + str(self.model) + ";" + str(self.autonomy) + ";" + str(self.refill)
        return car_info

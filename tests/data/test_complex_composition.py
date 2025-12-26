class Engine:
    def __init__(self, horsepower, fuel_type):
        self.horsepower = horsepower
        self.fuel_type = fuel_type

    def start(self):
        return f"Engine with {self.horsepower}HP started"

class Transmission:
    def __init__(self, gears):
        self.gears = gears
        self.current_gear = 1

    def shift_up(self):
        if self.current_gear < self.gears:
            self.current_gear += 1
            return f"Shifted to gear {self.current_gear}"

    def shift_down(self):
        if self.current_gear > 1:
            self.current_gear -= 1
            return f"Shifted to gear {self.current_gear}"

class Wheels:
    def __init__(self, size, tire_pressure):
        self.size = size
        self.tire_pressure = tire_pressure

    def rotate(self):
        return f"Wheels of size {self.size} rotating"

class Car:
    def __init__(self, model, engine_hp, transmission_gears, wheel_size):
        self.model = model
        self.engine = Engine(engine_hp, "Petrol")
        self.transmission = Transmission(transmission_gears)
        self.wheels = Wheels(wheel_size, 32)
        self.fuel = 100

    def drive(self):
        engine_status = self.engine.start()
        wheel_status = self.wheels.rotate()
        return f"{self.model}: {engine_status}, {wheel_status}"

    def refuel(self, amount):
        self.fuel += amount
        return f"Fuel level: {self.fuel}%"

class Garage:
    def __init__(self):
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)
        return f"Added {car.model} to garage"

    def get_car(self, model):
        for car in self.cars:
            if car.model == model:
                return car
        return None

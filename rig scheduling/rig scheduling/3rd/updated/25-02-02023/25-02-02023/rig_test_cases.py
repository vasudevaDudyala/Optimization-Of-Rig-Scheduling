import random
class Rig:
    def __init__(self, id, name, type, power_rating, depth_rating, max_load, price, status):
        self.id = id
        self.name = name
        self.type = type
        self.power_rating = power_rating
        self.depth_rating = depth_rating
        self.max_load = max_load
        self.price = price
        self.status = status

    def __str__(self):
        status_str = ', '.join([f"{k}={v}" for k, v in self.status.items()])
        return f"Rig({self.id}, {self.name}, {self.type}, {self.power_rating}, {self.depth_rating}, {self.max_load}, {self.price}, {{{status_str}}})"

num_rigs = int(input())
rigs = []

for i in range(num_rigs):
    id = str(i + 1)
    name = f"Rig{id}"
    type = "Drilling"
    power_rating = random.randint(1500, 2500)
    depth_rating = random.randint(1000, 2000)
    max_load = random.randint(5, 15)
    price = random.randint(10000, 30000)
    status = {'rig_location': f'({random.randint(100, 999)} , {random.randint(100, 999)})',
              'rig_maintance': random.randint(1, 5),
              'rig_init_status': random.choice(['mastUp', 'mastDown'])}
    rig = Rig(id, name, type, power_rating, depth_rating, max_load, price, status)
    rigs.append(rig)

for rig in rigs:
    print(rig)

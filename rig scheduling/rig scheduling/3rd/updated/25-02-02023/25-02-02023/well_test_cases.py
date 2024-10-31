import random

class Well:
    def __init__(self, id, name, type, depth, status):
        self.id = id
        self.name = name
        self.type = type
        self.depth = depth
        self.status = status

    def __str__(self):
        status_str = ', '.join([f"'{k}': '{v}'" for k, v in self.status.items()])
        return f"('{self.id}', '{self.name}', '{self.type}', {self.depth}, {{{status_str}}})"

num_wells = int(input())  # number of wells to generate

for i in range(num_wells):
    id = str(i)
    name = f"well{i+1}"
    type = "Drilling"
    depth = random.randint(1000, 5000)
    status = {
        'startTime': f'{random.randint(1, 28)}-02-2023',
        'endTime': f'{random.randint(1, 28)}-03-2023',
        'workoverTime': random.randint(1, 5),
        'priority': random.randint(1, 5),
        'well_location': f"({random.randint(100, 999)} , {random.randint(100, 999)})",
        'lossFactor': round(random.uniform(0, 0.5), 2)
    }
    well = Well(id, name, type, depth, status)
    print('well =',well)

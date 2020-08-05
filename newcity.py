import random
import math

RADIUS_INCREASE = 10.0
NEW_SITE_DENSITY = 0.0002
AUXIN_BIRTH_THRESHOLD = 2.0
VEIN_BIRTH_THRESHOLD = 2.0
VEIN_DEATH_THRESHOLD = 1.0
NODE_DISTANCE = 1.0
 
CENTRE_X = 400
CENTRE_Y = 400
SCALE = 15
ITERATIONS = 20


class Leaf:
    auxin_sites = {}
    vein_sites = {}
    used_vein_ids = 1
    used_auxin_ids = 0
    radius = 10.0

    def new_auxin_id(self):
        auxin_id = self.used_auxin_ids
        self.used_auxin_ids += 1
        return auxin_id

    def new_vein_id(self):
        vein_id = self.used_vein_ids
        self.used_vein_ids += 1
        return vein_id
    
    def __init__(self):
        start_id = self.new_vein_id()
        self.vein_sites[start_id] = {'id': start_id, 'coords': (0, 0), 'root': [], 'tags': []}

    def iteration(self):
        self.modify_shape()
        self.generate_new_auxin()
        new_veins = self.generate_new_vein()
        self.kill_veins(new_veins)

    def modify_shape(self):
        self.radius += RADIUS_INCREASE

    def pick_site(self):
        # hell yeah
        # pick a random magnitude
        r = random.random * self.radius
        # pick a random angle
        theta = random.random() * 2 * math.pi - math.pi
        x = math.sqrt(r) * math.cos(theta)
        y = math.sqrt(r) * math.sin(theta)
        return (x, y)

    def new_sites(self):
        # number of new sites we want, as a function of area
        return int(NEW_SITE_DENSITY * math.pi * (self.radius**2))

    def generate_new_auxin(self):
        # generate new auxin nodes
        for i in range(self.new_sites()):
            site = self.pick_site()
            # rule out sites that are too close
            failed = False
            for auxin_id in self.auxin_sites:
                auxin = self.auxin_sites[auxin_id]
                dx = site[0] - auxin['coords'][0]
                dy = site[1] - auxin['coords'][1]
                if math.sqrt(dx**2 + dy**2) < AUXIN_BIRTH_THRESHOLD:
                    failed = True
                    break
            if failed:
                continue
        # If we didn't fail, make a new site.
        new_id = self.new_auxin_id()
        self.auxin_sites[new_id] = {'id': new_id, 'coords': site, 'tag': False, 'linked': []}

    def generate_new_vein(self):
        # creates a new vein. yup.
        new_veins = {}



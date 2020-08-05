from tkinter import *
import random
import math
 
RADIUS_INCREASE = 15.0
NEW_SITE_DENSITY = 0.0003
AUXIN_BIRTH_THRESHOLD = 2.0
VEIN_BIRTH_THRESHOLD = 2.0
VEIN_DEATH_THRESHOLD = 1.0
NODE_DISTANCE = 1.0
 
CENTRE_X = 800
CENTRE_Y = 300
SCALE = 25
ITERATIONS = 20
 
class Leaf:
    # DATA
    auxin_sites = {}
    vein_sites = {}
    used_vein_ids = 1
    used_auxin_ids = 0
    radius = 10.0
 
    # UTILITY FUNCTIONS
    def new_auxin_id(self):
        auxin_id = self.used_auxin_ids
        self.used_auxin_ids += 1
        return auxin_id
 
    def new_vein_id(self):
        vein_id = self.used_vein_ids
        self.used_vein_ids += 1
        return vein_id
 
    # MAIN FUNCTIONS
    def __init__(self):
        start_id = self.new_vein_id()
        self.vein_sites[start_id] = {'ID': start_id, 'CO-ORDS': (0, 0), 'ROOT': [], 'TAGS': []}
 
    def iteration(self):
        self.modify_shape()
        self.generate_new_auxin()
        new_veins = self.generate_new_vein()
        self.kill_veins(new_veins)
 
    # SECONDARY FUNCTIONS
    def modify_shape(self):
        self.radius += RADIUS_INCREASE
 
    def pick_site(self):
        r = random.random() * self.radius
        theta = random.random() * 2 * math.pi - math.pi
        x = math.sqrt(r) * math.cos(theta)
        y = math.sqrt(r) * math.sin(theta)
        return (x, y)
 
    def new_sites(self):
        return int(NEW_SITE_DENSITY * math.pi * (self.radius**2))
 
    def generate_new_auxin(self):
        # Generate new auxin nodes
        for i in range(self.new_sites()):
            site = self.pick_site()
            # Test each auxin node to see if we are too close
            failed = False
            for auxin_id in self.auxin_sites:
                auxin = self.auxin_sites[auxin_id]
                dx = site[0] - auxin['CO-ORDS'][0]
                dy = site[1] - auxin['CO-ORDS'][1]
                if math.sqrt(dx**2 + dy**2) < AUXIN_BIRTH_THRESHOLD:
                    failed = True
                    break
            if failed:
                continue
            # Test each vein node to see if we are too close
            for vein_id in self.vein_sites:
                vein = self.vein_sites[vein_id]
                dx = site[0] - vein['CO-ORDS'][0]
                dy = site[1] - vein['CO-ORDS'][1]
                if math.sqrt(dx**2 + dy**2) < VEIN_BIRTH_THRESHOLD:
                    failed = True
                    break
            if failed:
                continue
            # Create new auxin site
            new_id = self.new_auxin_id()
            self.auxin_sites[new_id] = {'ID': new_id, 'CO-ORDS': site, 'TAG': False, 'LINKED': []}
 
    def generate_new_vein(self):
        # Create new veins
        new_veins = {}
        for vein_id in self.vein_sites:
            vein = self.vein_sites[vein_id]
            # Identify close auxin nodes
            linked_auxin = []
            for auxin_id in self.auxin_sites:
                auxin = self.auxin_sites[auxin_id]
                # Only allow tagged veins to grow towards dead auxin
                if auxin['TAG'] and auxin_id not in vein['TAGS']:
                    continue
                # Check to see if there are any closer veins
                dx = auxin['CO-ORDS'][0] - vein['CO-ORDS'][0]
                dy = auxin['CO-ORDS'][1] - vein['CO-ORDS'][1]
                distance_squared = dx**2 + dy**2
                for test_vein_id in self.vein_sites:
                    if test_vein_id is vein_id:
                        continue
                    test_vein = self.vein_sites[test_vein_id]
                    d1x = auxin['CO-ORDS'][0] - test_vein['CO-ORDS'][0]
                    d1y = auxin['CO-ORDS'][1] - test_vein['CO-ORDS'][1]
                    distance1_squared = d1x**2 + d1y**2
                    d2x = vein['CO-ORDS'][0] - test_vein['CO-ORDS'][0]
                    d2y = vein['CO-ORDS'][1] - test_vein['CO-ORDS'][1]
                    distance2_squared = d2x**2 + d2y**2
                    if distance1_squared < distance_squared and distance2_squared < distance_squared:
                        break
                else:
                    linked_auxin.append(auxin_id)
                    auxin['LINKED'].append(vein_id)
            # Tag cleanup
            self.vein_sites[vein_id]['TAGS'] = [tag for tag in vein['TAGS'] if tag in linked_auxin]
            # Calculate the new co-ords
            if not linked_auxin:
                continue
            sum_x = 0
            sum_y = 0
            for auxin_id in linked_auxin:
                auxin = self.auxin_sites[auxin_id]
                dx = auxin['CO-ORDS'][0] - vein['CO-ORDS'][0]
                dy = auxin['CO-ORDS'][1] - vein['CO-ORDS'][1]
                scale = NODE_DISTANCE / math.sqrt(dx**2 + dy**2)
                sum_x += dx * scale
                sum_y += dy * scale
            total = len(linked_auxin)
            new_coords = (sum_x / total + vein['CO-ORDS'][0], sum_y / total + vein['CO-ORDS'][1])
            # Create the new vein node
            new_id = self.new_vein_id()
            new_veins[new_id] = {'ID': new_id, 'CO-ORDS': new_coords, 'ROOT': [vein_id], 'TAGS': vein['TAGS']}
            self.vein_sites[vein_id]['TAGS'] = []
        self.vein_sites.update(new_veins)
        return new_veins.keys()
 
    def kill_veins(self, new_veins):
        for auxin_id in self.auxin_sites:
            auxin = self.auxin_sites[auxin_id]
            # Find overly close auxin nodes
            if not auxin['TAG']:
                for vein_id in self.vein_sites:
                    vein = self.vein_sites[vein_id]
                    dx = auxin['CO-ORDS'][0] - vein['CO-ORDS'][0]
                    dy = auxin['CO-ORDS'][1] - vein['CO-ORDS'][1]
                    if math.sqrt(dx**2 + dy**2) < VEIN_DEATH_THRESHOLD:
                        # Kill the node
                        new_id = self.new_vein_id()
                        self.vein_sites[new_id] = {'ID': new_id, 'CO-ORDS': auxin['CO-ORDS'], 'ROOT': [], 'TAGS': []}
                        auxin['VEIN'] = new_id
                        auxin['TAG'] = True
                        affected_veins = filter(lambda ID: ID in auxin['LINKED'], self.vein_sites)
                        for new_vein_id in new_veins:
                            new_vein = self.vein_sites[new_vein_id]
                            if len(set(affected_veins) & set(new_vein['ROOT'])) > 0:
                                new_vein['TAGS'].append(auxin_id)
                        break
            # Process dead auxin nodes
            if auxin['TAG']:
                for vein_id in self.vein_sites:
                    vein = self.vein_sites[vein_id]
                    if auxin_id not in vein['TAGS']:
                        continue
                    dx = auxin['CO-ORDS'][0] - vein['CO-ORDS'][0]
                    dy = auxin['CO-ORDS'][1] - vein['CO-ORDS'][1]
                    if math.sqrt(dx**2 + dy**2) < VEIN_DEATH_THRESHOLD:
                        vein['TAGS'].remove(auxin_id)
                        self.vein_sites[auxin['VEIN']]['ROOT'].append(vein_id)
                        self.vein_sites[auxin['VEIN']]['TAGS'].extend(vein['TAGS'])
                        vein['TAGS'] = []
            # Clear for next cycle
            auxin['LINKED'] = []
 
# Create the city
leaf = Leaf()
for i in range(ITERATIONS):
    leaf.iteration()
 
# Create the window
window = Tk()
canvas = Canvas(window, width=1600, height=600)
canvas.pack()
 
# Draw the city
for vein_id in leaf.vein_sites:
    coords = leaf.vein_sites[vein_id]['CO-ORDS']
    x = CENTRE_X + int(coords[0] * SCALE)
    y = CENTRE_Y + int(coords[1] * SCALE)
    for root_id in leaf.vein_sites[vein_id]['ROOT']:
        root_coords = leaf.vein_sites[root_id]['CO-ORDS']
        root_x = CENTRE_X + int(root_coords[0] * SCALE)
        root_y = CENTRE_Y + int(root_coords[1] * SCALE)
        canvas.create_line(root_x, root_y, x, y, fill='red')
 
# Display
mainloop()


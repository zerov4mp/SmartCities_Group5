class Location():
    def __init__(self, building, floor, room, coords=None):
        self.building = building
        self.floor = floor
        self.room = room
        # coords stores real world coordinates (maybe needed for visualization of building)
        self.coords = coords

    def toString(self):
        return self.building + "." + self.floor + "." + self.room

class Therapist:

    def __init__(self, thId, name):
        self.id = thId
        self.name = name
        self.timeSlots = []
        self.assignedRooms = {}
        self.unassignedTimeSlots = []

    def addTimeSlots(self, timeSlots):
        for slot in timeSlots:
            if self.timeSlots.count(slot) == 0:
                self.timeSlots.append(slot)
                self.assignedRooms[slot] = -1

    def removeTimeSlots(self, timeSlots):
        for slot in timeSlots:
            if self.timeSlots.count(slot) != 0:
                self.timeSlots.remove(slot)
                self.assignedRooms.pop(slot)

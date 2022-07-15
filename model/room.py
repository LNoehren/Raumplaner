import utils


class Room:

    def __init__(self, roomId, openingTime, closingTime, timeSlotSize):
        self.id = roomId
        self.openingTime = openingTime
        self.closingTime = closingTime
        self.timSlotSize = timeSlotSize
        self.occupation = [-1] * int(((closingTime - openingTime) / timeSlotSize))

    def computeOccupationIndexFromTime(self, time):
        return int((time - self.openingTime)/self.timSlotSize)

    def computeTimeFromOccupationIndex(self, index):
        return self.openingTime + index * self.timSlotSize

    def getOccupation(self, time):
        if time < self.openingTime or time > self.closingTime:
            return -2

        timeSlot = self.computeOccupationIndexFromTime(time)
        if timeSlot >= len(self.occupation):
            return -2

        return self.occupation[timeSlot]

    def isOccupied(self, time):
        return self.getOccupation(time) >= 0

    def addOccupationRange(self, thId, start, end):
        if start < self.openingTime or start > self.closingTime\
                or end < self.openingTime or end > self.closingTime:
            return

        adaptedStart = self.computeOccupationIndexFromTime(start)
        adaptedEnd = self.computeOccupationIndexFromTime(end)

        for i in range(adaptedStart, adaptedEnd):
            if self.occupation[i] != -1:
                print(f"Trying to add therapist {thId} into room {self.id} when it is already occupied "
                      f"(between {utils.timeToTimeString(start)} and {utils.timeToTimeString(end)})")
                return

        for i in range(adaptedStart, adaptedEnd):
            self.occupation[i] = thId

    def addOccupation(self, thId, timeSlot):
        if timeSlot < self.openingTime or timeSlot > self.closingTime:
            return

        adaptedTimeSlot = self.computeOccupationIndexFromTime(timeSlot)

        if self.occupation[adaptedTimeSlot] != -1:
            print(f"Trying to add therapist {thId} into room {self.id} when it is already occupied "
                  f"(at {utils.timeToTimeString(timeSlot)})")
        else:
            self.occupation[adaptedTimeSlot] = thId

    def removeOccupation(self, timeSlot):
        if timeSlot < self.openingTime or timeSlot > self.closingTime:
            return

        adaptedTimeSlot = self.computeOccupationIndexFromTime(timeSlot)

        if self.occupation[adaptedTimeSlot] == -1:
            print(f"Trying to remove therapist from room {self.id} when it is not occupied "
                  f"(at {utils.timeToTimeString(timeSlot)})")
        else:
            self.occupation[adaptedTimeSlot] = -1

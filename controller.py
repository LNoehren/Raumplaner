import model.room
import model.therapist
import utils
import view.mainWindow


class Controller:

    def __init__(self, config, ui):
        self.config = config
        self.rooms = {}
        self.therapists = {}
        self.lastUsedThId = -1
        self.ui = ui

        for openingDay in config.openingTime:
            roomList = []
            for i in range(config.numberOfRooms):
                openingTime = utils.timeStringToTime(config.openingTime[openingDay])
                closingTime = utils.timeStringToTime(config.closingTime[openingDay])
                roomList.append(model.room.Room(i+1, openingTime, closingTime, config.minimalTimeSlot))

            ui.addWeekday(openingDay, roomList, self.createTherapist)

            self.rooms[openingDay] = roomList

    def createTherapist(self, weekday, name):
        """
        Creates a new therapist
        :param weekday: The weekday on which the therapist ist active
        :param name: The name of the therapist to be created
        :return: A lmbda function that can be used to set the time slots of the created therapist. The function has
        a list of time slots as input parameter
        """
        print(f"Adding therapist {name} on {weekday}")

        self.lastUsedThId += 1
        newTherapist = model.therapist.Therapist(self.lastUsedThId, name)
        self.therapists[self.lastUsedThId] = newTherapist

        return lambda timeSlots, setActive: self.setTherapistTimes(weekday, newTherapist.id, timeSlots, setActive)

    def setTherapistTimes(self, weekday, therapistId, timeSlots, setActive):
        therapist = self.therapists[therapistId]
        if setActive:
            therapist.addTimeSlots(timeSlots)
            print(f"Adding time slots {timeSlots} for therapist {therapist.name}")
        else:
            therapist.removeTimeSlots(timeSlots)
            print(f"Removing time slots {timeSlots} for therapist {therapist.name}")

        self.distributeTherapistsToRooms(weekday)

    def distributeTherapistsToRooms(self, weekday):
        # first clear all rooms from therapist that have no longer a time slot there
        for room in self.rooms[weekday]:
            for i in range(len(room.occupation)):
                if room.occupation[i] != -1:
                    # check if the therapist still has that time slot
                    therapist = self.therapists[room.occupation[i]]
                    if therapist.timeSlots.count(i) == 0:
                        room.occupation[i] = -1
                        self.ui.setRoomOccupation(weekday, room.id, i, False)

        # now insert all unassigned therapist time slots into rooms
        for therapist in self.therapists.values():
            remainingTimeWindows = therapist.timeSlots.copy()
            for timeSlot in therapist.timeSlots:
                if therapist.assignedRooms[timeSlot] == -1:
                    for room in self.rooms[weekday]:
                        time = room.computeTimeFromOccupationIndex(timeSlot)
                        if not room.isOccupied(time):
                            room.addOccupation(therapist.id, time)
                            therapist.assignedRooms[timeSlot] = room.id
                            self.ui.setRoomOccupation(weekday, room.id, timeSlot, True)

                            remainingTimeWindows.remove(timeSlot)
                            break
                else:
                    remainingTimeWindows.remove(timeSlot)

            # check if any previously unassigned time slots are assigned now
            for unassignedTimeSlot in therapist.unassignedTimeSlots:
                if unassignedTimeSlot in therapist.assignedRooms and therapist.assignedRooms[unassignedTimeSlot] != -1:
                    self.ui.setTherapistAssignment(weekday, therapist.name, [unassignedTimeSlot], True)

            # in case not all time slots were assigned we need to mark that in the UI
            if len(remainingTimeWindows) != 0:
                print(f"Could not fit therapist {therapist.name} into the available rooms. Remaining slots: {remainingTimeWindows}")
                self.ui.setTherapistAssignment(weekday, therapist.name, remainingTimeWindows, False)
                therapist.unassignedTimeSlots = remainingTimeWindows

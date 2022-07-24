import model.room
import model.therapist
import model.saveContainer
import utils
import pickle


class Controller:

    VERSION_NUMBER = "0.3"

    def __init__(self, config, ui):
        self.config = config
        self.rooms = {}
        self.therapists = {}
        self.lastUsedThId = -1
        self.ui = ui
        self.ui.saveCallback = self.saveState
        self.ui.loadCallback = self.loadState

        self.initializeFromConfig()

    def initializeFromConfig(self):
        for openingDay in self.config.openingTime:
            roomList = []
            for i in range(self.config.numberOfRooms):
                openingTime = utils.timeStringToTime(self.config.openingTime[openingDay])
                closingTime = utils.timeStringToTime(self.config.closingTime[openingDay])
                roomList.append(model.room.Room(i+1, openingTime, closingTime, self.config.minimalTimeSlot))

            self.ui.addWeekday(openingDay, roomList, self.createTherapist)

            self.rooms[openingDay] = roomList

    def getTherapistFromDayAndName(self, weekday, name):
        for therapistId in self.therapists:
            if self.therapists[therapistId].name == name and self.therapists[therapistId].assignedWeekday == weekday:
                return self.therapists[therapistId]
        return None

    def createTherapist(self, weekday, name, delete=False):
        """
        Creates a new therapist
        :param weekday: The weekday on which the therapist ist active
        :param name: The name of the therapist to be created
        :param delete: If this is true the therapist with the given name is deleted instead of created
        :return: A lmbda function that can be used to set the time slots of the created therapist. The function has
        a list of time slots as input parameter
        """
        if delete:
            print(f"Deleting therapist {name} on {weekday}")
            selectedTherapist = self.getTherapistFromDayAndName(weekday, name)
            if selectedTherapist is not None:
                # first delete time slots so the room can be updated easily
                selectedTherapist.timeSlots = []
                selectedTherapist.assignedRooms = {}
                selectedTherapist.unassignedTimeSlots = []
                self.distributeTherapistsToRooms(weekday)

                # now also delete model object
                del self.therapists[selectedTherapist.id]
        else:
            print(f"Adding therapist {name} on {weekday}")

            self.lastUsedThId += 1
            newTherapist = model.therapist.Therapist(self.lastUsedThId, name, weekday)
            self.therapists[self.lastUsedThId] = newTherapist

            return lambda day, thName, timeSlots, setActive: self.setTherapistTimes(day, thName, timeSlots, setActive)

    def setTherapistTimes(self, weekday, name, timeSlots, setActive):
        therapist = self.getTherapistFromDayAndName(weekday, name)
        if therapist is not None:
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
                        self.ui.setRoomOccupation(weekday, room.id, i, "")

        # now insert all unassigned therapist time slots into rooms
        for therapist in self.therapists.values():
            if therapist.assignedWeekday == weekday:
                remainingTimeWindows = therapist.timeSlots.copy()
                for timeSlot in therapist.timeSlots:
                    if therapist.assignedRooms[timeSlot] == -1:
                        for room in self.rooms[weekday]:
                            time = room.computeTimeFromOccupationIndex(timeSlot)
                            if not room.isOccupied(time):
                                room.addOccupation(therapist.id, time)
                                therapist.assignedRooms[timeSlot] = room.id
                                self.ui.setRoomOccupation(weekday, room.id, timeSlot, therapist.name)

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

    def saveState(self, savePath):
        try:
            with open(savePath, mode="wb") as file:
                saveContainer = model.saveContainer.SaveContainer(self.VERSION_NUMBER, self.config, self.rooms, self.therapists)
                pickle.dump(saveContainer, file)
                file.close()
                print(f"Saved state to file {savePath}.")
                return True
        except (OSError, pickle.PicklingError):
            print(f"Could not save state to file {savePath}!")
            return False

    def loadState(self, filePath):
        self.rooms = {}
        self.therapists = {}
        self.lastUsedThId = -1

        try:
            with open(filePath, mode="rb") as file:
                loadedState = pickle.load(file)

                if loadedState is None:
                    print(f"Could not load state from file {filePath}!")
                    self.initializeFromConfig()
                    return "EMPTY"

                outString = "SUCCESS"

                if loadedState.generatedVersion != self.VERSION_NUMBER:
                    print(f"Loaded state was created with outdated version {loadedState.generatedVersion}, "
                          f"current version is {self.VERSION_NUMBER}")
                    outString = "OLD_VERSION"

                # restore the controller attributes from save state
                self.config = loadedState.configuration
                self.rooms = loadedState.modelRooms
                self.therapists = loadedState.modelTherapists
                for therapist in self.therapists.values():
                    if therapist.id > self.lastUsedThId:
                        self.lastUsedThId = therapist.id

                # restore UI from save state
                for weekday in self.config.openingTime:
                    self.ui.addWeekday(weekday, self.rooms[weekday], self.createTherapist)

                    for therapist in self.therapists.values():
                        if therapist.assignedWeekday == weekday:
                            self.ui.addTherapist(weekday, therapist.name,
                                                 lambda day, name, timeSlots, setActive: self.setTherapistTimes(day, name, timeSlots, setActive))
                            for timeSlot in therapist.timeSlots:
                                roomId = therapist.assignedRooms[timeSlot]
                                if roomId != -1:
                                    self.ui.setRoomOccupation(weekday, roomId, timeSlot, therapist.name)
                            self.ui.setTherapistAssignment(weekday, therapist.name, therapist.timeSlots, True)
                            self.ui.setTherapistAssignment(weekday, therapist.name, therapist.unassignedTimeSlots, False)

                print(f"Successfully loaded state from file {filePath}.")
                return outString
        except (OSError, pickle.UnpicklingError, EOFError):
            print(f"Could not load state from file {filePath}!")
            self.initializeFromConfig()
            return "EXCEPTION"

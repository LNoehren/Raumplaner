import model.room
import model.therapist
import utils


class Controller:

    def __init__(self, config):
        self.config = config
        self.rooms = {}
        self.therapists = []
        self.lastUsedThId = -1

        for openingDay in config.openingTime:
            roomList = []
            for i in range(config.numberOfRooms):
                openingTime = utils.timeStringToTime(config.openingTime[openingDay])
                closingTime = utils.timeStringToTime(config.closingTime[openingDay])
                roomList.append(model.room.Room(i + 1, openingTime, closingTime, config.minimalTimeSlot))

            self.rooms[openingDay] = roomList

    """
    Function ads a therapist on the given day in the given time window.
    In case no room is available at any time of the time window, the remaining time slots at which
    no room was available is returned
    """
    def addTherapist(self, weekday, name, start, end):
        print(f"Adding therapist {name} on {weekday} from {start} until {end}")

        self.lastUsedThId += 1
        newTherapist = model.therapist.Therapist(self.lastUsedThId, name, start, end)
        self.therapists.append(newTherapist)

        # first check if the therapist can fit completely in one room
        availableRoom = None
        for room in self.rooms[weekday]:
            roomFullyAvailable = True
            for time in range(start, end, self.config.minimalTimeSlot):
                if room.isOccupied(time):
                    roomFullyAvailable = False
                    break

            if roomFullyAvailable:
                availableRoom = room
                break

        remainingTimeWindows = []
        if availableRoom is not None:
            availableRoom.addOccupationRange(newTherapist.id, newTherapist.startingTime, newTherapist.endTime)
        else:
            # split the therapist up between different rooms
            remainingTimeWindows = list(range(start, end, self.config.minimalTimeSlot))
            for time in range(start, end, self.config.minimalTimeSlot):
                for room in self.rooms[weekday]:
                    if not room.isOccupied(time):
                        room.addOccupation(newTherapist.id, time)
                        remainingTimeWindows.remove(time)
                        continue

        if len(remainingTimeWindows) != 0:
            print(f"Could not fit therapist {name} into the available rooms. Remaining times: {remainingTimeWindows}")

        return remainingTimeWindows

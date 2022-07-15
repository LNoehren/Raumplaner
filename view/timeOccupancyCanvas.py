import view.resizingCanvas


FREE_ROOM_COLOR = "green"
OCCUPIED_ROOM_COLOR = "red"
ACTIVE_THERAPIST_COLOR = "yellow"
INACTIVE_THERAPIST_COLOR = "grey"


class TimeOccupancyCanvas(view.resizingCanvas.ResizingCanvas):

    def __init__(self, parent, nrTimeSlots, isRoomOccupancy, **kwargs):
        super().__init__(parent, **kwargs)

        self.setTherapistTimes = None
        self.nrTimeSlots = nrTimeSlots
        self.timeSlotWidth = self.width / nrTimeSlots
        self.timeSlots = []

        self.clickPos = []
        self.clickedOnInactive = False

        startX = 0
        for i in range(nrTimeSlots):
            if isRoomOccupancy:
                rect = self.create_rectangle(startX, 0, startX + self.timeSlotWidth, self.height + 4, fill=FREE_ROOM_COLOR)
            else:
                rect = self.create_rectangle(startX, 0, startX + self.timeSlotWidth, self.height + 4, activefill=ACTIVE_THERAPIST_COLOR)
                self.bind("<Button-1>", self.mouseClicked)
                self.bind("<ButtonRelease-1>", self.mouseReleased)

            self.timeSlots.append(rect)
            startX += self.timeSlotWidth

    def on_resize(self, event):
        super().on_resize(event)
        self.timeSlotWidth = self.width / self.nrTimeSlots

    def setSlotColors(self, slotList, color):
        for rectId in slotList:
            self.itemconfig(rectId, fill=color)

    def getTimeSlotFromPos(self, x, y):
        if y < 0 or y > self.height + 4 or x < 0 or x > self.width:
            return -1

        timeSlotIndex = int(x/self.timeSlotWidth)
        return self.timeSlots[timeSlotIndex]

    def mouseClicked(self, event):
        self.clickPos = [event.x, event.y]
        rectId = self.getTimeSlotFromPos(self.clickPos[0], self.clickPos[1])
        self.clickedOnInactive = self.itemcget(rectId, "fill") == ""

    def mouseReleased(self, event):
        if self.setTherapistTimes is None:
            return

        if event.y < 0 or event.y > self.height + 4 or event.x < 0 or event.x > self.width:
            self.clickPos = []
            return

        if len(self.clickPos) != 0:
            startRectId = self.getTimeSlotFromPos(self.clickPos[0], self.clickPos[1])
            endRectId = self.getTimeSlotFromPos(event.x, event.y)
            idRange = list(range(startRectId, endRectId+1) if startRectId < endRectId else range(endRectId, startRectId+1))

            if self.clickedOnInactive:
                self.setSlotColors(idRange, ACTIVE_THERAPIST_COLOR)
            else:
                self.setSlotColors(idRange, "")
            self.setTherapistTimes(idRange, self.clickedOnInactive)

            self.clickPos = []

import view.mainWindow
import controller
import configuration

if __name__ == '__main__':
    config = configuration.Configuration()
    config.read("assets/configuration.json")

    controller = controller.Controller(config)

    window = view.mainWindow.MainWindow(controller.addTherapist)
    for openingTimeDay in config.openingTime:
        window.addWeekday(openingTimeDay, config.numberOfRooms)

    window.mainloop()

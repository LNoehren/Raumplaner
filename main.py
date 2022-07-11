import view.mainWindow
import configuration

if __name__ == '__main__':
    config = configuration.Configuration()
    config.read("assets/configuration.json")

    window = view.mainWindow.MainWindow()

    for openingTimeDay in config.openingTime:
        window.addWeekday(openingTimeDay)

    window.mainloop()

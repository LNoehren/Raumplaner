import view.mainWindow
import controller
import configuration

if __name__ == '__main__':
    config = configuration.Configuration()
    config.read("assets/configuration.json")

    window = view.mainWindow.MainWindow()
    controller = controller.Controller(config, window)
    window.mainloop()

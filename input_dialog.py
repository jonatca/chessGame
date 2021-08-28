from graphics import *
from button import *


class InputDialog:
    """Takes the initial angle and velocity values, and the current wind value"""

    def __init__(self, suggested_start_time):
        self.win = win = GraphWin("Meny", 400, 400)
        self.win.setBackground("lightblue")
        win.setCoords(0, 10, 10, 0)
        Text(Point(3, 1), "Time White (min)").draw(win)
        self.white_time = Entry(Point(7, 1), 10).draw(win)
        self.white_time.setText(str(suggested_start_time))

        Text(Point(3, 2), "Time Black (min)").draw(win)
        self.black_time = Entry(Point(7, 2), 10).draw(win)
        self.black_time.setText(str(suggested_start_time))

        Text(Point(3, 3), "White players name").draw(win)
        self.white_name = Entry(Point(7, 3), 10).draw(win)
        self.white_name.setText("White")

        Text(Point(3, 4), "Black players name").draw(win)
        self.black_name = Entry(Point(7, 4), 10).draw(win)
        self.black_name.setText("Black")

        self.start = Button(win, Point(3.5, 8), 1.25, 0.5, "Start")
        self.start.activate()
        self.quit = Button(win, Point(7, 8), 1.25, 0.5, "Quit")
        self.quit.activate()

    """ Runs a loop until the user presses either the quit or fire button """

    def interact(self):
        while True:
            pt = self.win.getMouse()
            if self.quit.clicked(pt):
                return "Quit"
            if self.start.clicked(pt):
                return "Start"

    """ Returns the current values of (angle, velocity) as entered by the user"""

    def get_times(self):
        w = float(self.white_time.getText())
        b = float(self.black_time.getText())
        return w, b

    def get_names(self):
        w = self.white_name.getText()
        b = self.black_name.getText()
        return w, b

    def close(self):
        self.win.close()


""" A general button class (from the book) """

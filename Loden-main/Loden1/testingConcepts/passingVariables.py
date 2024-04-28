from tkinter import *

class Frames(object):

    def __init__(self):
        pass

    def main_frame(self, root):
        root.title('WeatherMe')
        root.geometry('300x100')

        self.query = StringVar()

        Label(root, text='Enter a city below').pack()

        Entry(root, textvariable=self.query).pack()

        Button(root, text="Submit", command=self.result_frame).pack()

    def result_frame(self):
        result = Toplevel()
        result.title('City')
        result.geometry('1600x150')

        print(self.query.get()) #This would print the StringVar's value , use this in whatever way you want.

        forecast = ['20 degree test','20 degree test','20 degree test']

        Label(result, text='1-3 DAY: \n' + forecast[0]).pack()
        Label(result, text='4-7 DAY: \n' + forecast[1]).pack()
        Label(result, text='8-10 DAY: \n' + forecast[2]).pack()

        Button(result, text="OK", command=result.destroy).pack()


root = Tk()
app = Frames()
app.main_frame(root)
root.mainloop()
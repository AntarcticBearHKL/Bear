import tkinter
from tkinter import END

class UI:
    def __init__(self):
        self.gadgetDict = {}
        self.gadgetDict['__main__'] = tkinter.Tk()

    def uiConfig(self, x, y, xo, yo):
        self.findGadget('__main__').geometry('''%dx%d+%d+%d'''%(x,y,xo,yo))

    def findGadget(self, name):
        try:
            return self.gadgetDict[name]
        except Exception as e:
            return None

    def f(self, name):
        self.findGadget(name)
    
    def newLabel(self, name, text, size, position):
        self.gadgetDict[name] = tkinter.Label(
            self.findGadget('__main__'), text = text,
            width = size[0], height = size[1],
        )
        self.gadgetDict[name].place(x = position[0], y = position[1])

    def newButton(self, name, text, command, size, position):
        self.gadgetDict[name] = tkinter.Button(
            self.findGadget('__main__'), text = text,
            width = size[0], height = size[1],
            command = command
        )
        self.gadgetDict[name].place(x = position[0], y = position[1])

    def newEntry(self, name, text, size, position):
        self.gadgetDict[name] = tkinter.Entry(
            self.findGadget('__main__'), text = text,
            width = size[0],
        )
        self.gadgetDict[name].place(x = position[0], y = position[1])

    def getS(self, name):
        return self.gadgetDict[name].get()

    def setS(self, name , content):
        self.gadgetDict[name].delete(0, END)
        self.gadgetDict[name].insert(0, content)

    def uiSetting(self, name):
        return self.gadgetDict[name].configure

    def us(self, name):
        return self.uiSetting(name)

    def start(self):
        self.findGadget('__main__').mainloop()

if __name__ == '__main__':
    ui = UI()
    ui.uiConfig(900,900,100,100)
    ui.newButton('b1', 'click', None, [10,10], [0,0])
    ui.start()
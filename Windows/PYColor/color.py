from UI import UI
import random

TestMode = 0
ColorMode = 0

Window = UI()
Window.uiConfig(450,400,100,100)

if TestMode == 0:
    Window.newLabel('Background', 'Color', [500, 400], [0,0])
    Window.us('Background')(bg = '#FFFFFF')
    BaseX = 162
    BaseY = 43
    OffsetX = 0
    OffsetY = 60
    Window.newButton('buttonA', 'A', lambda: select(0), [15,0], [BaseX,BaseY+OffsetY*0])
    Window.newButton('buttonB', 'B', lambda: select(1), [15,0], [BaseX,BaseY+OffsetY*1])
    Window.newButton('buttonC', 'C', lambda: select(2), [15,0], [BaseX,BaseY+OffsetY*2])
    Window.newButton('buttonD', 'D', lambda: select(3), [15,0], [BaseX,BaseY+OffsetY*3])
    Window.newButton('buttonN', 'Start', lambda: nextCommand(), [15,0], [BaseX,BaseY+OffsetY*4])
    Window.newLabel('labelA', 'Answer', [15,0], [BaseX,BaseY+OffsetY*5])
    colorList = [1,2,3,4,5,6,7,8,9,0,'A','B','C','D','E','F']
    def getColor():
        color = '#'
        for count in range(6):
            color += str(colorList[random.randint(0,15)])
        return color

    def getGray():
        color = ''
        for count in range(2):
            color += str(colorList[random.randint(0,15)])
        return '#' + color * 3

    def H2O(hexinput):
        output = '('
        for i in range(3):
            output += str(int(hexinput[1+2*i:1+2*i+2],16))
            if i != 2:
                output += ', '
        output += ')'
        return output



    TrueColor = None
    TrueButton = None
    if ColorMode == 0:
        genColor = getColor
    elif ColorMode == 1:
        genColor = getGray

    def nextCommand():
        global TrueColor
        global TrueButton
        buttonList = ['buttonA', 'buttonB', 'buttonC', 'buttonD']
        TrueColor = genColor()
        Window.us('Background')(bg = TrueColor)
        Window.us('buttonN')(text = 'Next')
        TrueButton = random.randint(0,3)
        for count in range(4):
            if count == TrueButton:
                Window.us(buttonList[count])(text = H2O(TrueColor))
            else:
                Window.us(buttonList[count])(text = H2O(genColor()))
        Window.us('labelA')(text = 'Answer')

    def select(input):
        if input == TrueButton:
            Window.us('labelA')(text = 'true')
        else:
            Window.us('labelA')(text = 'false')


elif TestMode == 1:
    Window.newLabel('Backgroundl', '', [35, 40], [0,0])
    Window.newLabel('Backgroundr', '', [35, 40], [220,0])
    Window.us('Backgroundl')(bg = '#555555')
    Window.us('Backgroundr')(bg = '#555555')
    BaseX = 162
    BaseY = 23
    OffsetX = 0
    OffsetY = 50
    Window.newEntry('answerR', '', [18,10], [BaseX,BaseY+OffsetY*1])
    Window.newEntry('answerG', '', [18,10], [BaseX,BaseY+OffsetY*2])
    Window.newEntry('answerB', '', [18,10], [BaseX,BaseY+OffsetY*3])
    Window.newButton('buttonE', 'Examine', lambda: examineCommand(),[15,0], [BaseX,BaseY+OffsetY*4])
    Window.newButton('buttonN', 'Start', lambda: nextCommand(), [15,0], [BaseX,BaseY+OffsetY*5])
    Window.newLabel('labelA', 'Answer', [21,0], [BaseX-19,BaseY+OffsetY*6])


    colorList = [1,2,3,4,5,6,7,8,9,0,'A','B','C','D','E','F']
    def getColor():
        color = '#'
        for count in range(6):
            color += str(colorList[random.randint(0,15)])
        return color

    def getGray():
        color = ''
        for count in range(2):
            color += str(colorList[random.randint(0,15)])
        return '#' + color * 3

    def H2O(hexinput):
        output = '('
        for i in range(3):
            output += str(int(hexinput[1+2*i:1+2*i+2],16))
            if i != 2:
                output += ', '
        output += ')'
        return output

    def O2H(input):
        output = '#'
        for item in input:
            hexout = str(hex(int(item, 10)))[2:]
            if len(hexout) == 1:
                output += '0' + hexout
            else:
                output += hexout
        return output


    TrueColor = None
    if ColorMode == 0:
        genColor = getColor
    elif ColorMode == 1:
        genColor = getGray

    def nextCommand():
        global TrueColor
        global TrueButton
        TrueColor = genColor()
        Window.us('Backgroundl')(bg = TrueColor)
        Window.us('buttonN')(text = 'Next')
        Window.us('labelA')(text = 'Answer')
        Window.setS('answerR', '0')
        Window.setS('answerG', '0')
        Window.setS('answerB', '0')

    def examineCommand():
        answer = [Window.getS('answerR'), Window.getS('answerG'), Window.getS('answerB')]
        Window.us('Backgroundr')(bg = O2H(answer))
        for count in range(3):
            answer[count] = str(int(O2RGB(TrueColor)[count]) - int(answer[count]))
        Window.us('labelA')(text = H2O(TrueColor) + '   ' + '  '.join(answer))

    def O2RGB(input):
        return H2O(input)[1:-1].split(',')


Window.start()

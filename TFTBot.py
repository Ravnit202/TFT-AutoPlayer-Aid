import threading
from pyautogui import *
from pytesseract import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QFont
from qt_material import apply_stylesheet
import pyautogui
import pydirectinput
import time
import keyboard
import random
import win32api, win32con, win32gui
import psutil
import sys

pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class windowManager(QMainWindow):
    
    def __init__(self):

        super(windowManager, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200,200,485,200)
        self.setWindowTitle("TFT Bot")
        self.setMinimumSize(460,200)

        self.traitLabel = QtWidgets.QLabel(self)
        self.traitLabel.setText("Traits")
        self.traitLabel.setFont(QFont('Helvetica', 12))
        self.traitLabel.move(30,20)
        

        self.buyRedeemed = QCheckBox("Redeemed", self)
        self.buyRedeemed.move(30,45)
        self.buyRedeemed.setFont(QFont('Helvetica', 10))
        
        self.buyForgotten = QCheckBox("Forgotten", self)
        self.buyForgotten.move(30,75)
        self.buyForgotten.setFont(QFont('Helvetica', 10))

        self.buyDawnbringer = QCheckBox("Dawnbringer", self)
        self.buyDawnbringer.move(30,105)
        self.buyDawnbringer.setFont(QFont('Helvetica', 10))
        self.buyDawnbringer.resize(320,30)

        self.buyHellion = QCheckBox("Hellion", self)
        self.buyHellion.move(30,135)
        self.buyHellion.setFont(QFont('Helvetica', 10))
  
        self.optionsLabel = QtWidgets.QLabel(self)
        self.optionsLabel.setText("Options")
        self.optionsLabel.move(155,20)
        self.optionsLabel.setFont(QFont('Helvetica', 12))

        self.buyOneCosts = QCheckBox("Buy One Costs", self)
        self.buyOneCosts.move(155,50)
        self.buyOneCosts.resize(300,20)
        self.buyOneCosts.setFont(QFont('Helvetica', 10))
        self.buyOneCosts.setToolTip('If checked, the bot will buy all 1-cost units')

        self.putUnits = QCheckBox("Place and Sell Units", self)
        self.putUnits.move(155,80)
        self.putUnits.resize(300,20)
        self.putUnits.setFont(QFont('Helvetica', 10))
        self.putUnits.setToolTip('If checked, the bot will randomly place and sell units')

        self.noSurrender = QCheckBox("Don't Surrender", self)
        self.noSurrender.move(155,110)
        self.noSurrender.resize(300,20)
        self.noSurrender.setFont(QFont('Helvetica', 10))
        self.noSurrender.setToolTip('If checked, the bot will not surrender')

        self.runTime = QCheckBox("Run Indefinitely", self)
        self.runTime.setChecked(True)
        self.runTime.move(155,140)
        self.runTime.resize(300,20)
        self.runTime.setFont(QFont('Helvetica', 10))
        self.runTime.setToolTip('If unchecked, the bot will run for a total of 5 games')

        self.startButton = QtWidgets.QPushButton(self)
        self.startButton.setText("Start Bot")
        self.startButton.move(360, 50)
        self.startButton.clicked.connect(self.begin)
        self.startButton.resize(110,200)

        self.stopButton = QtWidgets.QPushButton(self)
        self.stopButton.setText("Terminate")
        self.stopButton.move(360, 122)
        self.stopButton.clicked.connect(terminateProcess)
        self.stopButton.setProperty('class', 'danger')
        self.stopButton.resize(110,200)

        
        self.screenRes = pyautogui.size()
        print("Screen", self.screenRes)

    def func(self):
        '''long-running work'''
        self.startButton.setText('Starting...')
        time.sleep(2)
        self.startButton.setStyleSheet('color : #3fda0b; border-color : #3fda0b')
        self.startButton.setText('Running')
        checkAndStart(self)
        time.sleep(0.2)
        self.startButton.setStyleSheet('color: #448aff; border-color : #448aff')
        self.startButton.setText('Start Bot')

    def begin(self):
        '''start a thread and connect it to func'''
        threading.Thread(target=self.func, daemon=True).start()

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(float(random.randrange(20, 40))/100)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def rightClick(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    time.sleep(float(random.randrange(20, 40))/100)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

def terminateProcess():
    sys.exit()

def checkIfGameOpen():
    for proc in psutil.process_iter():
        try:   
            if "LeagueClientUxRender.exe".lower() in proc.name().lower():
                return True 
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def _windowEnumHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def openLeague(window_name):
    top_windows = []
    win32gui.EnumWindows(_windowEnumHandler, top_windows)
    for i in top_windows:
        #print(i[1])
        if window_name.lower() in i[1].lower():
            #print("found", window_name)
            try:
                win32gui.ShowWindow(i[0], win32con.SW_SHOWNORMAL)
                win32gui.SetForegroundWindow(i[0])
            except:
                print("Can't open league")
            break

def quitGame():
    pydirectinput.press('esc')
    firstSurrender = pyautogui.locateOnScreen('./inGame/Surrender.png', confidence=0.80)
    if(firstSurrender) != None:
        click(firstSurrender[0]+12, firstSurrender[1]+5)
        time.sleep(0.5)
        finalSurrender = pyautogui.locateOnScreen('./inGame/Surrender Confirm.png', confidence=0.80)
        if(finalSurrender) != None:
            click(finalSurrender[0]+11, finalSurrender[1]+4)
            time.sleep(5)
            return True
    return False

def checkAndStart(self):
    openOrNot = checkIfGameOpen()
    if(openOrNot):
        startGame(self)
    else:
        QMessageBox.about(self,"Game not Running", "Open League of Legends to begin")  


def greeting():
    pydirectinput.press('enter')
    pydirectinput.write('hello fellow summoners!')
    pydirectinput.press('enter')

def randomize(max):
    return int(random.randrange(5, max))

def startGame(self):
    gamesPlayed = 0 # Track how many games have been played
    placeDelay = 0
    #time.sleep(2)   # Time to open up the screen
    openLeague("League of Legends")
    time.sleep(0.5)

    pregame = True
    if(pyautogui.locateOnScreen('./inGame/In Game.png',grayscale=True, confidence=0.60)):
        pregame = False
    
    print("Bot Started")
    while keyboard.is_pressed('q') is False:

        if(pregame):    
            
            playButton = pyautogui.locateOnScreen('./outOfGame/Play.png', grayscale=True, confidence=0.70)
            if (playButton)!= None:
                click(playButton[0]+randomize(55), playButton[1]+randomize(20))

            partyButton = pyautogui.locateOnScreen('./outOfGame/Party.png', confidence=0.75)
            if (partyButton)!= None:
                click(partyButton[0]+randomize(25) , partyButton[1]+randomize(20))   

            TFTButton = pyautogui.locateOnScreen('./outOfGame/TFT.png', grayscale=True, confidence=0.75)
            if (TFTButton)!= None:
                click(TFTButton[0]+randomize(25), TFTButton[1]+randomize(20))

            confirmButton = pyautogui.locateOnScreen('./outOfGame/Confirm.png', grayscale=True, confidence=0.75)
            if (confirmButton)!= None:
                click(confirmButton[0]+randomize(25), confirmButton[1]+randomize(20))

            findMatchButton = pyautogui.locateOnScreen('./outOfGame/Find Match.png', grayscale=True, confidence=0.75)
            if (findMatchButton)!= None:
                click(findMatchButton[0]+randomize(55), findMatchButton[1]+randomize(20))

            chatOpen = pyautogui.locateOnScreen('./outOfGame/Chat Open.png', grayscale=True, confidence=0.75)
            if (chatOpen)!= None:
                click(chatOpen[0]+5, chatOpen[1]+5)

            acceptMatch = pyautogui.locateOnScreen('./outOfGame/Accept Match.png', grayscale=True, confidence=0.75)
            if (acceptMatch)!= None:
                click(acceptMatch[0]+randomize(55), acceptMatch[1]+randomize(35))
                time.sleep(0.5)

            okButton = pyautogui.locateOnScreen('./outOfGame/Ok Button.png', grayscale=True, confidence=0.86)
            if (okButton)!= None:
                click(okButton[0]+randomize(45),okButton[1]+randomize(20))

            playAgain = pyautogui.locateOnScreen('./outOfGame/Play Again.png', grayscale=True, confidence=0.75)
            if (playAgain) != None:
                click(playAgain[0]+randomize(25) , playAgain[1]+randomize(20))     
                
                   

            gameStart = pyautogui.locateOnScreen('./inGame/Game Start.png', grayscale=True, confidence=0.75)
            if (gameStart)!= None:
                greeting()
                print("greeted players")
                pregame = False


                
        ###Champion Detection###


        else:

            if(self.noSurrender.isChecked() is False):
                gameEnd = pyautogui.locateOnScreen('./inGame/End Game.png', confidence=0.8)
                if(gameEnd)!= None:
                    print('Surrendering')
                    complete = quitGame()
                    if (complete):
                        print('Surrendered')
                        gamesPlayed += 1
                        print(gamesPlayed)
                        pregame = True
                        if(self.runTime.isChecked() is False and (gamesPlayed >= 5)):
                            break

            if(self.buyOneCosts.isChecked() is True):
                oneGold = pyautogui.locateOnScreen('./inGame/One Gold.png', confidence=0.80)
                if(oneGold) != None:
                    img = pyautogui.screenshot(region=(875, 848, 35, 26))
                    output = pytesseract.image_to_string(img, config="--psm 13")
                    a = output[0].isdigit()
                    print(output[0], output[0].isdigit())
                    try:
                        if((a is False) or int(output[0]) !=0): 
                            pyautogui.moveTo(oneGold[0]-30, oneGold[1]-30, duration=float(random.randrange(5,20)/100))
                            click(oneGold[0]-30, oneGold[1]-30)
                    except:
                        pass
            
            if(self.buyRedeemed.isChecked() is True):
                redeemed = pyautogui.locateOnScreen('./champions/Redeemed.png', confidence=0.80)
                if(redeemed) != None:
                    r = randomize(40)
                    pyautogui.moveTo(redeemed[0]+r, redeemed[1] + r, duration=float(random.randrange(5,30)/100))
                    click(redeemed[0]+ r, redeemed[1] + r)

            if(self.buyForgotten.isChecked() is True):
                forgotten = pyautogui.locateOnScreen('./champions/Forgotten.png', confidence=0.80)
                if(forgotten) != None:
                    r = randomize(40)
                    pyautogui.moveTo(forgotten[0]+r,forgotten[1] + r, duration=float(random.randrange(5,30)/100))
                    click(forgotten[0]+ r, forgotten[1] + r)

            if(self.buyDawnbringer.isChecked() is True):
                dawnbringer = pyautogui.locateOnScreen('./champions/Dawnbringer.png', confidence=0.80)
                if(dawnbringer) != None:
                    r = randomize(40)
                    pyautogui.moveTo(dawnbringer[0]+r,dawnbringer[1] + r, duration=float(random.randrange(5,30)/100))
                    click(dawnbringer[0]+ r, dawnbringer[1] + r)

            if(self.buyHellion.isChecked() is True):
                hellion = pyautogui.locateOnScreen('./champions/Hellion.png', confidence=0.80)
                if(hellion) != None:
                    r = randomize(40)
                    pyautogui.moveTo(hellion[0]+r, hellion[1] + r, duration=float(random.randrange(5,40)/100))
                    click(hellion[0]+ r, hellion[1] + r)

            levelUnit = pyautogui.locateOnScreen('./inGame/Two Star.png', confidence=0.80)
            if(levelUnit) != None:
                r = randomize(80)
                pyautogui.moveTo(levelUnit[0]+r,levelUnit[1] + r, duration=float(random.randrange(5,30)/100))
                click(levelUnit[0]+ r, levelUnit[1] + r)

            continueWidget = pyautogui.locateOnScreen('./inGame/Enemies Surrendered.png', confidence=0.80)
            if(continueWidget) != None:
                r = randomize(40)
                pyautogui.moveTo(continueWidget[0]+r,continueWidget[1] + r, duration=float(random.randrange(5,30)/100))
                click(continueWidget[0]+ r, continueWidget[1] + r)

            ###Items and Orbs###


            blueOrb = pyautogui.locateOnScreen('./inGame/blueOrb.png', confidence=0.65)
            if(blueOrb) != None:
                r = randomize(15)
                pyautogui.moveTo(blueOrb[0]+r, blueOrb[1]+r, duration=float(random.randrange(10,20)/100))
                rightClick(blueOrb[0]+r, blueOrb[1]+r)


            greyOrb = pyautogui.locateOnScreen('./inGame/greyOrb.png', confidence=0.75)
            if(greyOrb) != None:
                r = randomize(15)
                pyautogui.moveTo(greyOrb[0]+r, greyOrb[1]+r, duration=float(random.randrange(5,20)/100))
                rightClick(greyOrb[0]+r, greyOrb[1]+r)


            apWand = pyautogui.locateOnScreen('./inGame/APWand.png', confidence=0.65)
            if(apWand) != None:
                r = randomize(30)
                #pyautogui.moveTo(apWand[0]+5, apWand[1]+5, duration=float(random.randrange(5,20)/100))
                click(apWand[0]+r, apWand[1]+r)
                rightClick(apWand[0]+r, apWand[1]+r)
            
            chooseOne = pyautogui.locateOnScreen('./inGame/ChooseOne.png', confidence=.70)
            if(chooseOne)!= None:
                r = random.randrange(-100,100)
                if r > 0:
                    r=100
                else:
                    r=-100
                pyautogui.moveTo(chooseOne[0]+r, chooseOne[1]+50, float(random.randrange(10,40)/100))
                click(chooseOne[0]+r, chooseOne[1]+r)

            ### Champion Placement ###
            if(placeDelay >= 15 and self.putUnits.isChecked() is True):
                placeDelay = 0
                c = random.randint(0,5)

                if(c==0 or c==1):
                    pyautogui.moveTo(953, 629, float(random.randrange(20, 60))/100)
                    pydirectinput.press('e')

                elif(c==1 or c==2):
                    pyautogui.moveTo(976, 637, float(random.randrange(20, 60))/100)
                    pydirectinput.press('e')

                elif(c==2 or c==3):
                    pyautogui.moveTo(915, 528, float(random.randrange(20, 60))/100)
                    pydirectinput.press('e')

                elif(c==3 or c==4):
                    pyautogui.moveTo(584, 640, float(random.randrange(20, 60))/100)
                    pydirectinput.press('e')
                    
                elif(c==4 or c==5):
                    pyautogui.moveTo(random.randrange(471, 917), 754, float(random.randrange(20, 60))/100)
                    pydirectinput.press('e')
                

                pyautogui.moveTo(random.randrange(471, 917), 754, float(random.randrange(10, 30))/100)
                pydirectinput.press('w')

                
            placeDelay += 1
            #X:  471 Y:  754 RGB: (160, 149, 132)
            #if(pyautogui.pixel(471, 754)[0] != 160):
            #    dragCursor(471, 754)
    print("Finished " + str(gamesPlayed), "Games and Stopped")



if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = windowManager()
    
    extra = {
        # Button colors
        'danger': '#dc3545',
        # Font
        'font-family': 'Roboto',
    }
    apply_stylesheet(app, theme='dark_blue.xml', extra=extra)

    qtRectangle = window.frameGeometry()
    centerPoint = QDesktopWidget().availableGeometry().center()
    qtRectangle.moveCenter(centerPoint)
    window.move(qtRectangle.topLeft())
    qtRectangle = window.frameGeometry()

    window.show()  
    app.exec_()


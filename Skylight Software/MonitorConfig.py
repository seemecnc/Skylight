from tkinter import *
from tkinter.ttk import Separator
from math import *
from utils import *

class MonitorConfig(Tk):
    def __init__(self, handler):
        Tk.__init__(self)
        
        
        self.handler = handler    
        
        
        self.pX = StringVar(self)
        self.pY = StringVar(self)
        self.pW = StringVar(self)
        self.pH = StringVar(self)
        self.pxCM = StringVar(self)
        self.dState = StringVar(self)
        self.drawState = "area"
        
        container = Frame(self)
        container.pack(side=TOP)
        
        self.dState.set("area")
        
        self.areaCanvas = Canvas(container, width=300, height=300)
        self.areaCanvas.pack(side=LEFT)
        
        settingsFrame = Frame(container)
        
        Label(settingsFrame, text="Print Area Width").pack(anchor=W)
        self.widthText = Spinbox(settingsFrame, from_=1, to=2, textvariable=self.pW)
        self.widthText.pack()
        #widthText.bind('<KeyRelease>', self.valueChanged)
        Label(settingsFrame, text="Print Area Height").pack(anchor=W)
        self.heightText = Spinbox(settingsFrame, from_=1, to=2, textvariable = self.pH)
        self.heightText.pack()
        Label(settingsFrame, text="Margin From Left").pack(anchor=W)
        self.posXText = Spinbox(settingsFrame, from_=0, to=1, textvariable = self.pX)
        self.posXText.pack()
        Label(settingsFrame, text="Margin From Top").pack(anchor=W)
        self.posYText = Spinbox(settingsFrame, from_=0, to=1, textvariable = self.pY)
        self.posYText.pack()
        
        Separator(settingsFrame, orient=HORIZONTAL).pack(expand=True, fill=X, pady=10)
        
        Label(settingsFrame, text="Pixels Per Centimeter").pack(anchor=W)
        
        self.pxPerMM = Spinbox(settingsFrame, from_=1, to=100, textvariable=self.pxCM)
        self.pxPerMM.pack()
        
        Separator(settingsFrame, orient=HORIZONTAL).pack(expand=True, fill=X, pady=10)
        Label(settingsFrame, text="Show").pack(anchor=W)
        
        showAreaBtn = Radiobutton(settingsFrame, text="Print Area", value="area", variable=self.dState)
        showAreaBtn.pack(side=RIGHT, anchor=W)
        showGridBtn = Radiobutton(settingsFrame, text="Grid", value="grid", variable=self.dState)
        showGridBtn.pack(side=LEFT, anchor=W)
        
        
        settingsFrame.pack(side=LEFT)
        
        actionFrame = Frame(self)
        actionFrame.pack(anchor=S)
        saveBtn = Button(actionFrame, text="Save", command=self.saveSettings)
        saveBtn.pack(side=LEFT, padx=10, pady=10, ipadx=8, ipady = 2)
        cancelBtn = Button(actionFrame, text="Cancel", command=self.cancel)
        cancelBtn.pack(side=LEFT, padx=10, pady=10, ipadx=8, ipady = 2)
        
        
        self.pX.trace("w", self.areaChanged)
        self.pY.trace("w", self.areaChanged)
        self.pW.trace("w", self.areaChanged)
        self.pH.trace("w", self.areaChanged)
        self.pxCM.trace("w", self.ratioChanged)
        self.dState.trace("w", self.drawChange)
        
        self.reloadDisplay()
        
        self.redraw()
    def reloadDisplay(self):
        self.mW = self.handler.window.dimensions['width']
        self.mH = self.handler.window.dimensions['height']
        
        monConfig = self.handler.config.getDisplay(self.handler.config.get('selectedDisplay'))
        
        self.widthText['to'] = self.mW
        self.heightText['to'] = self.mH
        self.posXText['to'] = self.mW
        self.posYText['to'] = self.mH
        self.pxPerMM['to'] = max(self.mW, self.mH)
        
        if 'printArea' in monConfig:
            self.pX.set(monConfig['printArea']['x'])
            self.pY.set(monConfig['printArea']['y'])
            self.pW.set(monConfig['printArea']['width'])
            self.pH.set(monConfig['printArea']['height'])
        else:
            self.pX.set(round(self.mW * .1))
            self.pY.set(round(self.mH * .1))
            self.pW.set(round(self.mW * .80))
            self.pH.set(round(self.mH * .80))
        if 'pixelsPerCM' in monConfig:
            self.pxCM.set(monConfig['pixelsPerCM'])
        else:
            self.pxCM.set(50)
        self.posXText['to'] = self.mW - parseInt(self.pW.get())
        self.posYText['to'] = self.mH - parseInt(self.pH.get())
    def ratioChanged(self, *args):
        validateInt(self.pxCM, self.pxPerMM)
        
        self.drawState = "grid"
        self.redraw()
    def areaChanged(self, *args):
        validateInt(self.pW, self.widthText)
        validateInt(self.pH, self.heightText)
        self.posXText['to'] = parseInt(self.widthText['to']) - parseInt(self.pW.get())
        self.posYText['to'] = parseInt(self.heightText['to']) - parseInt(self.pH.get())
        validateInt(self.pX, self.posXText)
        validateInt(self.pY, self.posYText)
        
        
        self.drawState = "area"
        self.redraw()
        
    def drawChange(self, *args):
        self.drawState = self.dState.get()
        self.redraw()
    def redraw(self):
        if self.drawState == "area":
            self.redrawArea()
        elif self.drawState == "grid":
            self.redrawGrid()
    def redrawGrid(self):
        self.areaCanvas.delete('all')
        if self.mW / 300 > self.mH /300:
            scale = 300 / self.mW
            drawW = 300
            drawH = scale * self.mH
        else:
            scale = 300 / self.mH
            drawW = scale * self.mW
            drawH = 300
        bX = round((300 - drawW)/2)
        bY = round((300 - drawH)/2)
        self.areaCanvas.create_rectangle(bX, bY, drawW + bX, drawH + bY, fill="#000000")
        
        
        temppxCM = float(self.pxCM.get())
        linesX = floor(self.mW / temppxCM)
        if linesX % 2 == 1:
            linesX -=1
        linesX /= 2
        
        linesY = floor(self.mH / temppxCM)
        if linesY % 2 == 1:
            linesY -= 1
        linesY /= 2
        
        diffX = self.mW / 2 - linesX * temppxCM
        diffY = self.mH / 2 - linesY * temppxCM
        for i in range(0, int((linesX * 2) + 1)):
            tempX = round( i * temppxCM * scale) + scale * diffX
            self.areaCanvas.create_line(tempX + bX, bY, tempX + bX, bY + drawH, fill="#FF0000")
        for i in range(0, int((linesY * 2) + 1)):
            tempY = round( i * temppxCM * scale) +  scale * diffY
            self.areaCanvas.create_line( bX, tempY + bY, bX + drawW, tempY + bY, fill="#FF0000")
            
        self.handler.window.clear()
        for i in range(0, int((linesX * 2) + 1)):
            self.handler.window.canvas.create_line(i * temppxCM + diffX , 0, i * temppxCM + diffX , self.mH, fill="#FF0000")
        for i in range(0, int((linesY * 2) + 1)):
            self.handler.window.canvas.create_line(0, i * temppxCM + diffY , self.mW, i * temppxCM + diffY, fill="#FF0000")
    def redrawArea(self):
        self.areaCanvas.delete('all')
        self.handler.window.clear()
        
        if self.mW / 300 > self.mH /300:
            scale = 300 / self.mW
            drawW = 300
            drawH = scale * self.mH
        else:
            scale = 300 / self.mH
            drawW = scale * self.mW
            drawH = 300
        bX = round((300 - drawW)/2)
        bY = round((300 - drawH)/2)
        
        _pX = parseInt(self.pX.get())
        _pY = parseInt(self.pY.get())
        _pW = parseInt(self.pW.get())
        _pH = parseInt(self.pH.get())
        
        self.areaCanvas.create_rectangle(bX, bY, drawW + bX, drawH + bY, fill="#000000")
        aX = round(scale * float(_pX)) + bX
        aY = round(scale * float(_pY)) + bY
        aW = round(scale * float(_pW)) + aX
        aH = round(scale * float(_pH)) + aY
        self.areaCanvas.create_rectangle(aX, aY, aW, aH, fill = "#FF0000", outline="#FF0000")
        
        self.handler.window.canvas.create_rectangle(_pX, _pY, _pW + _pX, _pH + _pY, fill="#FF0000", outline="#FF0000")
    def saveSettings(self):
        self.handler.config.saveDisplay(self.handler.config.get('selectedDisplay'), {'printArea':{'x':self.pX.get(), 'y':self.pY.get(), 'width':self.pW.get(), 'height':self.pH.get()}, 'pixelsPerCM':self.pxCM.get()})
        self.destroy()
    def cancel(self):
        self.destroy()
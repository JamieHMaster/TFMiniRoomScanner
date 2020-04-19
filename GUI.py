import tkinter
from tkinter import ttk
from tkinter import filedialog as fd 

root = tkinter.Tk()
root.title("3D Room Scanner")

main_frame = ttk.Frame(root, padding=20)
main_frame.grid()

fileName = ""
saveToLocation = ""

def getFileName():
    global fileName
    fileName = fd.askopenfilename() 
    print(fileName)

def getSaveLocation():
    global saveToLocation
    files = [('Text Document', '*.txt')] 
    saveToLocation = str(fd.asksaveasfile(filetypes = files, defaultextension = files))
    saveToLocation = saveToLocation.strip("<_io.TextIOWrapper name='")
    saveToLocation = saveToLocation.strip(" mode='w' encoding='cp1252'>")
    print(saveToLocation)

#main menu funtions
class MainMenu():
    def __init__(self):   
        #main menu widgets
        #create new scan
        self.newScanButton = ttk.Button(main_frame, text="Create new scan")
        self.newScanButton['command'] = lambda: newScanFunc()

        #upload scan from raw data
        self.rawUploadButton = ttk.Button(main_frame, text="Upload scan from RAW data")
        self.rawUploadButton['command'] = lambda: rawUploadFunc()

        #upload scan from processed data
        self.processedUploadButton = ttk.Button(main_frame, text="Upload scan from processed data")
        self.processedUploadButton['command'] = lambda: processedUploadFunc()

    def showWidgets(self):
        self.newScanButton.grid(row=0, column=0)
        self.rawUploadButton.grid(row=1, column=0)
        self.processedUploadButton.grid(row=2, column=0)
    
    def hideWidgets(self):
        self.newScanButton.grid_forget()
        self.rawUploadButton.grid_forget()
        self.processedUploadButton.grid_forget()

#new scan funtions
class NewScan():
    def __init__(self):   
        #create new scan widgets
        #create new scan label
        self.createNewScanLabel = ttk.Label(main_frame, text="Create new scan")

        #resolution label
        self.resolutionLabel = ttk.Label(main_frame, text="Resolution:")

        #resolution entry
        self.resolutionEntry = ttk.Entry(main_frame, widget=None)

        #Pan scan angle label
        self.panAngleLabel = ttk.Label(main_frame, text="Pan scan angle from ")

        #get minimum pan angle
        self.minimumPanEntry = ttk.Entry(main_frame, widget=None)

        #Pan scan angle label continued
        self.panAngleLabel2 = ttk.Label(main_frame, text=" to ")

        #Get maximum pan angle
        self.maximumPanEntry = ttk.Entry(main_frame, widget=None)

        #Tilt scan angle label
        self.tiltAngleLabel = ttk.Label(main_frame, text="Tilt scan angle from ")

        #get minimum pan angle
        self.minimumTiltEntry = ttk.Entry(main_frame, widget=None)

        #Pan scan angle label continued
        self.tiltAngleLabel2 = ttk.Label(main_frame, text=" to ")

        #Get maximum pan angle
        self.maximumTiltEntry = ttk.Entry(main_frame, widget=None)

        #Estimated time
        self.estimatedTimeLabel = ttk.Label(main_frame, text="Estimated time for completion: ")

        #Time to completion
        self.timeToCompletionLabel = ttk.Label(main_frame, text="0 seconds")

        #save button
        self.saveButton = ttk.Button(main_frame, text="Save Output to")
        self.saveButton['command'] = lambda: getSaveLocation()

        #start new scan
        self.startNewScan = ttk.Button(main_frame, text="Start New Scan")
        self.startNewScan['command'] = lambda: self.startNewScanFunc()

    def showWidgets(self):
        self.createNewScanLabel.grid(row=0, column=1)
        self.resolutionLabel.grid(row=1, column=0)
        self.resolutionEntry.grid(row=1, column=1)
        self.panAngleLabel.grid(row=2, column=0)
        self.minimumPanEntry.grid(row=2, column=1)
        self.panAngleLabel2.grid(row=2, column=2)
        self.maximumPanEntry.grid(row=2, column=3)
        self.tiltAngleLabel.grid(row=3, column=0)
        self.minimumTiltEntry.grid(row=3, column=1)
        self.tiltAngleLabel2.grid(row=3, column=2)
        self.maximumTiltEntry.grid(row=3, column=3)
        self.estimatedTimeLabel.grid(row=4, column=0)
        self.timeToCompletionLabel.grid(row=4, column=1)
        self.startNewScan.grid(row=5, column=3)
        self.saveButton.grid(row=5, column=2)
    
    def hideWidgets(self):
        self.createNewScanLabel.grid_forget()
        self.resolutionLabel.grid_forget()
        self.resolutionEntry.grid_forget()
        self.panAngleLabel.grid_forget()
        self.minimumPanEntry.grid_forget()
        self.panAngleLabel2.grid_forget()
        self.maximumPanEntry.grid_forget()
        self.tiltAngleLabel.grid_forget()
        self.minimumTiltEntry.grid_forget()
        self.tiltAngleLabel2.grid_forget()
        self.maximumPanEntry.grid_forget()
        self.estimatedTimeLabel.grid_forget()
        self.startNewScan.grid_forget()
        self.saveButton.grid_forget()
    
    def startNewScanFunc(self):
        import ReadAndDisplay
        global saveToLocation
        ReadAndDisplay.main(self.resolutionEntry.get(), self.minimumPanEntry.get(), self.maximumPanEntry.get(), self.minimumTiltEntry.get(), self.maximumTiltEntry.get(), saveToLocation)

#new scan funtions
class UploadRaw():
    def __init__(self):   
        #create new scan widgets
        #create new scan label
        self.uploadRawLabel = ttk.Label(main_frame, text="Upload scan from RAW data")

        #get source file label
        self.sourceFileLabel = ttk.Label(main_frame, text="Source file:")

        #get source file button
        self.sourceFileButton = ttk.Button(main_frame, text="Get file name")
        self.sourceFileButton['command'] = lambda: getFileName()

        #start upload
        self.startUploadButton = ttk.Button(main_frame, text="Start Upload")
        self.startUploadButton['command'] = lambda: self.startUpload()

    def showWidgets(self):
        self.uploadRawLabel.grid(row=0, column=1)
        self.sourceFileLabel.grid(row=1, column=0)
        self.sourceFileButton.grid(row=1, column=1)
        self.startUploadButton.grid(row=2, column=0)
    
    def hideWidgets(self):
        self.uploadRawLabel.grid_forget()
        self.sourceFileLabel.grid_forget()
        self.sourceFileButton.grid_forget()
        self.startUploadButton.grid_forget()
    
    def startUpload(self):
        import uploadRAWData
        global fileName
        uploadRAWData.main(fileName)

#new scan funtions
class UploadProcessed():
    def __init__(self):   
        #create new scan widgets
        #create new scan label
        self.uploadProcessedLabel = ttk.Label(main_frame, text="Upload scan from processed data")

        #get source file label
        self.sourceFileLabel = ttk.Label(main_frame, text="Source file:")

        #get source file button
        self.sourceFileButton = ttk.Button(main_frame, text="Get file name")
        self.sourceFileButton['command'] = lambda: getFileName()

        #start upload
        self.startUploadButton = ttk.Button(main_frame, text="Start Upload")
        self.startUploadButton['command'] = lambda: self.startUpload()

    def showWidgets(self):
        self.uploadProcessedLabel.grid(row=0, column=1)
        self.sourceFileLabel.grid(row=1, column=0)
        self.sourceFileButton.grid(row=1, column=1)
        self.startUploadButton.grid(row=2, column=0)
    
    def hideWidgets(self):
        self.uploadProcessedLabel.grid_forget()
        self.sourceFileLabel.grid_forget()
        self.sourceFileButton.grid_forget()
        self.startUploadButton.grid_forget()
    
    def startUpload(self):
        import uploadProcessedData
        global fileName
        uploadProcessedData.main(fileName)

mainMenu = MainMenu()
newScan = NewScan()
uploadRaw = UploadRaw() 
uploadProcessed = UploadProcessed()

def mainMenuFunc():
    newScan.hideWidgets()
    uploadRaw.hideWidgets()
    uploadProcessed.hideWidgets()
    mainMenu.showWidgets()

def newScanFunc():
    mainMenu.hideWidgets()
    uploadRaw.hideWidgets()
    uploadProcessed.hideWidgets()
    newScan.showWidgets()

def rawUploadFunc():
    mainMenu.hideWidgets()
    newScan.hideWidgets()
    uploadProcessed.hideWidgets()
    uploadRaw.showWidgets()

def processedUploadFunc():
    mainMenu.hideWidgets()
    newScan.hideWidgets()
    uploadRaw.hideWidgets()
    uploadProcessed.showWidgets()

def main():
    mainMenuFunc()
    root.mainloop()

main()
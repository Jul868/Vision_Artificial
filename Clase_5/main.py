import gui
import reportLog

if __name__ == "__main__":
    logReport = reportLog.ReportLog() #Solo corre el __init__ de la clase
    logReport.logger.info("Initializing Program")
    gui.main()
    
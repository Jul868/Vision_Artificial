import gui
import reportLog


if __name__ == "__main__":
    logReport = reportLog.ReportLog()
    logReport.logger.info("Init main")
    gui.main()
    
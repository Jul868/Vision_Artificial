import gui
import reportlog

if __name__=="__main__":
    logReport = reportlog.ReportLog() # Solo recorre el init de la clase creada 
    logReport.logger.info("Init main") # Inicia el prgrama 
    gui.main()
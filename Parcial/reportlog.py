import logging

class ReportLog():
    def __init__(self): # self -> acceder a todos los atributos de la clase
        try: # Trata de hacer lo que hay adentro hasta que haya un error 
            logging.basicConfig(filename="log.log", level = logging.INFO)
            self.logger = logging.getLogger()

        except Exception as e:
            self.logger.info("Error in class ReportLog" + str(e)) # Si hay un error me dice cual es con str(e)

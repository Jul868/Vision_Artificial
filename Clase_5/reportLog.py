import logging

class ReportLog:
    def __init__(self):
        try: # Intenta ejecutar el código, si hay un error.
            logging.basicConfig(filename='log.log', level=logging.INFO)
            self.logger = logging.getLogger()

        except Exception as e: # Si hay un error, lo imprime en consola
            self.logger.info("Error in class ReportLog: " + str(e))

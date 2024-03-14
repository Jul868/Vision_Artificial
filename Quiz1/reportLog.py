import logging

class ReportLog():
    def __init__(self):
        try:
            logging.basicConfig(filename="log.log", level=logging.INFO)
            self.logger = logging.getLogger()
        except Exception as e:
            self.logger.info("Error in class ReportLog " + str(e))
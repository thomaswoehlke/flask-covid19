import os

from database import app
from app.oodm.who.who_service_download import WhoServiceDownload
from app.oodm.who.who_service_import import WhoServiceImport
from app.oodm.who.who_service_update import WhoServiceUpdate


class WhoService:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WHO Service [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        self.__who_cvsfile_name = "WHO-COVID-19-global-data.csv"
        self.__src_who_cvsfile_name = "data"+os.sep+self.__who_cvsfile_name
        self.__src_who_cvsfile_tmp_name = "data"+os.sep+"tmp_"+self.__who_cvsfile_name
        self.__url_src_data = "https://covid19.who.int/"+self.__who_cvsfile_name
        self.who_service_download = WhoServiceDownload(database)
        self.who_service_import = WhoServiceImport(database)
        self.who_service_update = WhoServiceUpdate(database)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WHO Service [ready]")

    def run_download(self):
        app.logger.info(" run update [begin]")
        app.logger.info("------------------------------------------------------------")
        success = self.who_service_download.download_file()
        app.logger.info("")
        app.logger.info(" run update [done]")
        app.logger.info("------------------------------------------------------------")
        return success

    def run_update(self, import_file=True):
        app.logger.info(" run update [begin]")
        app.logger.info("------------------------------------------------------------")
        if import_file:
            self.who_service_import.import_file()
        self.who_service_update.update_db()
        app.logger.info("")
        app.logger.info(" run update [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_update_short(self, import_file=True):
        app.logger.info(" run update short [begin]")
        app.logger.info("------------------------------------------------------------")
        if import_file:
            self.who_service_import.import_file()
        self.who_service_update.update_db_short()
        app.logger.info("")
        app.logger.info(" run update short [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_update_initial(self, import_file=True):
        app.logger.info(" run update initial [begin]")
        app.logger.info("------------------------------------------------------------")
        if import_file:
            self.who_service_import.import_file()
        self.who_service_update.update_db_initial()
        app.logger.info("")
        app.logger.info(" run update initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self


from flask import flash

from database import app
from covid19.blueprints.rki.rki_service_download import RkiServiceDownload
from covid19.blueprints.rki.rki_service_import import RkiServiceImport
from covid19.blueprints.rki.rki_service_update import RkiServiceUpdate


class RkiService:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        self.service_download = RkiServiceDownload(database)
        self.service_import = RkiServiceImport(database)
        self.service_update = RkiServiceUpdate(database)
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" RKI Service [ready]")

    def pretask_database_drop_create(self):
        flash("rki_service.run_download started")
        success = self.service_download.download_file()
        return self

    def task_database_drop_create(self):
        self.service_import.import_file()
        self.service_update.update_db_short()
        return self

    def run_download(self):
        app.logger.info(" run update [begin]")
        app.logger.info("------------------------------------------------------------")
        success = self.service_download.download_file()
        app.logger.info("")
        app.logger.info(" run update [done]")
        app.logger.info("------------------------------------------------------------")
        return success

    def run_update(self, import_file=True):
        app.logger.info(" run update [begin]")
        app.logger.info("------------------------------------------------------------")
        if import_file:
            self.service_import.import_file()
        self.service_update.update_db()
        app.logger.info("")
        app.logger.info(" run update [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_update_short(self, import_file=True):
        app.logger.info(" run update short [begin]")
        app.logger.info("------------------------------------------------------------")
        if import_file:
            self.service_import.import_file()
        self.service_update.update_db_short()
        app.logger.info("")
        app.logger.info(" run update short [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_update_initial(self, import_file=True):
        app.logger.info(" run update initial [begin]")
        app.logger.info("------------------------------------------------------------")
        if import_file:
            self.service_import.import_file()
        self.service_update.update_db_initial()
        app.logger.info("")
        app.logger.info(" run update initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

import os
import subprocess
from database import app

admin_service = None


class AdminService:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Admin Service [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Admin Service [ready]")

    def run_admin_database_dump(self):
        app.logger.info(" run update countries [begin]")
        app.logger.info("------------------------------------------------------------")
        user = app.config['POSTGRES_USER']
        url = app.config['POSTGRES_URL']
        db = app.config['POSTGRES_DB']
        cmd = 'pg_dump -U '+user+' -h '+url+' '+db+' --inserts > data'+os.sep+'covid19data.sql'
        args = [cmd]
        result = subprocess.run(args, shell=True, check=True, capture_output=True, encoding='UTF-8')
        app.logger.info(" result: " + str(result.returncode))
        app.logger.info(" run update countries [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_admin_database_import(self):
        app.logger.info(" run update countries [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info("... TBD")
        app.logger.info(" run update countries [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_admin_database_drop(self):
        app.logger.info(" run update countries [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__database.drop_all()
        self.__database.create_all()
        app.logger.info("")
        app.logger.info(" run update countries [done]")
        app.logger.info("------------------------------------------------------------")
        return self

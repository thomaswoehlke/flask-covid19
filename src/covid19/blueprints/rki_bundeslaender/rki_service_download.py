import os
import wget
from flask import flash

from database import app
from covid19.blueprints.rki_bundeslaender.rki_service_config import RkiBundeslaenderServiceConfig


class RkiBundeslaenderServiceDownload:
    def __init__(self, database, config: RkiBundeslaenderServiceConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service Download [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service Download [ready]")

    def download_file(self):
        app.logger.info(" download - RKI [begin] ")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" download FILE: "+self.cfg.cvsfile_name+" from "+self.cfg.url_src)
        app.logger.info("------------------------------------------------------------")
        try:
            os.makedirs(self.cfg.data_path, exist_ok=True)
            if os.path.isfile(self.cfg.cvsfile_path):
                os.remove(self.cfg.cvsfile_path)
            data_file = wget.download(self.cfg.url_src, self.cfg.cvsfile_path)
            app.logger.info(" " + data_file + " ")
        except RuntimeError as runtimeError:
            app.logger.error("############################################################")
            app.logger.error(" " + runtimeError + " ")
            app.logger.error("############################################################")
            flash(message="error while downloading: " + self.cfg.cvsfile_path, category='error')
        except AttributeError as attributeError:
            app.logger.error("############################################################")
            app.logger.error(attributeError)
            app.logger.error("############################################################")
            flash(message="error after downloading: " + self.cfg.cvsfile_path, category='error')
        except Exception as exception:
            app.logger.error("############################################################")
            app.logger.error(exception)
            app.logger.error("############################################################")
            flash(message="error while downloading: " + self.cfg.cvsfile_path, category='error')
        finally:
            app.logger.info("")
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" downloaded FILE: "+self.cfg.cvsfile_name+" from "+self.cfg.url_src)
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" download - RKI [done] ")
            msg = "downloaded: " + self.cfg.cvsfile_path+" from "+self.cfg.url_src
            flash(msg)
        return self

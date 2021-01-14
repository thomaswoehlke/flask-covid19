from logging.config import dictConfig
from celery import Celery, states
from database import db, app, my_logging_comfig
from org.woehlke.covid19.who.who_service import WhoService
from org.woehlke.covid19.europe.europe_service import EuropeService

who_service = WhoService(db)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task(bind=True)
def who_run_update_task(self):
    self.update_state(state=states.STARTED)
    who_service.run_update()
    self.update_state(state=states.SUCCESS)
    result = "OK"
    return result


@celery.task(bind=True)
def alive_message_task(self):
    self.update_state(state=states.STARTED)
    app.logger.info("------------------------------------------------------------")
    app.logger.info(" Alive Message Received [OK] ")
    app.logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK"
    return result


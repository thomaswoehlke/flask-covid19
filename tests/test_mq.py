import sys
import subprocess
import covid19
import covid19_worker
from covid19 import app
from covid19.blueprints.application.application_workers import celery, run_mq


# ---------------------------------------------------------------------------------
#  MAIN
# ---------------------------------------------------------------------------------

if __name__ == '__main__':
    run_mq(app, celery)
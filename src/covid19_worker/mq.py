import sys
import subprocess
from covid19 import app
from covid19.blueprints.application.application_workers import celery
from covid19_worker import run_mq

#################################################################################################################
#
# MAIN
#
#################################################################################################################
if __name__ == '__main__':
    run_mq()

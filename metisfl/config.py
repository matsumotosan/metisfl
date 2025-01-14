import os

from pathlib import Path
from shutil import which, copyfile


METIS_WORKING_DIR = ".metisfl"
DRIVER_DIR_NAME = "driver"
CONTROLLER_DIR_NAME = "controller"
LEARNER_DIR_NAME = "learner_{}"
LEARNER_ID_FILE = "learner_id"


def get_project_home() -> str:
    path = os.path.join(Path.home(), METIS_WORKING_DIR)
    return _get_path_safe(path)


def get_driver_path() -> str:
    path = get_project_home()
    path = os.path.join(path, DRIVER_DIR_NAME)
    return _get_path_safe(path)


def get_controller_path():
    path = get_project_home()
    path = os.path.join(path, "controller")
    return _get_path_safe(path)


def get_learner_path(learner_id: int):
    path = get_project_home()
    path = os.path.join(path, "learner_{}".format(learner_id))
    return _get_path_safe(path)


def get_learner_id_fp(learner_id):
    learner_id_fp = get_learner_path(learner_id)
    _get_path_safe(learner_id_fp)
    return os.path.join(learner_id_fp, LEARNER_ID_FILE)


def _get_path_safe(path: str) -> str:
    if not os.path.exists(path):
        os.makedirs(path)
    return path

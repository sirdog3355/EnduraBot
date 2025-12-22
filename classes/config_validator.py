from dotenv import load_dotenv
import json
from utils.config_loader import SETTINGS_DATA
from utils.constants import GLOBAL_ALLOW_EMPTY
from classes.custom_exceptions import ConfigValidate

import logging

logger = logging.getLogger('endurabot.' + __name__)

class ConfigValidator():
    def __init__(self):
        pass

    def load_vars(self):
        pass
    
    def settings_data(self, vars_list):

        if not isinstance(vars_list, list):
            raise TypeError("Method settings_data of class ConfigValidator expects a list")

        existing_vars = []

        for key, _ in SETTINGS_DATA.items():
            existing_vars.append(key)

        missing_vars = []
        invalid_empty_vars = []

        for key in vars_list:
            if not key in existing_vars:
                missing_vars.append(key)
                continue

            if not key in GLOBAL_ALLOW_EMPTY and ( len(str(SETTINGS_DATA[key])) == 0 or SETTINGS_DATA[key] == "" or SETTINGS_DATA[key] == [] or SETTINGS_DATA[key] == {} ):
                invalid_empty_vars.append(key)

        if missing_vars and not invalid_empty_vars:
            raise ConfigValidate(f"Following variables missing but are expected to exist: {missing_vars}")
        elif invalid_empty_vars and not missing_vars:
            raise ConfigValidate(f"Following variables may not be empty: {invalid_empty_vars}")
        elif missing_vars and invalid_empty_vars:
            raise ConfigValidate(f"Variables must exist but do not: {missing_vars} and following variables DO exist but may not be empty: {invalid_empty_vars}")

from typing import List, get_origin

from environs import Env
from pydantic import BaseSettings
from pydantic.main import ModelMetaclass


class EnvironmentVariable(BaseSettings):
    SLACK_WEBHOOK: str
    MIN_AGE_LIMIT: int = 45


class Config(EnvironmentVariable):
    def __init__(self, *args, **kwargs):
        env = Env(eager=False)
        # env.read_env(os.path.join(self.PROJECT_DIR, ".envs/.pre.env"))
        get_env_var = lambda var_type, var_value: getattr(env, var_type)(var_value)
        env_var = {}
        for var_value, var_type in EnvironmentVariable.__annotations__.items():
            # pydantic object or list of objects
            if type(var_type) == ModelMetaclass or (get_origin(var_type) is list):
                data_type = "json"
            # primitive datatypes
            else:
                data_type: str = var_type.__name__
            env_var_value = get_env_var(data_type, var_value)
            if env_var_value:
                env_var[var_value] = env_var_value
        super().__init__(**env_var)


config = Config()

from pydantic import BaseSettings  #to declare environment variables; perform validation checks

class Settings(BaseSettings):
    database_hostname : str 
    database_port : str
    database_password : str
    database_name : str
    database_username : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int
    class Config:
        env_file = '.env'

setting = Settings()
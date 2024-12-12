from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

# abs_path_env = os.path.abspath("../../.env")
# env_template = os.path.abspath("../../.env.template")
load_dotenv()


class BaseServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class ApiV1Prefix(BaseModel):
    api_prefix: str = "/api/v1"


class MongoDBConfig(BaseServiceSettings):
    mongo_db_name: str
    mongo_host: str
    mongo_username: str
    mongo_password: str
    mongo_collection: str
    mongo_max_connections: int = 10
    mongo_min_connections: int = 3

    testing: bool = False
    test_name: str = "test_db"
    test_collection: str = "test_collection"

    @property
    def url(self) -> str:
        # mongodb://user:password@localhost:27017
        return f"mongodb://{self.mongo_username}:{self.mongo_password}@{self.mongo_host}:27017"


class Settings(BaseModel):
    api: ApiV1Prefix = ApiV1Prefix()
    mongoDB: MongoDBConfig = MongoDBConfig()
    logging: str = "DEBUG"


settings = Settings()

if __name__ == "__main__":
    print(settings.mongoDB.url)

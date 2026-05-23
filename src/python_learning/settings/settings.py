# BaseSettings merges multiple sources per field:
#   1. __init__ kwargs   2. env vars   3. .env file   4. secrets_dir files   5. defaults
# Each field is resolved independently; the first source that has it wins.

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

SECRETS_DIR = Path(__file__).resolve().parent / "secrets"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=SECRETS_DIR / ".env.secrets",
        secrets_dir=SECRETS_DIR,
        case_sensitive=False,
        extra="ignore",
    )

    # From env vars (prefix APP_): APP_NAME, APP_LOG_LEVEL, APP_PORT, APP_ALLOWED_HOSTS
    name: str = "default-app"
    log_level: str = "INFO"
    port: int = 8000                          # env vars are strings; coerced to int
    allowed_hosts: list[str] = []             # list/dict env vars expect JSON

    # From secrets_dir: files named `app_db_password` and `app_api_key`
    # (env_prefix applies to secret file names too).
    db_password: str = Field(default="<unset>")
    api_key: str = Field(default="<unset>")
    email_name: str = Field(default="<unset>")
    email_password: str = Field(default="<unset>")


def main() -> None:
    s = Settings()
    print(f"name           = {s.name}")
    print(f"log_level      = {s.log_level}")
    print(f"port           = {s.port!r}        (type: {type(s.port).__name__})")
    print(f"allowed_hosts  = {s.allowed_hosts}")
    print(f"db_password    = {s.db_password}")
    print(f"api_key        = {s.api_key}")
    print(f"email_name     = {s.email_name}")
    print(f"email_password = {s.email_password}")


if __name__ == "__main__":
    main()

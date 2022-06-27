import toml
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    """
    Configuration class to represent app config
    """
    stack_client_id: str = None
    stack_client_secret: str = None
    stack_api_key: str = None
    redis_host: str = None
    redis_password: str = None
    redis_port: int = None
    log_to_file: bool = False
    log_filename: str = None
    log_level: str = "DEBUG"

    @classmethod
    def from_toml_file(cls, file_path: str) -> 'Config':
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Config file path: {path} is invalid!")

        with path.open() as f:
            config = toml.load(f)

        config = {**config['API'], **config['database'], **config['logging']}
        config = {k: v for k, v in config.items() if v}
        return cls(**config)

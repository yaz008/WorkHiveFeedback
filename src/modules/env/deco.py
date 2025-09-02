from collections.abc import Callable, Iterable

from dotenv import load_dotenv

from modules.env.var import EnvVar


def env[EnvT: type](path: str) -> Callable[[EnvT], EnvT]:
    if not load_dotenv(path):
        raise FileNotFoundError(f'Unable to load \"{path}\" file')

    def decorator(cls: EnvT) -> EnvT:
        field_names: Iterable[str] = getattr(cls, '__annotations__')
        if not all(
            isinstance(getattr(cls, field_name), EnvVar) for field_name in field_names
        ):
            raise TypeError('Class with @env must only have fields of type EnvVar')
        return cls

    return decorator

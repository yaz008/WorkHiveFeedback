from modules.env import env, EnvVar


@env(path='.env')
class Env:
    TELEGRAM_BOT_TOKEN = EnvVar(
        name='TELEGRAM_BOT_TOKEN', pattern=r'^\d{1,10}:[A-Za-z0-9_-]{35}$'
    )

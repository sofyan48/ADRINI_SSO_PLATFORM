import os

class MetaFlaskEnv(type):
    def __init__(cls, name, bases, dict):
        super(MetaFlaskEnv, cls).__init__(name, bases, dict)
        prefix = dict.get('ENV_PREFIX', '')
        for key, value in os.environ.items():
            if not key.startswith(prefix):
                continue

            key = key[len(prefix):]

            if 'PASSWORD' in key:
                value = str(value)
            elif value.lower() in ('true', 'false'):
                value = True if value.lower() == 'true' else False
            elif '.' in value:
                try:
                    value = float(value)
                except ValueError:
                    pass
            else:
                try:
                    value = int(value)
                except ValueError:
                    pass
            setattr(cls, key, value)

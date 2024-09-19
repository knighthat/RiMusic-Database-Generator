class Json:

    def __init__(self, json: dict) -> None:
        self._json = json

    def __getitem__(self, key: str):
        return self._json[key]
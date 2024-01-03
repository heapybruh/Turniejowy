import pathlib

class Cogs():
    def get() -> list[pathlib.Path]:
        cogs = pathlib.Path("./cogs")
        return list(cogs.iterdir())
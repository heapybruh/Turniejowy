from .cogs import Cogs
from .config import Config
from .database import Team, Database
from .exceptions import NoConfig, WrongConfig, NoAdmin, TooSmallTeam, TeamNotFound, UserNotInDatabase, DatabaseNotConnected
from .embed import Embed

db: Database | None = None
cfg: Config | None = None
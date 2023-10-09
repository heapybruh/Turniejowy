from .cogs import Cogs
from .config import Config
from .database import Team, Database
from .exceptions import NoConfigException, WrongConfigException, NoAdminException, TooSmallTeamException, TeamNotFoundException
from .embed import Embed

db: Database | None = None
cfg: Config | None = None
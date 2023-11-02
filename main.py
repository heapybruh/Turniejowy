import utils
import os

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    utils.cfg = utils.Config()
    bot = utils.Bot()
    bot.run(utils.cfg.token, log_handler = None)
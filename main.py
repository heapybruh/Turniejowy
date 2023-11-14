import utils

if __name__ == "__main__":
    utils.cfg = utils.Config()
    bot = utils.Bot()
    bot.run(utils.cfg.token, log_handler = None)
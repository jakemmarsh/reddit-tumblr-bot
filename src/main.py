import ConfigParser
from bot import Bot

config = ConfigParser.RawConfigParser()
config.read('settings.cfg')

if __name__ == '__main__':
    bot = Bot(subreddit = config.get('reddit', 'subreddit'), timer = int(config.get('timer', 'seconds')))
    bot.run()
import bot, sched, time

def getLatest(sc, bot): 
    bot.process()
    sc.enter(60, 1, getLatest, (sc,))

if __name__ == '__main__':
    # bot connected to Tumblr and reddit APIs
    bot = bot.Bot()
    # scheduler to check for posts periodically
    s = sched.scheduler(time.time, time.sleep)
    
    # check for posts immediately, then once every 30 minutes
    bot.process()
    s.enter(1800, 1, getLatest, (s, bot))
    s.run()
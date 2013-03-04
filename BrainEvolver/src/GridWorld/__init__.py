from GridSimulation import *
import pickle


world = GridSimulation()
world.elapseTime(6000)
#pickle.dump(world, open('./bot.pkl', 'wb'))
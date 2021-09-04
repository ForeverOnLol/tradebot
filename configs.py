from environs import Env
env = Env
env.read_env()
mytelephone = env.str('mytelephon')
mypassword = env.str('mypassword')
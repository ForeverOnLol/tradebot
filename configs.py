from environs import Env
env = Env
env.read_env()
mytelephone = env.str("mytelephone")
mypassword = env.str('mypassword')
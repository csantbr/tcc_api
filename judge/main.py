from judge.app import Application
from judge.routers import routers

app = Application(routers=routers)

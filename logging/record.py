import os
import logging

curpath=os.path.dirname(__file__)
logpath=os.path.join(curpath,"log.txt")
logging.basicConfig(filename=logpath,level=logging.DEBUG)
logging.debug("test")

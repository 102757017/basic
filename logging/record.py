import os
import logging



curpath=os.path.dirname(__file__)
logpath=os.path.join(curpath,"log.txt")
#一旦某个模块在自己的代码里调用了 logging.basicConfig()，它就会为 root logger 配置好 handler。
#之后您在 main.py 中再次调用 basicConfig() 时，会静默地忽略您的这次调用。
logging.basicConfig(filename=logpath,level=logging.DEBUG)
logging.debug("test")



#强制重新配置
logging.basicConfig(filename=logpath,
                    level=logging.DEBUG,
                    force=True  # 这个参数会自动移除旧的 handlers 并应用新配置
                    )


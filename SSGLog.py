# -*- coding: utf-8 -*-
'''
Created on Sep 6, 2017

@author: Promod George
'''

import logging
from logging import handlers
loggers = {}
def setup_custom_logger(name):
    global loggers
    
    if loggers.get(name):
        return loggers.get(name)
    else:    
        formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    
        #handler = logging.StreamHandler()
        handler = logging.FileHandler(name+'.log', encoding="utf-8",mode='a', delay=False)
        handler.setFormatter(formatter)
    
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            handler = logging.handlers.RotatingFileHandler(name + '.log', maxBytes=(1048576*2), backupCount=70, encoding="utf-8", mode='a', delay=False)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.propagate = False
            loggers[name] = logger
        return logger
import os
import logging
import configparser

config = configparser.RawConfigParser()

HERE = os.path.dirname(__file__)

configfiles = [
    os.path.join(HERE, 'yourtickets.default.cfg'),
    os.path.join(HERE, 'yourtickets.test.cfg'),
    os.path.join(HERE, 'yourtickets.dev.cfg'),
    'ubuntu/yourtickets/yourtickets.live.cfg',
]

files_read = config.read(configfiles)

import logging

log_name = 'runtime.log'
LOGGER = logging.getLogger(__name__)
fh = logging.FileHandler(encoding='utf-8', mode='a', filename=log_name)
logging.basicConfig(handlers=[fh], format='[%(asctime)s %(levelname)s]<%(process)d> %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
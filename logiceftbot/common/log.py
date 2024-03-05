import logging
import logging.handlers as handlers
import sys
import os

log = logging.getLogger("LogicEFTBot")
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)
log.info("Logging all info to STDOUT. Disable by setting `unset BOT_VERBOSE` in bash.")

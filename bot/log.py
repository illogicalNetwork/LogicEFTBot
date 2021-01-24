import logging
import logging.handlers as handlers
import sys
import os

log = logging.getLogger("the_bot")
log.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)-15s | %(message)s")
log_handler = handlers.RotatingFileHandler(
    "bot.log",
    maxBytes=5000000,
    backupCount=3
)
log_handler.setLevel(logging.DEBUG)
log_handler.setFormatter(formatter)
log.addHandler(log_handler)

# TODO: turn this off before launching.
IS_VERBOSE = os.environ.get('BOT_VERBOSE')

if IS_VERBOSE:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.info("Logging all info to STDOUT. Disable by setting `unset BOT_VERBOSE` in bash.")
else:
    print("[info] All logs sent to `bot.log`. To log to stdout, open bash and `export BOT_VERBOSE=true`")

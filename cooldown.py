#!/usr/bin/python3
from bot.database import Database
import datetime
from datetime import timedelta
from bot.config import settings

cooldowns = {}

def check_cooldown(db: Database, channel_name: str) -> bool:
    """
    Returns true if the given channel is under cooldown.
    (API requests should be blocked to avoid overloading backend.)
    """
    if channel_name[0] == "#":
        channel_name = channel_name[1:]
        log.error("Someplace in the code is using channels with #.")
    cooldown_time = cooldowns[channel_name] if channel_name in cooldowns else None
    if cooldown_time is None:
        return False # no cooldown found.
    cooldown = db.get_cd(channel_name)
    if cooldown is None:
        cooldown = int(settings["default_cooldown"])
    return not datetime.datetime.utcnow() - cooldown_time > timedelta(seconds=cooldown)

def reset_cooldown(channel_name: str) -> None:
    """
    Updates the cooldown for the given channel, setting the last accessed
    time to now.
    """
    if channel_name[0] == "#":
        channel_name = channel_name[1:]
        log.error("Someplace in the code is using channels with #.")
    cooldowns[channel_name] = datetime.datetime.utcnow()

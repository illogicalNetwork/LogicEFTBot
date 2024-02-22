from dataclasses import dataclass
from typing import Optional


@dataclass
class ShardUpdate:
    """
    An update for a shard to give the master process.
    """

    status: str
    message: str
    requestedBroadcast: Optional[str] = None
    RPM: int = 0

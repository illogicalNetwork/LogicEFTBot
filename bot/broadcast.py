from typing import Callable, Optional
from threading import Event

class BroadcastCenter:
    BROADCAST_LISTENER: Optional[Callable[[str], None]]
    NEXT_EVENT: Event = Event()
    HAS_WAITER: bool = False
    IS_BROADCASTING: bool = False

    """
    Listen with the following broadcaster. Will run on the notifier's thread.
    """
    @classmethod
    def setListener(cls, fn: Callable[[str], None]) -> None
        cls.BROADCAST_LISTENER = fn
    
    """
    Broadcast a message to the listener. Awakens all waiting threads once their callbacks have been run.

    This can be called from ANY shard thread.
    """
    @classmethod
    def broadcast(cls, message: str) -> None
        cls.IS_BROADCASTING = True
        if not cls.HAS_WAITER:
            # no one is listening anyways...
            cls.IS_BROADCASTING = False
            return
        if cls.BROADCAST_LISTENER:
            cls.BROADCAST_LISTENER(message)
        # awaken all awaiting threads, and then
        # reset the Event.
        cls.NEXT_EVENT.set()
        cls.NEXT_EVENT.clear()
        cls.HAS_WAITER = False
        cls.IS_BROADCASTING = False

    """ 
    Sleep gracefully until the next event comes in. 
    Called from EXACTLY ONE listener.
    """
    @classmethod
    async def waitUntilNextEvent(cls) -> None:
        while cls.IS_BROADCASTING:
            time.sleep(0.1)
        cls.HAS_WAITER = True
        return await cls.NEXT_EVENT.wait()


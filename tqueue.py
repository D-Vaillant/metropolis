# Taken from https://github.com/TStand90/tcod_tutorial_v2/
import heapq
from typing import Any, List, NamedTuple, Iterable, Iterator

""" Ticks: 1 tick = .1 seconds """
""" Some principles:
All actions have variable tick costs, depending on skill in that.

Movement: 5 ft spaces.
"""

class Ticket(NamedTuple):
    time: int
    uid: int
    value: Any


class TurnQueue(Iterable[Ticket]):
    def __init__(
        self, time: int = 0, next_uid: int = 0, heap: Iterable[Ticket] = (),
    ) -> None:
        self.time = time
        self.next_uid = next_uid
        self.heap: List[Ticket] = list(heap)
        heapq.heapify(self.heap)

    def schedule(self, interval: int, value: Any) -> Ticket:
        """ Schedule and return a new ticket for `value` after `interval` time. """
        ticket = Ticket(self.time + interval, self.next_uid, value)
        heapq.heappush(self.heap, ticket)
        self.next_uid += 1
        return ticket

    def next(self) -> Ticket:
        """Pop and return the next scheduled ticket."""
        ticket = heapq.heappop(self.heap)
        self.time = ticket.time
        return ticket

    def __iter__(self) -> Iterator[Ticket]:
        """Returns an iterator that goes through all of the tickets in the queue.
        (We can add new tickets on the fly."""
        while self.heap:
            yield self.next()

    def __repr__(self) -> str:
        """Represents instance and tickets."""
        return f"{self.__class__.__name__}(time={self.time}, next_uid={self.next_uid}, heap={self.heap})"


# No idea why we need this.
__all__ = (
    "Ticket",
    "TurnQueue",
)

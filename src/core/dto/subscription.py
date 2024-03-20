from dataclasses import dataclass


@dataclass
class Subscription:
    id: int
    channel_id: str
    link: str

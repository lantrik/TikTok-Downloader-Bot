from typing import List


class Settings:
    """Bot Settings."""
    owners: List[int] = [
        1390707560 #lantrik
    ]

    debug: bool = False
    
    directories: List[str] = [
        "handlers/*",
        "handlers/panels/*",
    ]
from typing import List


class Settings:
    """Bot Settings."""
    debug: bool = False
    
    directories: List[str] = [
        "handlers/*",
        "handlers/panels/*",
    ]
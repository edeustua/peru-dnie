# Standard Library
from typing import Final

# Third Party Library
from attrs import define
from rich.console import Console


@define
class CliConfig:
    console: Final = Console(color_system="truecolor")
    DEBUG: Final = False


CLI_CONFIG: Final = CliConfig()

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, TypeVar

import pandas as pd
from rdetoolkit.models.rde2types import MetaType, RdeOutputResourcePath

T = TypeVar("T")


class IInputFileParser(ABC):
    """Abstract base class (interface) for input file parsers.

    This interface defines the contract that input file parser
    implementations must follow. The parsers are expected to read files
    from a specified path, parse the contents of the files, and provide
    options for saving the parsed data.

    Methods:
        read: A method expecting a file path and responsible for reading a file.

    Example implementations of this interface could be for parsing files
    of different formats like CSV, Excel, JSON, etc.

    """

    @abstractmethod
    def read(self, srcpath: Path) -> tuple[MetaType, pd.DataFrame]:
        """Read file."""
        raise NotImplementedError


class IMetaParser(ABC):
    """Abstract base class (interface) for meta information parsers.

    This interface defines the contract that meta information parser
    implementations must follow. The parsers are expected to save the
    constant and repeated meta information to a specified path.

    Method:
        save_meta: Saves the constant and repeated meta information to a specified path.
        parse: This method returns two types of metadata: const_meta_info and repeated_meta_info.

    """

    @abstractmethod
    def save_empty_meta(self, resource_paths: RdeOutputResourcePath) -> Any:
        """Read excel."""
        raise NotImplementedError

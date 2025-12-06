# tools/base_converter.py
from typing import List, Any

class BaseConverter:
    def to_int(self, value: Any) -> int:
        raise NotImplementedError

    def from_int(self, number: int) -> str:
        raise NotImplementedError

    def explain_to_int(self, value: Any) -> List[str]:
        try:
            return [f"Parsed '{value}' -> {self.to_int(value)} using {self.__class__.__name__}"]
        except Exception as e:
            return [f"Error explaining to_int: {e}"]

    def explain_from_int(self, number: int) -> List[str]:
        try:
            return [f"Converted {number} -> '{self.from_int(number)}' using {self.__class__.__name__}"]
        except Exception as e:
            return [f"Error explaining from_int: {e}"]

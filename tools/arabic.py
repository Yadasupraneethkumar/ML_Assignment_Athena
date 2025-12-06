# tools/arabic.py
from typing import List
from tools.base_converter import BaseConverter

ARABIC_INDIC = {"٠":0,"١":1,"٢":2,"٣":3,"٤":4,"٥":5,"٦":6,"٧":7,"٨":8,"٩":9}
REV_ARABIC_INDIC = {v:k for k,v in ARABIC_INDIC.items()}

class ArabicConverter(BaseConverter):
    def to_int(self, value) -> int:
        s = str(value).strip()
        if s == "0": return 0
        # accept ascii digits
        if all(ch.isdigit() for ch in s):
            return int(s)
        # accept Arabic-Indic digits
        out=0
        for ch in s:
            if ch not in ARABIC_INDIC:
                raise ValueError(f"Invalid Arabic-Indic digit: {ch}")
            out = out*10 + ARABIC_INDIC[ch]
        return out

    def from_int(self, number:int)->str:
        if number == 0:
            return REV_ARABIC_INDIC[0]
        if number < 0:
            raise ValueError("Negative not supported")
        s = str(number)
        return "".join(REV_ARABIC_INDIC[int(d)] for d in s)

    def explain_to_int(self, value)->List[str]:
        s=str(value).strip()
        return [f"Parsed Arabic string '{s}' -> integer {self.to_int(s)}."]

    def explain_from_int(self, number:int)->List[str]:
        return [f"Converted integer {number} -> Arabic-Indic '{self.from_int(number)}'."]

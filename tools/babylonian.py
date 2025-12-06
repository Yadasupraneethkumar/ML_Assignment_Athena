# tools/babylonian.py
from typing import List
from tools.base_converter import BaseConverter

class BabylonianConverter(BaseConverter):
    def _encode_place(self, v:int)->str:
        if v==0: return "0"
        tens = v//10; ones = v%10
        return "<"*tens + "Y"*ones

    def _decode_place(self, s:str)->int:
        s = s.strip()
        if s == "0": return 0
        return s.count("<")*10 + s.count("Y")

    def to_int(self, txt)->int:
        s=str(txt).strip()
        if s=="":
            raise ValueError("Empty")
        parts = s.split()
        total=0
        for p in parts:
            v = self._decode_place(p)
            if v>=60:
                raise ValueError("Place >=60")
            total = total*60 + v
        return total

    def from_int(self, number:int)->str:
        if number==0: return "0"
        if number<0: raise ValueError("Negative not supported")
        parts=[]
        n=number
        while n>0:
            parts.append(self._encode_place(n%60))
            n//=60
        return " ".join(reversed(parts))

    def explain_to_int(self, txt)->List[str]:
        steps=["Parse Babylonian (places space-separated, high->low)."]
        parts = str(txt).split()
        total=0
        for p in parts:
            v = self._decode_place(p)
            steps.append(f"Group '{p}' -> {v}; accumulate -> {total*60 + v}")
            total = total*60 + v
        steps.append(f"Final integer: {total}")
        return steps

    def explain_from_int(self, number:int)->List[str]:
        steps=[f"Convert {number} to base-60 groups."]
        if number==0:
            steps.append("Return '0'."); return steps
        parts=[]
        n=number; level=0
        while n>0:
            v=n%60; parts.append(v)
            steps.append(f"Level {level}: {v}")
            n//=60; level+=1
        parts=list(reversed(parts))
        steps.append(f"Groups (high->low): {parts}")
        steps.append(f"Representation: {' '.join(self._encode_place(x) for x in parts)}")
        return steps

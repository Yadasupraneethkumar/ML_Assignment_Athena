# tools/mayan.py
from typing import List
from tools.base_converter import BaseConverter

class MayanConverter(BaseConverter):
    def _encode_level(self, v:int)->str:
        if v==0: return "0"
        bars = v//5; dots = v%5
        return "-"*bars + "."*dots

    def _decode_level(self, s:str)->int:
        s = s.strip()
        if s=="0": return 0
        return s.count("-")*5 + s.count(".")

    def to_int(self, txt)->int:
        s=str(txt).strip().replace("\n","|")
        parts = [p for p in s.split("|") if p!='']
        if not parts: raise ValueError("Empty Mayan")
        # parts are top->bottom; bottom is least significant
        total=0
        # compute place multipliers: pos 0(bottom)=1, pos1=20, pos2=360 (18*20), pos3=7200 (18*20*20), etc.
        multipliers=[]
        for i in range(len(parts)-1, -1, -1):
            pos = len(parts)-1 - i
            if pos==0: multipliers.append(1)
            elif pos==1: multipliers.append(20)
            else:
                # for pos>=2 multiplier = 20 * 18 * 20^(pos-2) = 360 * 20^(pos-2)
                multipliers.append(360 * (20**(pos-2)))
        multipliers=list(reversed(multipliers))
        for p,m in zip(parts, multipliers):
            total += self._decode_level(p) * m
        return total

    def from_int(self, number:int)->str:
        if number==0: return "0"
        if number<0: raise ValueError("Negative not supported")
        # greedily produce levels bottom-up
        levels=[]
        n=number
        # produce bottom level first (units)
        while True:
            if len(levels)==0:
                # units
                v = n % 20
                levels.append(v)
                n//=20
            elif len(levels)==1:
                # twenties level
                v = n % 18  # because next multiplier is 18*20
                levels.append(v)
                n //= 18
            else:
                v = n % 20
                levels.append(v)
                n//=20
            if n==0:
                break
        # convert levels to strings top->bottom
        return "|".join(reversed([self._encode_level(v) for v in levels]))


    def explain_to_int(self, txt)->List[str]:
        s=str(txt).strip().replace("\n","|")
        parts = [p for p in s.split("|") if p!='']
        steps=[f"Parse Mayan '{s}' (top->bottom)."]
        multipliers=[]
        for i in range(len(parts)-1, -1, -1):
            pos = len(parts)-1 - i
            if pos==0: multipliers.append(1)
            elif pos==1: multipliers.append(20)
            else:
                multipliers.append(360 * (20**(pos-2)))
        multipliers=list(reversed(multipliers))
        total=0
        for p,m in zip(parts,multipliers):
            v = self._decode_level(p)
            steps.append(f"Level '{p}' -> {v} × {m} = {v*m}")
            total += v*m
        steps.append(f"Final integer: {total}")
        return steps

    def explain_from_int(self, number:int)->List[str]:
        steps=[f"Convert {number} to Mayan mixed-vigesimal levels."]
        if number==0:
            steps.append("Return '0'"); return steps
        # compute levels bottom-up
        levels=[]; n=number
        while True:
            if len(levels)==0:
                v = n % 20; levels.append(v); n//=20
            elif len(levels)==1:
                v = n % 18; levels.append(v); n//=18
            else:
                v = n % 20; levels.append(v); n//=20
            steps.append(f"Computed level {len(levels)-1} -> {v}")
            if n==0: break
        steps.append(f"Levels (bottom->top): {levels}")
        steps.append(f"Representation top->bottom: {'|'.join([self._encode_level(v) for v in reversed(levels)])}")
        return steps

# tools/yoruba.py
from typing import List
from tools.base_converter import BaseConverter

class YorubaConverter(BaseConverter):
    # base lexicon for small units; extended algorithmic representation for large numbers
    UNITS = {
        0:"odo",1:"ọ̀kan",2:"èjì",3:"ẹ̀ta",4:"ẹ̀rin",5:"àrún",6:"ẹ̀fà",7:"èje",8:"ẹ̀jọ",9:"ẹ̀sàn",
        10:"ẹ̀wá",11:"ọ̀kànlá",12:"èjìlá",13:"ẹ̀tàlá",14:"ẹ̀rìnlá",15:"mẹ́ẹ̀dógún",16:"mẹ́rìndínlógún",
        17:"mẹ́tàdínlógún",18:"mẹ́jìdínlógún",19:"mẹ́kàndínlógún",20:"ogún"
    }

    # powers: 20^1, 20^2, 20^3 ... with labels using generic numeric markers for algorithmic clarity
    POW_LABELS = {1:"ogún",2:"ogún²",3:"ogún³"}  # label strings only for human reading; we will construct algorithmically

    def _compose_small(self,n:int)->str:
        if n in self.UNITS:
            return self.UNITS[n]
        if n < 20:
            return str(n)
        if n < 100:
            tens = (n//20)*20
            rem = n - tens
            if rem == 0:
                return self.UNITS.get(tens, f"{tens}")
            # additive (e.g., 27 = ogún + èje)
            return f"{self.UNITS.get(tens,str(tens))} + {self._compose_small(rem)}"
        # fallback
        return str(n)

    def from_int(self, number:int)->str:
        if number == 0: return "odo"
        if number < 0: raise ValueError("Negative not supported")
        parts=[]
        n=number
        power=0
        while n>0:
            chunk = n % 20
            if chunk:
                # represent chunk at this power
                chunk_str = self._compose_small(chunk)
                if power == 0:
                    parts.append(chunk_str)
                else:
                    parts.append(f"{chunk_str} * (20^{power})")
            n//=20; power+=1
        # assemble high->low
        return " + ".join(reversed(parts))

    def to_int(self, text)->int:
        if isinstance(text,int): return text
        s=str(text).strip()
        if s.isdigit():
            return int(s)
        # accept algorithmic shapes we produce: parse "A + B * (20^k)" etc.
        s = s.replace(" ", "")
        if s == "odo": return 0
        # split by '+'
        parts = s.split("+")
        total=0
        for p in parts:
            if "*(" in p:
                # pattern chunk*(20^k) or similar
                left, right = p.split("*(")
                right = right.rstrip(")")
                if right.startswith("20^"):
                    k = int(right.split("^")[1])
                    # parse left small
                    val = self._parse_small(left)
                    total += val * (20**k)
                else:
                    raise ValueError("Unsupported pow format")
            else:
                total += self._parse_small(p)
        return total

    def _parse_small(self, s:str)->int:
        # handle small forms e.g., "ogún","ogún + èje"
        if s.isdigit():
            return int(s)
        if s=="odo": return 0
        # additive plus sign in small?
        if "+" in s:
            parts = s.split("+")
            return sum(self._parse_small(p) for p in parts)
        # direct lookup
        for k,v in self.UNITS.items():
            if v == s:
                return k
        # fallback error
        raise ValueError(f"Cannot parse Yoruba fragment '{s}'")

    def explain_from_int(self, number:int)->List[str]:
        steps=[f"Compose Yoruba for {number} using base-20 grouping."]
        steps.append(f"Result: {self.from_int(number)}")
        return steps

    def explain_to_int(self, text)->List[str]:
        steps=[f"Parse Yoruba expression '{text}'"]
        steps.append(f"Result: {self.to_int(text)}")
        return steps

# tools/inuktitut.py
from typing import List
from tools.base_converter import BaseConverter

SIMPLE = {
    0:"0",1:"atausiq",2:"marruk",3:"pingasut",4:"sisamat",5:"tallimat",
    6:"arvinillit",7:"hitamat",8:"innussat",9:"qulitinnasat",10:"qulit"
}

class InuktitutConverter(BaseConverter):
    def from_int(self, number:int)->str:
        if number==0: return "0"
        if number<0: raise ValueError("Negative not supported")
        parts=[]
        n=number
        power=0
        while n>0:
            chunk = n % 20
            if chunk:
                chunk_str = SIMPLE.get(chunk, str(chunk))
                if power==0:
                    parts.append(chunk_str)
                else:
                    parts.append(f"{chunk_str}*(20^{power})")
            n//=20; power+=1
        return " + ".join(reversed(parts))

    def to_int(self, text)->int:
        if isinstance(text,int): return text
        s=str(text).strip()
        if s.isdigit(): return int(s)
        if s=="0": return 0
        # parse expression like "A*(20^k) + B*(20^j) + ..." or small names
        s = s.replace(" ","")
        parts = s.split("+")
        total=0
        for p in parts:
            if "*(20^" in p:
                left, right = p.split("*(")
                powpart = right.rstrip(")")
                if powpart.startswith("20^"):
                    k = int(powpart.split("^")[1])
                    val = self._parse_small(left)
                    total += val * (20**k)
                else:
                    raise ValueError("Unsupported pow format")
            else:
                total += self._parse_small(p)
        return total

    def _parse_small(self, s:str)->int:
        if s.isdigit(): return int(s)
        for k,v in SIMPLE.items():
            if v==s:
                return k
        raise ValueError(f"Cannot parse Inuktitut fragment '{s}'")

    def explain_to_int(self, text)->List[str]:
        return [f"Parse Inuktitut '{text}' -> {self.to_int(text)}"]

    def explain_from_int(self, number:int)->List[str]:
        return [f"Construct Inuktitut algorithmic representation: {self.from_int(number)}"]

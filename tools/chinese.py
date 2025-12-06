# tools/chinese.py
from typing import List
from tools.base_converter import BaseConverter

NUM = {"零":0,"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9}
# units with ascending multipliers
UNITS = [("十",10),("百",100),("千",1000),("万",10**4),("億",10**8),("兆",10**12),
         ("京",10**16),("垓",10**20),("秭",10**24),("穰",10**28)]

UNIT_MAP = {k:v for k,v in UNITS}

class ChineseConverter(BaseConverter):
    def to_int(self, s)->int:
        s = str(s).strip()
        if s == "" or s == "零":
            return 0
        # recursive approach using largest unit splitting
        def parse_segment(seg):
            if seg=="":
                return 0
            # try large units from largest to smallest
            for u_sym, u_val in reversed(UNITS):
                if u_sym in seg:
                    parts = seg.split(u_sym)
                    left = parts[0]
                    right = u_sym.join(parts[1:])  # remainder after first unit
                    left_val = parse_segment(left)
                    if left_val == 0: left_val = 1
                    return left_val * u_val + parse_segment(right)
            # now no large unit; parse smaller digits sequence (thousands/hundreds tens)
            # handle possible '十','百','千' presence
            total=0
            num_buffer=0
            i=0
            while i < len(seg):
                ch = seg[i]
                if ch in NUM:
                    num_buffer = NUM[ch]; i+=1
                elif ch in UNIT_MAP:
                    unit_val = UNIT_MAP[ch]
                    if num_buffer==0:
                        num_buffer = 1
                    total += num_buffer * unit_val
                    num_buffer = 0; i+=1
                else:
                    raise ValueError(f"Invalid Chinese char: {ch}")
            total += num_buffer
            return total
        return parse_segment(s)

    def from_int(self, number:int)->str:
        if number==0: return "零"
        res=[]
        # iterate from largest unit down
        n = number
        for sym,val in reversed(UNITS):
            if n >= val:
                q = n // val
                n -= q*val
                if q == 1:
                    res.append(sym)
                else:
                    res.append(self.from_int(q) + sym)
        # handle last < 10000 part with 千 百 十
        if n >= 1000:
            q = n // 1000; n -= q*1000
            res.append(self._digit(q) + "千")
        if n >= 100:
            q = n // 100; n -= q*100
            res.append(self._digit(q) + "百")
        if n >= 10:
            q = n // 10; n -= q*10
            if q==1:
                res.append("十")
            else:
                res.append(self._digit(q) + "十")
        if n > 0:
            res.append(self._digit(n))
        return "".join(res)

    def _digit(self, n:int)->str:
        rev = {v:k for k,v in NUM.items()}
        return rev[n]

    def explain_to_int(self, s)->List[str]:
        steps = [f"Parse Chinese '{s}'."]
        val = self.to_int(s)
        steps.append(f"Computed integer {val}.")
        return steps

    def explain_from_int(self, number:int)->List[str]:
        return [f"Convert {number} -> {self.from_int(number)}"]

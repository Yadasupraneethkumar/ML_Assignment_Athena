# tools/roman.py
from typing import List
from tools.base_converter import BaseConverter

class RomanConverter(BaseConverter):
    BASE_TOKENS = [("M",1000),("CM",900),("D",500),("CD",400),("C",100),("XC",90),
              ("L",50),("XL",40),("X",10),("IX",9),("V",5),("IV",4),("I",1)]
    BASE_MAP = {k:v for k,v in BASE_TOKENS}

    # convert a 1..999 chunk to roman (standard)
    @staticmethod
    def _chunk_to_roman(n:int) -> str:
        if n <= 0:
            return ""
        out=[]
        rem=n
        for sym,val in RomanConverter.BASE_TOKENS:
            while rem >= val:
                out.append(sym)
                rem -= val
        return "".join(out)

    @staticmethod
    def _roman_chunk_to_int(s:str)->int:
        i=0; total=0
        while i < len(s):
            if i+1 < len(s) and s[i:i+2] in RomanConverter.BASE_MAP:
                total += RomanConverter.BASE_MAP[s[i:i+2]]
                i += 2
            elif s[i] in RomanConverter.BASE_MAP:
                total += RomanConverter.BASE_MAP[s[i]]
                i += 1
            else:
                raise ValueError(f"Invalid Roman symbol: {s[i]}")
        return total

    def from_int(self, number:int)->str:
        if number == 0:
            return "0"
        if number < 0:
            raise ValueError("Negative not supported for Roman")
        # split into groups of 1000 (base 1000 groups)
        groups=[]
        n=number
        while n>0:
            groups.append(n % 1000)
            n//=1000
        # groups[0] = lowest (units), groups[1]=thousands, etc.
        parts=[]
        for idx, chunk in enumerate(groups):
            if chunk==0:
                parts.append("") 
                continue
            roman_chunk = self._chunk_to_roman(chunk)
            if idx==0:
                parts.append(roman_chunk)
            else:
                # wrap chunk in idx parentheses to denote * (1000^idx)
                wrapped = roman_chunk
                for _ in range(idx):
                    wrapped = f"({wrapped})"
                parts.append(wrapped)
        # assemble from high->low
        return "".join(reversed([p for p in parts if p!=""]))

    def to_int(self, value:str)->int:
        if isinstance(value, int): return value
        s=str(value).strip()
        if s=="0": return 0
        # parse nested-parenthesis groups: find deepest parentheses first
        # We'll replace groups with their numeric value iteratively
        # function to compute one-level expression without parentheses: sequence of roman chunks concatenated
        def eval_no_paren(expr:str)->int:
            # expr may contain multiple roman chunks concatenated; parse left-to-right tokens
            # We accept concatenation of tokens that represent >0
            i=0; total=0
            while i < len(expr):
                # find next roman token substring (we match 2-chars first)
                if i+1 < len(expr) and expr[i:i+2] in self.BASE_MAP:
                    total += self.BASE_MAP[expr[i:i+2]]; i+=2
                elif expr[i] in self.BASE_MAP:
                    total += self.BASE_MAP[expr[i]]; i+=1
                else:
                    raise ValueError(f"Invalid Roman symbol: {expr[i]}")
            return total

        # iterative parentheses evaluation:
        while "(" in s:
            # find innermost '(' ... ')'
            start = s.rfind("(")
            end = s.find(")", start)
            if end==-1:
                raise ValueError("Unmatched '(' in Roman string")
            inner = s[start+1:end]
            val = eval_no_paren(inner)
            # inner value multiplied by 1000 for each layer we are closing (single paren = *1000)
            # But nesting is handled via iterative replacement: one pair corresponds to *1000
            val_str = str(val * 1000)
            # replace the "(inner)" with its numeric representation encoded again as roman-group? we'll encode numeric to plain integer placeholder
            # To handle nested parentheses, we will temporarily put a marker like "<N>" not valid roman char.
            s = s[:start] + f"#{val}#" + s[end+1:]
        # now s is combination of roman tokens and markers like #123#; parse left-to-right accumulating using multipliers
        total=0
        i=0
        while i < len(s):
            if s[i]=="#":
                j = s.find("#", i+1)
                num = int(s[i+1:j])
                # this number already is base chunk value; but when parentheses were used we multiplied by 1000 each time we replaced;
                # because we replaced inner (chunk) by its val*1000? Wait above we only replaced with #val#, so we must re-evaluate properly.
                # Simpler approach: when we replace inner we inserted #val#, but val was chunk value not multiplied. However we intended each parentheses to multiply by 1000.
                # Correction: above we used val = eval_no_paren(inner) then val_str = str(val*1000) but replaced with #val#. To reuse, we'll interpret '#' markers as group *1000^k based on nested occurrences.
                # To keep code simple and robust, restart and use a recursive parse instead.
                raise RuntimeError("Parser flow should not reach here (internal).")
            else:
                # fallback: parse as pure roman (no nested markers) using chunk parser
                return self._roman_chunk_to_int(s)
        return total

    # We'll implement a robust recursive parser instead of the above mixed approach
    def to_int(self, value):
        if isinstance(value, int): return value
        s=str(value).strip()
        if s=="0": return 0
        # recursive parse: if there is parentheses, split into segments of pattern ( ... ) or plain roman
        def parse_segment(seg):
            seg=seg.strip()
            if seg=="":
                return 0
            # if seg starts with '(' and ends with ')' (balanced), handle nesting depth
            if seg[0]=="(":
                # count how many leading '(' and corresponding trailing ')'
                # find matching pairs from left: treat nesting uniformly by handling from leftmost group
                # We'll parse left-to-right, whenever we see '( ... )' take inner and multiply by 1000, then continue
                i=0; total=0
                while i < len(seg):
                    if seg[i] == "(":
                        # find corresponding closing ')' for this opening
                        depth=0
                        j=i
                        for j in range(i, len(seg)):
                            if seg[j]=="(":
                                depth +=1
                            elif seg[j]==")":
                                depth -=1
                                if depth==0:
                                    break
                        if depth!=0:
                            raise ValueError("Unmatched parentheses in Roman")
                        inner = seg[i+1:j]
                        # parse inner which may itself contain nested parentheses
                        inner_val = parse_segment(inner)
                        # multiply by 1000 once for this pair
                        inner_val *= 1000
                        total += inner_val
                        i = j+1
                    else:
                        # plain roman letters until next '(' or end
                        k=i
                        while k < len(seg) and seg[k] != "(":
                            k+=1
                        total += self._roman_chunk_to_int(seg[i:k])
                        i = k
                return total
            else:
                # no leading '(' -> plain roman chunk (possibly with trailing parentheses)
                # handle sequential plain chunk followed by parentheses handled above
                # parse until first '(' or end
                if "(" in seg:
                    idx = seg.find("(")
                    left = seg[:idx]
                    rest = seg[idx:]
                    return self._roman_chunk_to_int(left) + parse_segment(rest)
                else:
                    return self._roman_chunk_to_int(seg)
        return parse_segment(s)

    def explain_to_int(self, value:str)->List[str]:
        steps = [f"Start parsing Roman '{value}'."]
        # We'll reuse to_int recursion and record steps simply by describing segments
        # For clarity provide coarse steps
        val = self.to_int(value)
        steps.append(f"Interpreted value = {val}. (Parentheses act as ×1000 per nesting level.)")
        return steps

    def explain_from_int(self, number:int)->List[str]:
        steps = [f"Start converting {number} to extended Roman (parentheses = ×1000 per nesting)."]
        if number==0:
            steps.append("Return '0' for zero.")
            return steps
        groups=[]
        n=number
        idx=0
        while n>0:
            chunk = n % 1000
            groups.append((idx, chunk))
            n//=1000; idx+=1
        for idx,chunk in reversed(groups):
            if chunk==0: continue
            r = self._chunk_to_roman(chunk)
            if idx==0:
                steps.append(f"Lowest group -> {chunk} -> {r}")
            else:
                wrapped = r
                for _ in range(idx):
                    wrapped = f"({wrapped})"
                steps.append(f"Group index {idx} -> {chunk} -> wrap -> {wrapped}")
        steps.append("Assemble groups high->low to final representation.")
        return steps

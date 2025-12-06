# tools/universal_converter.py
from tools.roman import RomanConverter
from tools.arabic import ArabicConverter
from tools.chinese import ChineseConverter
from tools.babylonian import BabylonianConverter
from tools.mayan import MayanConverter
from tools.yoruba import YorubaConverter
from tools.inuktitut import InuktitutConverter

class ConversionError(Exception): pass

class UniversalConverter:
    converters = {
        "roman": RomanConverter(),
        "arabic": ArabicConverter(),
        "chinese": ChineseConverter(),
        "babylonian": BabylonianConverter(),
        "mayan": MayanConverter(),
        "yoruba": YorubaConverter(),
        "inuktitut": InuktitutConverter()
    }

    def list_systems(self):
        return list(self.converters.keys())

    def _get(self,name:str):
        k=name.lower()
        if k not in self.converters:
            raise ConversionError(f"Unsupported system '{name}'")
        return self.converters[k]

    def convert(self, src, dst, value, explain:bool=False):
        sconv = self._get(src); dconv = self._get(dst)
        if explain:
            steps_to = sconv.explain_to_int(value)
            num = sconv.to_int(value)
            steps_from = dconv.explain_from_int(num)
            result = dconv.from_int(num)
            explanation = []
            explanation.extend(steps_to)
            explanation.append(f"Intermediate integer: {num}")
            explanation.extend(steps_from)
            return result, explanation
        else:
            num = sconv.to_int(value)
            return dconv.from_int(num)

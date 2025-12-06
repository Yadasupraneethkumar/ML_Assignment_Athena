import random
from tools.universal_converter import UniversalConverter

uc = UniversalConverter()
SYSTEMS = list(uc.converters.keys())


class ConvertPuzzle:
    """Puzzle asking user to convert system → system"""

    @staticmethod
    def generate():
        src, dst = random.sample(SYSTEMS, 2)
        n = random.randint(1, 9999)

        given = uc.convert("arabic", src, str(n))
        correct = uc.convert("arabic", dst, str(n))

        return {
            "type": "convert",
            "question": f"Convert {given} ({src}) → {dst}",
            "source_system": src,
            "target_system": dst,
            "arabic_value": n,
            "correct": correct
        }


class ExplainPuzzle:
    """Puzzle asking user to explain a numeral"""

    @staticmethod
    def generate():
        system = random.choice(SYSTEMS)
        n = random.randint(1, 4000)

        numeral = uc.convert("arabic", system, str(n))
        _, steps = uc.explain(system, "arabic", numeral)

        return {
            "type": "explain",
            "question": f"Explain how {numeral} ({system}) converts to Arabic.",
            "system": system,
            "numeral": numeral,
            "arabic_value": n,
            "steps": steps
        }


class MissingPuzzle:
    """Roman numeral fill-in puzzle"""

    @staticmethod
    def generate():
        n = random.randint(10, 999)
        numeral = uc.convert("arabic", "roman", str(n))

        i = random.randint(0, len(numeral) - 1)
        missing = numeral[i]
        masked = numeral[:i] + "_" + numeral[i + 1:]

        return {
            "type": "missing",
            "question": f"Fill in the missing Roman numeral: {masked}",
            "correct": missing,
            "full": numeral
        }


class PuzzleEngine:
    """Master puzzle dispatcher"""

    @staticmethod
    def generate():
        choice = random.choice(["convert", "explain", "missing"])

        if choice == "convert":
            return ConvertPuzzle.generate()

        if choice == "explain":
            return ExplainPuzzle.generate()

        return MissingPuzzle.generate()

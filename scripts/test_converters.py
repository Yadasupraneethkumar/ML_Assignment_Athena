# scripts/test_converters.py
import sys; sys.path.append(".")
from tools.universal_converter import UniversalConverter

def quick_test():
    u = UniversalConverter()
    print("Systems:", u.list_systems())

    test_values = [
        0, 1, 5, 10, 19, 27, 49, 99, 202, 999,
        4000, 12345, 67890123, 10**12 + 3456
    ]

    for n in test_values:
        try:
            # test arabic -> each system -> back -> compare
            a = u.convert("arabic","roman", str(n)) if n!=0 else u.convert("arabic","roman","0")
            back = u.convert("roman","arabic", a)  # roman->arabic expects string representation produced
            back_int = int(back) if isinstance(back, str) and back.isdigit() else u._get("arabic").to_int(back)
            print(f"AR {n} -> ROM '{a}' -> back {back_int} [{'OK' if back_int==n else 'MISMATCH'}]")
        except Exception as e:
            print(f"Error roundtrip arabic->{n}: {e}")

    # cross explain test
    try:
        res, steps = u.convert("arabic","mayan", "2025", explain=True)
        print("2025 -> mayan:", res)
        for s in steps: print(" -", s)
    except Exception as e:
        print("Explain error:", e)

if __name__=="__main__":
    quick_test()

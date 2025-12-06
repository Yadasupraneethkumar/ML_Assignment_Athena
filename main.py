from tools.universal_converter import UniversalConverter

def main():
    uc = UniversalConverter()

    print("\n=== UNIVERSAL NUMERAL CONVERTER ===")
    print("Available systems:")
    for s in uc.converters.keys():
        print(" -", s)

    src = input("\nEnter source system: ").strip().lower()
    dst = input("Enter destination system: ").strip().lower()
    value = input("Enter value to convert: ").strip()

    print("\n--- RESULT ---")
    try:
        result, steps = uc.explain(src, dst, value)
        print(f"Converted: {result}\n")
        print("Steps:")
        for s in steps:
            print(" -", s)
    except Exception as e:
        print("ERROR:", e)


if __name__ == "__main__":
    main()

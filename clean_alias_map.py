import json

INPUT_FILE = "alias_map.json"
OUTPUT_FILE = "alias_map_cleaned.json"


def resolve_final(name, alias_map):
    seen = set()

    while name in alias_map:
        if name in seen:
            break

        seen.add(name)
        next_name = alias_map[name]

        if next_name == name:
            break

        name = next_name

    return name


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        alias_map = json.load(f)

    cleaned = {}

    for alias, target in alias_map.items():
        final_target = resolve_final(target, alias_map)

        # remove self-mapping
        if alias == final_target:
            continue

        cleaned[alias] = final_target

    cleaned = dict(sorted(cleaned.items()))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print(f"Original mappings: {len(alias_map)}")
    print(f"Cleaned mappings: {len(cleaned)}")
    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
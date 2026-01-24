import xml.etree.ElementTree as ET
import icu
import os
import csv

def parse(path: str) -> list | None:
    tree = ET.parse(path)
    root = tree.getroot()

    territories = root.find("localeDisplayNames/territories")
    if territories is None:
        return

    TARGETS = ["EE", "LV", "LT"]
    result = {}

    for t in territories.findall("territory"):
        
        if (t_type := t.get("type")) in TARGETS:
            result[t_type] = t.text.lower()

        if len(result) == len(TARGETS):
            return [result[c] for c in TARGETS]

def in_alphabetical_order(words: list[str], language: str) -> bool:
    collator = icu.Collator.createInstance(icu.Locale(language))
    return sorted(words, key=collator.getSortKey) == words

def main():
    cldr_directory = "cldr-data/common/main"
    header = ["language", "estonia", "latvia", "lithuania", "in_order"]
    data = [header]

    for filename in os.listdir(cldr_directory):
        path = os.path.join(cldr_directory, filename)

        names = parse(path)
        if names is None:
            continue

        language = filename.removesuffix(".xml")
        in_order = in_alphabetical_order(names, language)
        data.append([language, *names, in_order])

    with open("results.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerows(data)

if __name__ == "__main__":
    main()

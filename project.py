import sys
import os
import json


def parse_arguments():
    if len(sys.argv) != 3:
        print("Użycie: program.exe pathFile1.x pathFile2.y")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    input_format = os.path.splitext(input_file)[1].lower()
    output_format = os.path.splitext(output_file)[1].lower()

    if input_format not in [".xml", ".json", ".yml", ".yaml"]:
        print(
            "Nieobsługiwany format wejściowy. Obsługiwane formaty: "
            ".xml, .json, .yml, .yaml"
        )
        sys.exit(1)

    if output_format not in [".xml", ".json", ".yml", ".yaml"]:
        print(
            "Nieobsługiwany format wyjściowy. Obsługiwane formaty: "
            ".xml, .json, .yml, .yaml"
        )
        sys.exit(1)

    return input_file, output_file, input_format, output_format


def load_json(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)


def save_json(data, file_path):
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving JSON file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    input_file, output_file, input_format, output_format = parse_arguments()
    print(
        f"Konwertowanie {input_file} ({input_format}) ",
        f"do {output_file} ({output_format})",
    )
    if input_format == ".json":
        data = load_json(input_file)
    print(f"Wczytano dane: {data}")
    if output_format == ".json":
        save_json(data, output_file)
    print(f"Pomyślnie przekonwertowano dane i zapisane do {output_file}")

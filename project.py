import sys
import os
import json
import yaml
import xml.etree.ElementTree as ET


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
        print(f"Błąd podczas wczytywania pliku JSON: {e}")
        sys.exit(1)


def save_json(data, file_path):
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Błąd podczas zapisywania pliku JSON: {e}")
        sys.exit(1)


def load_yaml(file_path):
    try:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        return data
    except yaml.YAMLError as e:
        print(f"Błąd podczas wczytywania pliku YAML: {e}")
        sys.exit(1)


def save_yaml(data, file_path):
    try:
        with open(file_path, "w") as file:
            yaml.safe_dump(data, file)
    except Exception as e:
        print(f"Błąd podczas zapisywania pliku YAML: {e}")
        sys.exit(1)


def load_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
    except ET.ParseError as e:
        print(f"Błąd podczas wczytywania pliku XML: {e}")
        sys.exit(1)


def save_xml(data, file_path):
    try:
        tree = ET.ElementTree(data)
        tree.write(file_path)
    except Exception as e:
        print(f"Błąd podczas zapisywania pliku XML: {e}")
        sys.exit(1)


def log_error(e):
    with open("error_log.txt", "a") as log_file:
        log_file.write(str(e) + "\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            input_file, output_file, input_format, output_format = parse_arguments()
            print(
                f"Konwertowanie {input_file} ({input_format}) ",
                f"do {output_file} ({output_format}) rozpoczęte",
            )

            if input_format == ".json":
                data = load_json(input_file)
                print(f"Wczytano dane: {data}")
            elif input_format in [".yaml", ".yml"]:
                data = load_yaml(input_file)
                print(f"Wczytano dane: {data}")
            elif input_format == ".xml":
                data = load_xml(input_file)
                print(f"Wczytano dane: {data}")

            if output_format == ".json":
                save_json(data, output_file)
                print(
                    "Dane zostały pomyślnie przekonwertowane ",
                    f"i zapisane do {output_file}",
                )
            elif output_format in [".yaml", ".yml"]:
                save_yaml(data, output_file)
                print(
                    "Dane zostały pomyślnie przekonwertowane ",
                    f"i zapisane do {output_file}",
                )
            elif output_format == ".xml":
                save_xml(data, output_file)
                print(
                    "Dane zostały pomyślnie przekonwertowane ",
                    f"i zapisane do {output_file}",
                )
            print("Konwertowanie plików zakończone")
        except Exception as e:
            log_error(e)
            print(f"Wystąpił błąd: {e}")
    else:
        print(
            "Brak argumentów! "
            "Proszę podać ścieżki do plików wejściowych i wyjściowych."
        )
    input("Naciśnij enter aby wyjść...")

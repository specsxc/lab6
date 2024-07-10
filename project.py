import sys
import os
import json
import yaml
from collections import OrderedDict
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


def parse_arg():
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
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        print(f"Błąd podczas wczytywania pliku JSON: {e}")
        log_error(e)
        sys.exit(1)


def save_json(data, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Błąd podczas zapisywania pliku JSON: {e}")
        log_error(e)
        sys.exit(1)


def load_yaml(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
        return data
    except yaml.YAMLError as e:
        print(f"Błąd podczas wczytywania pliku YAML: {e}")
        log_error(e)
        sys.exit(1)


def save_yaml(data, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            yaml.safe_dump(data, file, allow_unicode=True)
    except Exception as e:
        print(f"Błąd podczas zapisywania pliku YAML: {e}")
        log_error(e)
        sys.exit(1)


def load_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
    except ET.ParseError as e:
        print(f"Błąd podczas wczytywania pliku XML: {e}")
        log_error(e)
        sys.exit(1)


def save_xml(data, file_path):
    try:
        root = dict_to_xml("root", data)
        xml_str = ET.tostring(root, encoding="utf-8")
        parsed_str = minidom.parseString(xml_str)
        pretty_xml_as_string = parsed_str.toprettyxml(indent="  ", encoding="utf-8")

        with open(file_path, "wb") as file:
            file.write(pretty_xml_as_string)
    except Exception as e:
        print(f"Błąd podczas zapisywania pliku XML: {e}")
        log_error(e)
        sys.exit(1)


def dict_to_xml(tag, value):
    elem = ET.Element(tag)
    if isinstance(value, dict):
        for key, val in value.items():
            child = dict_to_xml(key, val)
            elem.append(child)
    elif isinstance(value, list):
        for item in value:
            child = dict_to_xml(tag, item)
            elem.append(child)
    else:
        elem.text = str(value)
    return elem


def xml_to_dict(element):
    if len(element) == 0:
        return element.text
    result = OrderedDict()
    for child in element:
        if child.tag not in result:
            result[child.tag] = xml_to_dict(child)
        else:
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(xml_to_dict(child))
    return result


def log_error(e):
    with open("error_log.txt", "a") as log_file:
        log_file.write(str(e) + "\n")


yaml.add_representer(
    OrderedDict, lambda dumper, data: dumper.represent_dict(data.items())
)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            input_file, output_file, input_format, output_format = parse_arg()
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
                data = xml_to_dict(load_xml(input_file))
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

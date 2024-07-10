import sys
import os


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


if __name__ == "__main__":
    input_file, output_file, input_format, output_format = parse_arguments()
    print(
        f"Konwertowanie {input_file} ({input_format}) ",
        f"do {output_file} ({output_format})",
    )

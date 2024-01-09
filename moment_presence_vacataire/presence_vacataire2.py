import argparse
from module2 import process_data2, generate_html, read_ics_file, write_html_file

def main():
    parser = argparse.ArgumentParser(description="Générateur d'emploi du temps à partir de fichiers .ics")
    parser.add_argument("--input-file", nargs='+', required=True, help="Fichiers iCalendar (e.g., file1.ics file2.ics)")
    parser.add_argument("--output-file", required=True, help="Chemin du fichier HTML de sortie")

    args = parser.parse_args()

    all_data = []
    for file_path in args.input_file:
        ics_content = read_ics_file(file_path)
        all_data.append(ics_content)

    events = []
    for data in all_data:
        events.extend(process_data2(data))

    html_content = generate_html(events)
    write_html_file(html_content, args.output_file)

    print("Page HTML générée avec succès.")

if __name__ == "__main__":
    main()

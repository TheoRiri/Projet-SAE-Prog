import argparse
from module_2 import extract_data, process_data, generate_html
from typing import List

def main():
    """
    Fonction principale pour créer un emploi du temps à partir de fichiers .ics.

    Arguments en ligne de commande :
    --input-file : Liste des fichiers .ics.
    --output-file : Répertoire de sortie pour la page web.
    """
    parser = argparse.ArgumentParser(description="Créer un emploi du temps à partir de fichiers .ics")
    parser.add_argument("--input-file", nargs="+", help="Liste des fichiers .ics")
    parser.add_argument("--output-file", help="Répertoire de sortie pour la page web")
    args = parser.parse_args()

    data: List[str] = extract_data(args.input_file)

    allowed_teachers: List[str] = ["NAUDIN MATHIEU", "SAVIN DYLAN", "MIELON WILLIAMS", "TRICHARD PASCALE", "CHARTIER MAXIME", "BOUCHEAU TONY", "TRAPARIC DAVID", "HOUMEAU BERTRAND", "DEWAILLY SERGE"]

    processed_data: List[dict] = process_data(data, allowed_teachers)

    generate_html(processed_data, args.output_file)

if __name__ == "__main__":
    main()

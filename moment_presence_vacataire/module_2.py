from datetime import datetime
import pytz
from typing import List, Optional, Dict

def extract_data(file_list: List[str]) -> List[str]:
    """
    Extrait les données à partir d'une liste de chemins de fichiers.

    Paramètres :
    - file_list (List[str]): Liste des chemins de fichiers.

    Retourne :
    - List[str]: Liste contenant le contenu de chaque fichier.
    """
    data = []
    for file_path in file_list:
        with open(file_path, 'r') as file:
            data.append(file.read())
    return data

def process_data(data: List[str], allowed_teachers: Optional[List[str]] = None) -> List[Dict[str, str]]:
    """
    Traite les données du calendrier pour extraire les informations pertinentes.

    Paramètres :
    - data (List[str]): Liste contenant les données du calendrier.
    - allowed_teachers (Optional[List[str]]): Liste des noms d'enseignants autorisés.

    Retourne :
    - List[Dict[str, str]]: Données traitées contenant les informations sur les événements.
    """
    processed_data = []

    for ics_content in data:
        lines = ics_content.split('\n')
        events = []
        current_event: Optional[Dict[str, str]] = None

        for line in lines:
            if line.startswith('BEGIN:VEVENT'):
                current_event = {}
            elif line.startswith('SUMMARY:'):
                current_event['summary'] = line.split(':')[-1]
            elif line.startswith('LOCATION:'):
                current_event['location'] = line.split(':')[-1]
            elif line.startswith('DESCRIPTION:'):
                description_parts = line.split('\\n')
                if len(description_parts) >= 4:
                    current_event['group'] = description_parts[2].strip()
                    current_event['teacher'] = description_parts[3].strip()
            elif line.startswith('DTSTART:'):
                start_time = line.split(':')[-1]
                utc_start_time = datetime.strptime(start_time, '%Y%m%dT%H%M%SZ')
                paris_timezone = pytz.timezone('Europe/Paris')
                local_start_time = utc_start_time.replace(tzinfo=pytz.utc).astimezone(paris_timezone)
                current_event['start_time'] = local_start_time.strftime('%H:%M')
                current_event['date'] = local_start_time.strftime('%d-%m-%Y')
            elif line.startswith('DTEND:'):
                end_time = line.split(':')[-1]
                utc_end_time = datetime.strptime(end_time, '%Y%m%dT%H%M%SZ')
                paris_timezone = pytz.timezone('Europe/Paris')
                local_end_time = utc_end_time.replace(tzinfo=pytz.utc).astimezone(paris_timezone)
                current_event['end_time'] = local_end_time.strftime('%H:%M')
            elif line.startswith('END:VEVENT'):
                assert current_event is not None
                events.append(current_event)

        for event in events:
            if event.get('summary', '') and (allowed_teachers is None or event.get('teacher', '') in allowed_teachers):
                summary = event.get('summary', '')
                start_time = event.get('start_time', '')
                end_time = event.get('end_time', '')
                processed_data.append(event)

    processed_data.sort(key=lambda x: datetime.strptime(x['date'], '%d-%m-%Y'))

    return processed_data

def generate_html(data: List[Dict[str, str]], output_file: str) -> None:
    """
    Génère un fichier HTML basé sur les données traitées.

    Paramètres :
    - data (List[Dict[str, str]]): Données traitées contenant les informations sur les événements.
    - output_file (str): Chemin du fichier HTML de sortie.
    """
    html_content = """
    <html>
    <head>
        <title>Tableau de</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            h1, footer {
                background-color: #001F3F; /* Bleu foncé */
                color: white;
                padding: 10px;
                text-align: center;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin-top: 20px;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #001F3F; /* Bleu foncé */
                color: white;
            }
        </style>
    </head>
    <body>
        <h1>Emploi du temps Des Vacataires</h1>
        <table>
            <tr>
                <th>Date</th>
                <th>Horaire de début</th>
                <th>Horaire de fin</th>
                <th>Nom du cours</th>
                <th>Salle</th>
                <th>Groupe</th>
                <th>Enseignant</th>
            </tr>
    """

    for event in data:
        html_content += f"""
            <tr>
                <td>{event['date']}</td>
                <td>{event['start_time']}</td>
                <td>{event['end_time']}</td>
                <td>{event.get('summary', '')}</td>
                <td>{event.get('location', '')}</td>
                <td>{event.get('group', '')}</td>
                <td>{event.get('teacher', '')}</td>
            </tr>
        """

    html_content += """
        </table>
        <footer>Projet Moinereau Luka et Riviere Théo</footer>
    </body>
    </html>
    """

    with open(output_file + 'emploi.html', 'w') as file:
        file.write(html_content)

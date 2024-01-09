from datetime import datetime
import pytz

def read_ics_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def process_data2(data):
    events = []
    current_event = None

    lines = data.split('\n')
    for line in lines:
        if line.startswith('BEGIN:VEVENT'):
            current_event = {}
        elif line.startswith('SUMMARY:'):
            current_event['summary'] = line.split(':')[-1]
        elif line.startswith('LOCATION:'):
            current_event['location'] = line.split(':')[-1]
        elif line.startswith('DESCRIPTION:'):
            description_parts = line.split('\\n')
            group, teacher = extract_group_and_teacher(description_parts)
            current_event['group'] = group
            current_event['teacher'] = teacher 
        elif line.startswith('DTSTART:'):
            start_time = line.split(':')[-1]
            utc_start_time = datetime.strptime(start_time, '%Y%m%dT%H%M%SZ')
            paris_timezone = pytz.timezone('Europe/Paris')
            local_start_time = utc_start_time.replace(tzinfo=pytz.utc).astimezone(paris_timezone)
            current_event['start_time'] = local_start_time.strftime('%H:%M')
            current_event['date'] = local_start_time.strftime('%d/%m/%Y')
        elif line.startswith('DTEND:'):
            end_time = line.split(':')[-1]
            utc_end_time = datetime.strptime(end_time, '%Y%m%dT%H%M%SZ')
            paris_timezone = pytz.timezone('Europe/Paris')
            local_end_time = utc_end_time.replace(tzinfo=pytz.utc).astimezone(paris_timezone)
            current_event['end_time'] = local_end_time.strftime('%H:%M')
        elif line.startswith('END:VEVENT'):
            events.append(current_event)

    return events

def extract_group_and_teacher(description_parts):
    group = "Inconnu"
    teacher = "Inconnu"
    teachers = [
        "CAMARDA FLORENT", "BONNETON ISABELLE", "JACQUET MICHELE", "REY LAURENT",
        "VERDON VINCENT", "COUDERC TURQ SEBASTIEN", "LAIZE ANNE SOPHIE", "LAUNAY FREDERIC",
        "VUATTOUX NESE", "COIRAULT PATRICK", "BOUCHEAU TONY", "TREMBLAIS BENOIT",
        "CHARTIER MAXIME", "FAVRY BRUNO", "HOUMEAU BERTRAND", "TRICHARD PASCALE",
        "DEROUICHE ABD EL KAOUI", "NAUDIN MATHIEU","SAVIN DYLAN","MIELON WILLIAMS"


    ]

    for part in description_parts:
        if 'RT' in part:
            group = part.strip()
        elif any(name in part for name in teachers):
            teacher = part.strip()
    return group, teacher


def generate_html(events):
    html_content = "<html><head><title>Emploi du Temps</title></head><body>"
    html_content += "<table border='1'>"
    html_content += "<tr><th>Date</th><th>Heure de debut</th><th>Heure de fin</th><th>Resume</th><th>Lieu</th><th>Groupe</th><th>Enseignant</th></tr>"
    
    for event in events:
        html_content += f"<tr><td>{event.get('date', 'N/A')}</td>"
        html_content += f"<td>{event.get('start_time', 'N/A')}</td>"
        html_content += f"<td>{event.get('end_time', 'N/A')}</td>"
        html_content += f"<td>{event.get('summary', 'N/A')}</td>"
        html_content += f"<td>{event.get('location', 'N/A')}</td>"
        html_content += f"<td>{event.get('group', 'N/A')}</td>"
        html_content += f"<td>{event.get('teacher', 'N/A')}</td></tr>"
    
    html_content += "</table></body></html>"
    return html_content

def write_html_file(content, output_file):
    with open(output_file, "w") as file:
        file.write(content)
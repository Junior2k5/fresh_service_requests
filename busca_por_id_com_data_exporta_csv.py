import requests
import csv
from requests.auth import HTTPBasicAuth
from datetime import datetime

# Configurações
TOKEN = "API_TOKEN"
BASE_URL = "URL_BASE"
START_DATE = "2025-02-01T00:00:00Z"
TARGET_STATUSES = {2, 3, 4, 5}  # Filtrar por status Open (2), Pending (3), Resolved (4), e Closed (5)

# Função para consultar tickets com filtros desejados
def get_filtered_tickets():
    page = 1
    filtered_tickets = []
    while True:
        url = f"{BASE_URL}/tickets?per_page=100&page={page}&updated_since={START_DATE}"
        response = requests.get(url, auth=HTTPBasicAuth(TOKEN, 'X'), headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        tickets = response.json().get('tickets', [])

        # Filtra tickets por status desejado e data de atualização
        for ticket in tickets:
            if ticket['status'] in TARGET_STATUSES:
                created_at = datetime.strptime(ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                if created_at > datetime.strptime("2025-02-01", "%Y-%m-%d"):
                    filtered_tickets.append({
                        'id': ticket['id'],
                        'created_at': ticket['created_at'],
                        'updated_at': ticket['updated_at'],
                        'due_by': ticket['due_by'],
                        'status': ticket['status'],
                        'source': ticket['source'],
                        'priority': ticket['priority'],
                        'type': ticket['type']
                    })

        if not tickets:
            break

        page += 1

    return filtered_tickets

def main():
    # Obter tickets filtrados
    filtered_tickets = get_filtered_tickets()

    # Salvar tickets em um arquivo CSV
    with open('filtered_tickets.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'created_at', 'updated_at', 'due_by', 'status', 'source', 'priority', 'type'])
        writer.writeheader()
        for ticket in filtered_tickets:
            writer.writerow(ticket)

    print("CSV file 'filtered_tickets.csv' created successfully.")

if __name__ == "__main__":
    main()
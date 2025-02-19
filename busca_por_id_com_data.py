import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

# Configurações
TOKEN = "API_TOKEN"
BASE_URL = "URL_BASE"
START_DATE = "2025-02-01T00:00:00Z"
TARGET_STATUSES = {2, 4, 5}  # Filtrar por status Open (2), Resolved (4), e Closed (5)


# Função para consultar tickets com filtros desejados
def get_filtered_ticket_ids():
    page = 1
    ticket_ids = []
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
                    ticket_ids.append(ticket['id'])

        if not tickets:
            break

        page += 1

    return ticket_ids


def main():
    # Obter IDs dos tickets filtrados
    ticket_ids = get_filtered_ticket_ids()
    for ticket_id in ticket_ids:
        print(ticket_id)


if __name__ == "__main__":
    main()
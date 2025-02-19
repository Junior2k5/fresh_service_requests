import requests
from requests.auth import HTTPBasicAuth
import csv

# Configurações
EMAIL = "EMAIL@EMAIL.COM"
TOKEN = "API_TOKEN"
BASE_URL = "URL_BASE"
CSV_FILE = "tickets.csv"  # Nome do arquivo CSV


# Função para consultar tickets por e-mail
def get_tickets_by_email(email):
    url = f"{BASE_URL}/tickets/?email={email}"
    response = requests.get(url, auth=HTTPBasicAuth(TOKEN, 'X'), headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    return response.json().get('tickets', [])


# Função para obter detalhes do departamento
def get_department_details(department_id):
    url = f"{BASE_URL}/departments/{department_id}"
    response = requests.get(url, auth=HTTPBasicAuth(TOKEN, 'X'), headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    return response.json().get('department', {})


# Função para obter detalhes do grupo
def get_group_details(group_id):
    url = f"{BASE_URL}/groups/{group_id}"
    response = requests.get(url, auth=HTTPBasicAuth(TOKEN, 'X'), headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    return response.json().get('group', {})


# Função para obter detalhes do requisitante
def get_requester_details(requester_id):
    url = f"{BASE_URL}/requesters/{requester_id}"
    response = requests.get(url, auth=HTTPBasicAuth(TOKEN, 'X'), headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    return response.json().get('requester', {})


# Função para obter detalhes do workspace
def get_workspace_details(workspace_id):
    url = f"{BASE_URL}/workspaces/{workspace_id}"
    response = requests.get(url, auth=HTTPBasicAuth(TOKEN, 'X'), headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    return response.json().get('workspace', {})


# Função para obter detalhes do agente
def get_agent_details(agent_id):
    url = f"{BASE_URL}/agents/{agent_id}"
    response = requests.get(url, auth=HTTPBasicAuth(TOKEN, 'X'), headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    return response.json().get('agent', {})


def main():
    # Mapas para resolver os valores para suas descrições
    status_map = {
        2: "Open",
        3: "Pending",
        4: "Resolved",
        5: "Closed"
    }

    priority_map = {
        1: "Low",
        2: "Medium",
        3: "High",
        4: "Urgent"
    }

    source_map = {
        1: "Email",
        2: "Portal",
        3: "Phone",
        4: "Chat",
        5: "Feedback widget",
        6: "Yammer",
        7: "AWS Cloudwatch",
        8: "Pagerduty",
        9: "Walkup",
        10: "Slack"
    }

    # Consulta tickets por e-mail
    tickets = get_tickets_by_email(EMAIL)

    # Preparar o arquivo CSV
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # Escrever o header do CSV
        writer.writerow([
            "Ticket Subject", "Ticket ID", "Status", "Priority", "Source",
            "Created At", "Updated At", "Type", "Due By",
            "Department Name", "Group Name", "Requester Name",
            "Workspace Name", "Responder Name"
        ])

        # Iterar sobre tickets e escrever cada um como uma linha no CSV
        for ticket in tickets:
            status_description = status_map.get(ticket['status'], "Unknown")
            priority_description = priority_map.get(ticket['priority'], "Unknown")
            source_description = source_map.get(ticket['source'], "Unknown")

            department_details = get_department_details(ticket['department_id'])
            group_details = get_group_details(ticket['group_id'])
            requester_details = get_requester_details(ticket['requester_id'])
            workspace_details = get_workspace_details(ticket['workspace_id'])
            agent_details = get_agent_details(ticket['responder_id'])

            # Escrever dados do ticket no CSV
            writer.writerow([
                ticket['subject'],
                ticket['id'],
                status_description,
                priority_description,
                source_description,
                ticket['created_at'],
                ticket['updated_at'],
                ticket['type'],
                ticket['due_by'],
                department_details.get('name', ''),
                group_details.get('name', ''),
                f"{requester_details.get('first_name', '')} {requester_details.get('last_name', '')}",
                workspace_details.get('name', ''),
                f"{agent_details.get('first_name', '')} {agent_details.get('last_name', '')}"
            ])


if __name__ == "__main__":
    main()
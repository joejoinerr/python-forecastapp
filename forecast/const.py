"""Constant values across the Forecast library"""

ENDPOINT = 'https://api.forecast.it/api'

# All known API paths
API_PATH = {
    'person_id': '/v1/persons/{id}',
    'persons': '/v1/persons',
    'task_id': '/v2/tasks/{id}',
    'task_company_id': '/v2/tasks/company_task_id/{id}',
    'tasks': '/v2/tasks',
}

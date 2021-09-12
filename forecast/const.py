"""Constant values across the Forecast library"""

ENDPOINT = 'https://api.forecast.it/api'

# All known API paths
API_PATH = {
    'milestone_id': '/v1/projects/{project_id}/milestones/{milestone_id}',
    'milestones': '/v1/projects/{project_id}/milestones',
    'person_id': '/v1/persons/{id}',
    'persons': '/v1/persons',
    'project_id': '/v1/projects/{id}',
    'project_company_id': '/v1/projects/company_project_id/{id}',
    'projects': '/v1/projects',
    'role_id': '/v1/roles/{id}',
    'roles': '/v1/roles',
    'task_id': '/v2/tasks/{id}',
    'task_company_id': '/v2/tasks/company_task_id/{id}',
    'tasks': '/v2/tasks',
}

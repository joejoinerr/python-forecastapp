"""Constant values across the Forecast library"""

ENDPOINT = 'https://api.forecast.it/api'

# All known API paths
API_PATH = {
    'label_id': '/v1/labels/{id}',
    'labels': '/v1/labels',
    'milestone_id': '/v1/projects/{project_id}/milestones/{milestone_id}',
    'milestones': '/v1/projects/{project_id}/milestones',
    'non_project_time': '/v1/non_project_time',
    'non_project_time_id': '/v1/non_project_time/{id}',
    'person_id': '/v1/persons/{id}',
    'persons': '/v1/persons',
    'project_id': '/v1/projects/{id}',
    'project_team': '/v1/projects/{id}/team',
    'project_company_id': '/v1/projects/company_project_id/{id}',
    'projects': '/v1/projects',
    'role_id': '/v1/roles/{id}',
    'roles': '/v1/roles',
    'task_id': '/v2/tasks/{id}',
    'task_company_id': '/v2/tasks/company_task_id/{id}',
    'tasks': '/v2/tasks',
    'workflow_id': '/v1/projects/{project_id}/workflow_columns/{column_id}',
    'workflow': '/v1/projects/{project_id}/workflow_columns',
}

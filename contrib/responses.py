forbidden_response = {
    'detail': 'Not authenticated',
}

not_found_entity_response = {
    'detail': 'Not found',
}

conflict_response = {
    'detail': 'Conflict',
}

unprocessable_entity_response = {
    'detail': [{'loc': ['body', 'field'], 'msg': 'Invalid field type', 'type': 'value_error'}]
}

internal_server_error_response = ('Internal Server Error',)

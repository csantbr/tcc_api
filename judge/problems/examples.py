problem_in_example = {
    'name': 'Hello World',
    'description': 'Faça um hello world',
    'data_entry': '',
    'entry_description': 'Este problema não possui nenhuma entrada.',
    'data_output': 'SGVsbG8gV29ybGQhXG4=',
    'output_description': "Você deve imprimir a mensagem 'Hello World!' e em seguida o final de linha.",
}

problem_out_example = {
    **problem_in_example,
    'created_at': '2022-06-15 14:25:37.766011+00:00',
}

problem_collection_response_example = {'results': [problem_out_example]}

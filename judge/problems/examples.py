problem_in_example = {
    "name": "Soma de Números",
    "description": "Faça um programa que some dois números inteiros.",
    "data_entries": [
        "MSAy",      # 1 2
        "MyA0",      # 3 4
        "NSA2",      # 5 6
        "MTAgMjA="   # 10 20
    ],
    "entry_description": "A entrada consiste de dois números inteiros separados por espaço.",
    "data_outputs": [
        "Mw==",      # 3\n
        "Nw==",      # 7\n
        "MTE=",      # 11\n
        "MzA="       # 30\n
    ],
    "output_description": "Imprima a soma dos dois números seguida de uma quebra de linha.",
}

problem_out_example = {
    **problem_in_example,
    "created_at": "2022-06-15 14:25:37.766011+00:00",
}

problem_collection_response_example = {"results": [problem_out_example]}

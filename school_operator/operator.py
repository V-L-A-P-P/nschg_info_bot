import json


def change_operator(operator_id):
    with open('school_operator/operator_id.json', 'w', encoding='utf8') as f:
        json.dump(operator_id, f, ensure_ascii=False, indent=4)


def get_operator_id():
    try:
        with open('school_operator/operator_id.json', 'r', encoding='utf8') as f:
            operator_id = json.load(f)
        if operator_id is None:
            raise FileNotFoundError("Добавьте оператора!")
        else:
            return operator_id
    except FileNotFoundError:
        print("Error: файл с id операторов отсутствует")
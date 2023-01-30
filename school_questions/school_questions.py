import json
import keyboards


def add_new_question(question, answer, category):
    questions = load_questions()
    if category in list(questions.keys()):
        questions[category][question] = answer
    else:
        questions[category] = {question : answer}

    with open('school_questions/questions.json', 'w', encoding='utf8') as f:
        print(json.dump(questions, f, ensure_ascii=False, indent=4))

def load_questions():
    try:
        with open('school_questions/questions.json', 'r', encoding='utf8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: Файл с вопросами и ответами отсутствует")


def find_answer_by_text(question):
    questions_dict = load_questions()
    for category in questions_dict:
        for key in questions_dict[category]:
            if key == question:

                return "❓" + key + "\n\n✅" + questions_dict[category][key]
    return None


def find_answer_by_num(num, category):
    questions_dict = load_questions()
    count = 0
    for key in questions_dict[category]:
        count += 1
        if count == num:
            return "❓" + key + "\n\n✅" + questions_dict[category][key]

    return None


def get_questions_list():
    questions_dict = load_questions()
    questions_list = []
    for category in questions_dict:
        for key in questions_dict[category]:
            questions_list.append(key)
    return questions_list


def get_str_questions(category):
    questions = list(load_questions()[category].keys())
    questions_str = ""
    for count in range(0, len(questions)):
        questions_str += ' \n\n' + keyboards.client_kb.convert_nums_to_buttons(str(count + 1)) + questions[count]
    print(questions_str)
    return questions_str



import math

NUMBERS_DICT = {
    "ноль": 0, "один": 1, "одна": 1, "два": 2, "две": 2,
    "три": 3, "четыре": 4, "пять": 5, "шесть": 6, "семь": 7,
    "восемь": 8, "девять": 9, "десять": 10, "одиннадцать": 11,
    "двенадцать": 12, "тринадцать": 13, "четырнадцать": 14,
    "пятнадцать": 15, "шестнадцать": 16, "семнадцать": 17,
    "восемнадцать": 18, "девятнадцать": 19, "двадцать": 20,
    "тридцать": 30, "сорок": 40, "пятьдесят": 50,
    "шестьдесят": 60, "семьдесят": 70, "восемьдесят": 80,
    "девяносто": 90, "сто": 100     ###词典
}

OPERATIONS = {
    "плюс": "+", "минус": "-", "умножить": "*", "разделить": "/",
    "в_степени": "**", "синус": "math.sin", "косинус": "math.cos", "тангенс": "math.tan"
}

CONSTANTS = {"пи": math.pi, "е": math.e}
EXTRA_WORDS = {"на", "от"}  # pass

def preprocess_input(input_text):
    combined_operators = {
        "в степени": "в_степени"
    }
    for phrase, replacement in combined_operators.items():
        input_text = input_text.replace(phrase, replacement)
    return input_text

def parse_tokens(tokens):
    total = 0
    for token in tokens:
        if token in NUMBERS_DICT:
            total += NUMBERS_DICT[token]
        else:
            raise ValueError(f"слова с неизвестными числами: {token}")
    return total

def convert_to_math(tokens):
    expression = []
    i = 0

    while i < len(tokens):
        word = tokens[i]

        # 忽略无关词
        if word in EXTRA_WORDS:
            i += 1
            continue

        # 操作符处理
        if word in OPERATIONS:
            if word in ["синус", "косинус", "тангенс"]:
                func = OPERATIONS[word]
                i += 1
                param_tokens = []
                while i < len(tokens) and tokens[i] not in OPERATIONS:
                    param_tokens.append(tokens[i])
                    i += 1
                param = convert_to_math(param_tokens)
                expression.append(f"{func}({param})")
            else:
                expression.append(OPERATIONS[word])
            i += 1
        # 常量处理
        elif word in CONSTANTS:
            expression.append(str(CONSTANTS[word]))
            i += 1
        # 数字处理
        else:
            num_tokens = []
            while i < len(tokens) and tokens[i] not in OPERATIONS:
                num_tokens.append(tokens[i])
                i += 1
            expression.append(str(parse_tokens(num_tokens)))

    return " ".join(expression)

def interpret_expression(input_text):# 预处理输入
    input_text = preprocess_input(input_text)

    tokens = input_text.split()
    return convert_to_math(tokens)

def calculate_expression(expression):
    try:
        return eval(expression)
    except ZeroDivisionError:
        raise ZeroDivisionError("ошибка деления на ноль")
    except Exception as e:
        raise ValueError(f"Произошла ошибка при вычислении выражения: {e}")

def run_calculator():     ###主程序
    print("Добро пожаловать в калькулятор на русском языке!")
    print("Вы можете использовать числа, операторы и тригонометрические функции.")
    print("Введите 'выход' для завершения.")

    while True:
        user_input = input("\nВведите выражение: ").strip().lower()
        if user_input == "выход":
            print("Спасибо за использование калькулятора! До свидания.")
            break

        try:
            math_expression = interpret_expression(user_input)
            print(f"Сгенерированное выражение: {math_expression}")
            result = calculate_expression(math_expression)
            print(f"Результат: {result}")
        except Exception as error:
            print(f"Ошибка: {error}")

if __name__ == "__main__":
    run_calculator()
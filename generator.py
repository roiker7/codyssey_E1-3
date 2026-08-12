import json
import re
import shutil
from pathlib import Path

# 저장 형태 통일성을 유지 하기 위한 함수
def save_json_keep_rows(filename, data):
    # 먼저 일반적인 예쁜 JSON 형태로 변환
    text = json.dumps(data, ensure_ascii=False, indent=4)

    # 숫자 패턴
    number = r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?"

    # 숫자만 들어있는 배열을 찾는 패턴
    pattern = re.compile(
        r"\[\s*(" + number + r"(?:\s*,\s*" + number + r")*)\s*\]"
    )

    # 세로로 풀린 숫자 배열을 한 줄로 바꾸는 함수
    def replace_array(match):
        nums = re.findall(number, match.group(1))
        return "[" + ", ".join(nums) + "]"

    # 숫자 배열만 한 줄로 압축
    text = pattern.sub(replace_array, text)

    # 파일 저장
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
        f.write("\n")
    print("JSON파일에 저장 완료")

def validate_size(n: int):
    """
    패턴 크기 검증 함수
    십자가 패턴은 중앙 행/열이 필요하므로 홀수 N만 허용합니다.
    """
    if not isinstance(n, int):
        raise TypeError("N은 int 타입이어야 합니다.")

    if n < 3:
        raise ValueError("N은 3 이상이어야 합니다.")

    if n % 2 == 0:
        raise ValueError("N은 홀수여야 합니다. 예: 5, 7, 13, 25")


def generate_x_pattern(n: int):
    """
    N x N X 패턴 생성
    두 대각선 위치만 1.0, 나머지는 0.0
    """
    validate_size(n)

    pattern = []

    for row in range(n):
        line = []
        for col in range(n):
            if row == col or row + col == n - 1:
                line.append(1.0)
            else:
                line.append(0.0)
        pattern.append(line)

    return pattern


def generate_cross_pattern(n: int):
    """
    N x N 십자가(+) 패턴 생성
    중앙 행과 중앙 열만 1.0, 나머지는 0.0
    """
    validate_size(n)

    center = n // 2
    pattern = []

    for row in range(n):
        line = []
        for col in range(n):
            if row == center or col == center:
                line.append(1.0)
            else:
                line.append(0.0)
        pattern.append(line)

    return pattern


def get_next_pattern_index(patterns: dict, n: int):
    """
    기존 patterns 안에서 size_N_번호 형식의 마지막 번호를 찾고,
    다음 번호를 반환합니다.

    예:
    size_5_1, size_5_2가 있으면 다음 번호는 3
    """
    max_index = 0

    pattern_key_regex = re.compile(rf"^size_{n}_(\d+)$")

    for key in patterns.keys():
        match = pattern_key_regex.match(key)
        if match:
            index = int(match.group(1))
            max_index = max(max_index, index)

    return max_index + 1


def add_patterns_to_json(json_path, n):
    """
    data.json 파일에 X 패턴과 십자가 패턴을 자동 추가합니다.

    추가 형식:
    "size_N_번호": {
        "input": [...],
        "expected": "x" 또는 "+"
    }
    """
    validate_size(n)

    path = Path(json_path)

    if not path.exists():
        raise FileNotFoundError(f"{json_path} 파일을 찾을 수 없습니다.")

    # JSON 읽기
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    # patterns 키가 없으면 생성
    if "patterns" not in data:
        data["patterns"] = {}

    patterns = data["patterns"]

    # 기존 번호 다음부터 추가
    next_index = get_next_pattern_index(patterns, n)

    x_key = f"size_{n}_{next_index}"
    cross_key = f"size_{n}_{next_index + 1}"

    # X 패턴 추가
    patterns[x_key] = {
        "input": generate_x_pattern(n),
        "expected": "x"
    }

    # 십자가 패턴 추가
    patterns[cross_key] = {
        "input": generate_cross_pattern(n),
        "expected": "+"
    }

    # JSON 저장
    save_json_keep_rows("data.json", data)



# 테스트 코드
if __name__ == "__main__":
    result = add_patterns_to_json("data.json", 7)
    print(result)
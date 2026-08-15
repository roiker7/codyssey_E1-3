import json
import re
from pathlib import Path

# 저장 형태 통일성을 유지하기 위한 함수 
def save_json_keep_rows(filename, data):
    text = json.dumps(data, ensure_ascii=False, indent=4)
    number = r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?"
    pattern = re.compile(r"\[\s*(" + number + r"(?:\s*,\s*" + number + r")*)\s*\]")

    def replace_array(match):
        nums = re.findall(number, match.group(1))
        return "[" + ", ".join(nums) + "]"

    text = pattern.sub(replace_array, text)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
        f.write("\n")
    print(f"** {filename} 파일에 필터 및 패턴 저장 완료 **")


def validate_size(n: int):
    if not isinstance(n, int):
        raise TypeError("N은 int 타입이어야 합니다.")
    if n < 3:
        raise ValueError("N은 3 이상이어야 합니다.")
    if n % 2 == 0:
        raise ValueError("N은 홀수여야 합니다. 예: 5, 7, 13, 25")


def generate_x_pattern(n: int):
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
    max_index = 0
    pattern_key_regex = re.compile(rf"^size_{n}_(\d+)$")

    for key in patterns.keys():
        match = pattern_key_regex.match(key)
        if match:
            index = int(match.group(1))
            max_index = max(max_index, index)

    return max_index + 1

# data.json 파일에 해당 크기(N)의 필터와 테스트 패턴을 동시에 추가
def make_patterns_filters(json_path: str, n: int):
  
    validate_size(n)
    path = Path(json_path)

    if not path.exists():
        raise FileNotFoundError(f"{json_path} 파일을 찾을 수 없습니다.")

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    # 1. 필터(filters) 영역 업데이트
    # 형태: "size_N": { "x": [[...]], "cross": [[...]] }
    if "filters" not in data:
        data["filters"] = {}

    filter_key = f"size_{n}"
    
    # 이미 해당 크기의 필터가 생성되어 있어도 최신 행렬로 덮어씁니다.
    data["filters"][filter_key] = {
        "x": generate_x_pattern(n),
        "cross": generate_cross_pattern(n)
    }

    # 2. 패턴(patterns) 영역 업데이트
    # 형태: "size_N_번호": { "input": [[...]], "expected": "x" }
    if "patterns" not in data:
        data["patterns"] = {}

    patterns = data["patterns"]
    next_index = get_next_pattern_index(patterns, n)

    x_key = f"size_{n}_{next_index}"
    cross_key = f"size_{n}_{next_index + 1}"

    patterns[x_key] = {
        "input": generate_x_pattern(n),
        "expected": "x"
    }

    patterns[cross_key] = {
        "input": generate_cross_pattern(n),
        "expected": "+"
    }

    # 3. 변경된 딕셔너리를 JSON 파일로 저장
    save_json_keep_rows(json_path, data)


# 실행 테스트
if __name__ == "__main__":
    add_patterns_and_filters_to_json("data.json", 7)
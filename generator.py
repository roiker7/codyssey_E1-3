import json
import os
import re

def generate_cross_pattern(n: int, offset_r: int = 0, offset_c: int = 0) -> list:
    """N x N 크기의 2차원 Cross(+) 패턴 생성"""
    matrix = [[0.0] * n for _ in range(n)]
    center_r = (n // 2) + offset_r
    center_c = (n // 2) + offset_c

    for i in range(n):
        for j in range(n):
            if i == center_r or j == center_c:
                matrix[i][j] = 1.0
    return matrix


def generate_x_pattern(n: int, dx: int = 0, dy: int = 0) -> list:
    """N x N 크기의 2차원 X 패턴 생성 (치우친 패턴 지원)"""
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            cond1 = (j - dy) == (i - dx)
            cond2 = (i - dx) + (j - dy) == n - 1
            if cond1 or cond2:
                matrix[i][j] = 1.0
    return matrix


def save_clean_2d_json(data: dict, filepath: str):
    """2차원 행렬의 각 행을 한 줄로 깔끔하게 정렬하여 JSON 저장"""
    # 저장 대상 폴더가 없으면 자동 생성
    dirname = os.path.dirname(filepath)
    if dirname:
        os.makedirs(dirname, exist_ok=True)

    json_str = json.dumps(data, indent=4, ensure_ascii=False)
    
    # 1차원 리스트 요소 [0.0, 0.0, ...] 내부의 불필요한 줄바꿈을 제거하여 가로 한 줄로 압축
    formatted_json = re.sub(
        r'\[\s*([0-9\.,\s-]+?)\s*\]',
        lambda m: '[' + re.sub(r'\s+', ' ', m.group(1)).strip() + ']',
        json_str
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(formatted_json)


def create_pattern_dataset(n: int, folder_name: str = "auto_generator_data", output_file: str = None) -> str:
    """N x N 2차원 패턴 세트를 지정된 폴더(auto_generator_data)에 저장하고 파일 경로 반환"""
    if output_file is None:
        filename = f"generated_data_{n}.json"
    else:
        filename = output_file

    # auto_generator_data 폴더 내부 경로 생성
    filepath = os.path.join(folder_name, filename)

    dataset = {
        "meta": {
            "version": "1.0",
            "type": "json"
        },
        "filters": {
            f"size_{n}": {
                "cross": generate_cross_pattern(n),
                "x": generate_x_pattern(n)
            }
        },
        "patterns": {
            f"size_{n}_1": {
                "input": generate_cross_pattern(n),
                "expected": "+"
            },
            f"size_{n}_2": {
                "input": generate_x_pattern(n),
                "expected": "x"
            },
            f"size_{n}_3": {
                "input": generate_x_pattern(n, dx=1, dy=0),
                "expected": "x"
            }
        }
    }

    save_clean_2d_json(dataset, filepath)
    return filepath
import json

def generate_cross_pattern(n: int, offset_r: int = 0, offset_c: int = 0) -> list:
    """N x N 크기의 Cross(+) 패턴 생성"""
    matrix = [[0.0] * n for _ in range(n)]
    center_r = (n // 2) + offset_r
    center_c = (n // 2) + offset_c

    for i in range(n):
        for j in range(n):
            if i == center_r or j == center_c:
                matrix[i][j] = 1.0
    return matrix


def generate_x_pattern(n: int, dx: int = 0, dy: int = 0) -> list:
    """N x N 크기의 X 패턴 생성 (dx, dy 이동으로 치우친 패턴 지원)"""
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            cond1 = (j - dy) == (i - dx)
            cond2 = (i - dx) + (j - dy) == n - 1
            if cond1 or cond2:
                matrix[i][j] = 1.0
    return matrix


def create_pattern_dataset(n: int, output_file: str = None) -> str:
    """N 크기에 맞춘 기준 필터 및 테스트 패턴 세트를 생성하여 JSON 저장"""
    if output_file is None:
        output_file = f"generated_data_{n}.json"

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
                "input": generate_x_pattern(n, dx=1, dy=0),  # 치우친 X 패턴 테스트
                "expected": "x"
            }
        }
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

    return output_file
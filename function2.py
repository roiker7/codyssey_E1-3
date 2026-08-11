import json
import time
from loads import validate_and_process_patterns

def result_print(cross_score, X_score, pattern_name, answers):
    # 계산 결과 평가
    if abs(cross_score - X_score) < 1e-9:
        result = "UNDECIDED"
    elif cross_score > X_score:
        result = "Cross"
    else:
        result = "X"

    # 정답 여부
    if answers == result:
        p_or_f = "PASS" 
    else:
        p_or_f = "FAIL"

    # 패턴 분석 출력
    print(f"--[{pattern_name}]--")
    print(f"Cross 점수: {cross_score}")
    print(f"X 점수: {X_score}")
    print(f"판정: {result} | expected: {answers} | {p_or_f}")


def standard(input_val: str):
    LABEL_MAP = {
        '+': 'Cross',
        'cross': 'Cross',
        'x': 'X'
    }
    if not input_val:
        return input_val
    cleaned = input_val.strip().lower()
    return LABEL_MAP.get(cleaned, input_val)


def flatten_2d_to_1d(matrix_2d: list) -> list:
    """2차원 배열을 N^2 길이를 가지는 1차원 배열로 변환 (메모리 평탄화)"""
    return [val for row in matrix_2d for val in row]


def MAC_2D(pat_m, c_f, X_f, size):
    """[최적화 전] 2차원 배열 이중 루프 MAC 연산"""
    total_time = 0 
    count = 0
    for i in range(10):
        start = time.perf_counter()
        sum1, sum2, count = 0.0, 0.0, 0
        for y in range(size):
            for x in range(size):
                sum1 += pat_m[y][x] * c_f[y][x]  
                sum2 += pat_m[y][x] * X_f[y][x]  
                count += 1        
        end = time.perf_counter()
        total_time += (end - start) * 1000  # ms 변환

    ave_time = total_time / 10
    return sum1, sum2, ave_time, count


def MAC_1D(pat_1d, c_f_1d, X_f_1d, size):
    """[최적화 후] 1차원 배열 단일 루프 MAC 연산 (메모리 접근 단순화)"""
    total_size = size * size
    total_time = 0 
    count = 0
    for i in range(10):
        start = time.perf_counter()
        sum1, sum2, count = 0.0, 0.0, 0
        for idx in range(total_size):
            sum1 += pat_1d[idx] * c_f_1d[idx]
            sum2 += pat_1d[idx] * X_f_1d[idx]
            count += 1
        end = time.perf_counter()
        total_time += (end - start) * 1000  # ms 변환

    ave_time = total_time / 10
    return sum1, sum2, ave_time, count


def calculate(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    filters = data.get("filters", {})
    patterns = data.get("patterns", {})

    # 성능 비교 데이터 저장용 딕셔너리
    perf_data = {}

    print("\n\n\n#---------------------------------------")
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    print("#---------------------------------------")

    for pattern_key, pattern_val in patterns.items():
        p_size = int(pattern_key.split('_')[1])
        input_matrix = pattern_val.get("input")
        label = standard(pattern_val.get("expected"))

        for filter_key, filter_val in filters.items():
            f_size = int(filter_key.split('_')[1]) 
            cross_matrix = filter_val.get("cross")
            X_matrix = filter_val.get("x")

            if p_size == f_size:
                # 1. 최적화 전 (2D) 연산
                sum1, sum2, time_2d, count = MAC_2D(input_matrix, cross_matrix, X_matrix, f_size)
                
                # 2. 최적화 후 (1D) 연산
                input_1d = flatten_2d_to_1d(input_matrix)
                cross_1d = flatten_2d_to_1d(cross_matrix)
                X_1d = flatten_2d_to_1d(X_matrix)
                _, _, time_1d, _ = MAC_1D(input_1d, cross_1d, X_1d, f_size)

                # 패턴 분석 결과 즉시 출력
                result_print(sum1, sum2, pattern_key, label)

                # 성능 수집 (2D vs 1D)
                size_str = f"{f_size}x{f_size}"
                if size_str not in perf_data:
                    perf_data[size_str] = {"times_2d": [], "times_1d": [], "count": count}
                perf_data[size_str]["times_2d"].append(time_2d)
                perf_data[size_str]["times_1d"].append(time_1d)

    print("\n\n\n#--------------------------------------------------------------------")
    print("# [3] 최적화 전/후 성능 분석 비교 (평균/10회)")
    print("#--------------------------------------------------------------------")
    print(f"{'크기':<8}{'2D 시간(ms)':<15}{'1D 시간(ms)':<15}{'성능 개선율':<12}{'연산 횟수':<8}")
    print("--------------------------------------------------------------------")

    for size_str, info in perf_data.items():
        avg_2d = sum(info["times_2d"]) / len(info["times_2d"])
        avg_1d = sum(info["times_1d"]) / len(info["times_1d"])
        
        # 성능 개선율 (%) 계산
        speedup = ((avg_2d - avg_1d) / avg_2d * 100) if avg_2d > 0 else 0
        op_count = info["count"]
        
        print(f"{size_str:<8}{avg_2d:<15.4f}{avg_1d:<15.4f}{speedup:>6.2f}%      {op_count:<8}")


def main():
    file_name = "data.json"
    validate_and_process_patterns(file_name)
    calculate(file_name)


if __name__ == "__main__":
    main()
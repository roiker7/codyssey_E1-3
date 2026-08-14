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
    p_flag ,f_flag = 0, 0 # 통과가 몇개인지 세기 위한 변수
    if answers == result:
        p_or_f = "PASS" 
        p_flag = 1
    else:
        p_or_f = "FAIL"
        f_flag = 1

    # 패턴 분석 출력
    print(f"--[{pattern_name}]--")
    print(f"Cross 점수: {cross_score}")
    print(f"X 점수: {X_score}")
    print(f"판정: {result} | expected: {answers} | {p_or_f}")

    return p_flag ,f_flag


def standard(input_val: str):
    LABEL_MAP = {
        '+': 'Cross',
        'cross': 'Cross',
        'x': 'X'
        #'o': 'O','circle'
    }
    if not input_val:
        return input_val
    cleaned = input_val.strip().lower()
    return LABEL_MAP.get(cleaned, input_val)


def MAC(pat_m, c_f, X_f, size):
    total_time = 0 
    count = 0
    for i in range(10):
        start = time.perf_counter()
        sum1, sum2, count = 0, 0, 0
        for y in range(size):
            for x in range(size):
                sum1 += pat_m[y][x] * c_f[y][x]  
                sum2 += pat_m[y][x] * X_f[y][x]  
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

    # 성능 데이터 저장용 딕셔너리
    perf_data = {}

    print("\n\n\n#---------------------------------------")
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    print("#---------------------------------------")

    Fail_case = []
    p_cnt ,f_cnt = 0 ,0
    for pattern_key, pattern_val in patterns.items():
        p_size = int(pattern_key.split('_')[1])
        input_matrix = pattern_val.get("input")
        label = standard(pattern_val.get("expected")) # 정규화된 라벨

        for filter_key, filter_val in filters.items():
            f_size = int(filter_key.split('_')[1]) 
            cross_matrix = (filter_val.get("cross")) # 정규화된 라벨
            X_matrix = filter_val.get("x") # 정규화된 라벨

            if p_size == f_size:
                sum1, sum2, ave_time, count = MAC(input_matrix, cross_matrix, X_matrix, f_size)
                
                # 패턴 분석 결과 즉시 출력 및 결과 요약 데이터 수집
                a ,b = result_print(sum1, sum2, pattern_key, label)
                p_cnt += a
                f_cnt += b
                if b:
                    Fail_case.append(pattern_key)
                # 성능 분석 출력을 위한 데이터 수집
                size_str = f"{f_size}x{f_size}"
                if size_str not in perf_data:
                    perf_data[size_str] = {"times": [], "count": count}
                perf_data[size_str]["times"].append(ave_time)
        else:
            print("필터와 패턴의 크기가 일치하지 않습니다. 분석을 건너뜁니다.")

    print("\n\n\n#---------------------------------------")
    print("# [3] 성능 분석 (평균/10회)")
    print("#---------------------------------------")
    print(f"{'크기':<7}{'평균 시간(ms)':<12}{'연산 횟수':<5}")
    print("----------------------------------------")

    for size_str, info in perf_data.items():
        avg_time = sum(info["times"]) / len(info["times"])
        op_count = info["count"]
        print(f"{size_str:<9}{avg_time:<16.3f}{op_count:<20}")

    print("\n\n\n#---------------------------------------")
    print("# [4] 결과 요약")
    print("#---------------------------------------")
    print(f"총 테스트: {p_cnt+f_cnt}")
    print(f"통과: {p_cnt}")
    print(f"실패: {f_cnt}\n")
    print("실패 케이스:")
    for i in Fail_case:        
        print(f"- {i}: 동점(UNDECIDED) 처리 규칙에 따라 FAIL")
def main():
    file_name = "data.json"
    validate_and_process_patterns(file_name)
    calculate(file_name)


if __name__ == "__main__":
    main()
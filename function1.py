import time

N = 3
REPEAT = 10

# 2차원 배열 계산 함수
def calculate_2d(fil, pat):
    ave_time = 0

    for _ in range(REPEAT):
        start = time.perf_counter()  # 시간 시작

        total = 0
        for y in range(N):
            for x in range(N):
                total += fil[y][x] * pat[y][x]

        end = time.perf_counter()  # 시간 끝
        ave_time += ((end - start) * 1000) / REPEAT

    return total, ave_time


# 1차원 배열 계산 함수
def calculate_1d(fil, pat):
    ave_time = 0

    for _ in range(REPEAT):
        start = time.perf_counter()  # 시간 시작

        total = 0
        for i in range(N * N):
            total += fil[i] * pat[i]

        end = time.perf_counter()  # 시간 끝
        ave_time += ((end - start) * 1000) / REPEAT

    return total, ave_time


# 2차원 배열을 1차원 배열로 변환하는 함수
def flatten_matrix(matrix):
    arr = []

    for row in matrix:
        arr.extend(row)

    return arr


# 사용자로부터 3X3 배열 입력받기
def user_input(prompt):
    print(f'\n{prompt}')
    matrix = []

    for y in range(N):
        while True:
            try:
                row = list(map(float, input().split()))

                if len(row) != N:
                    print(f"숫자를 정확히 {N}개 입력하세요")
                    continue

                matrix.append(row)
                break

            except ValueError:
                print("숫자만 입력하세요")

    return matrix


def main():
    filters_2d = []  # 2개의 필터를 2차원 배열로 저장
    pattern_2d = []  # 판별하고 싶은 패턴을 2차원 배열로 저장

    print("\n\n\n#---------------------------------------")
    print("# [1] 필터 입력")
    print("#---------------------------------------")

    for x in range(2):
        filters_2d.append(user_input(f"필터 {chr(x + 65)} (3줄 입력, 공백 구분)"))

    print("\n\n\n#---------------------------------------")
    print("# [2] 패턴 입력")
    print("#---------------------------------------")

    pattern_2d = user_input("패턴 (3줄 입력, 공백 구분)")

    # 2차원 배열을 1차원 배열로 변환
    filters_1d = [flatten_matrix(f) for f in filters_2d]
    pattern_1d = flatten_matrix(pattern_2d)


    # 2차원 방식 계산
    A_score_2d, A_time_2d = calculate_2d(filters_2d[0], pattern_2d)
    B_score_2d, B_time_2d = calculate_2d(filters_2d[1], pattern_2d)


    # 1차원 방식 계산  
    A_score_1d, A_time_1d = calculate_1d(filters_1d[0], pattern_1d)
    B_score_1d, B_time_1d = calculate_1d(filters_1d[1], pattern_1d)

    # 1차원과 2차원 계산 방식의 결과 값이 같은지 비교
    if  A_score_1d != A_score_2d or B_score_1d != B_score_2d:
        print("1차원과 2차원의 결과 값이 다릅니다.")
        return 
    total_time_2d = A_time_2d + B_time_2d
    total_time_1d = A_time_1d + B_time_1d
    persentage = ((total_time_2d - total_time_1d)/total_time_1d)*100

    # 2차원 계산 결과를 기준으로 판정
    if abs(A_score_2d - B_score_2d) < 1e-9:
        result = "판정 불가 (|A-B| < 1e-9)"
    elif A_score_2d > B_score_2d:
        result = "A"
    else:
        result = "B"


    # 결과 출력
    print(f'''
#----------------------------------------
# [3] MAC 결과
#----------------------------------------
A 점수: {A_score_2d}
B 점수: {B_score_2d}
판정: {result}

#----------------------------------------
# [4] 2차원 배열 계산 시간
#----------------------------------------
A 계산 시간(평균/{REPEAT}회): {A_time_2d:.6} ms
B 계산 시간(평균/{REPEAT}회): {B_time_2d:.6} ms
총 시간: {(total_time_2d):.6} ms

#----------------------------------------
# [5] 1차원 배열 계산 시간
#----------------------------------------
A 계산 시간(평균/{REPEAT}회): {A_time_1d:.6} ms
B 계산 시간(평균/{REPEAT}회): {B_time_1d:.6} ms
총 시간: {(total_time_1d):.6} ms

#----------------------------------------
# [6] 성능향상 총평
#----------------------------------------
1차원 배열의 계산이 2차원에 비해 {persentage:.2}% 더 빠르다

''')


if __name__ == "__main__":
    main()
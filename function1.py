import time

# 패턴과 필터 사이의 유사도를 계산하는 함수
def calculate(fil,pat):
    ave_time = 0
    for i in range(10):
        start = time.perf_counter() # 시간 시작
        sum = 0
        for y in range(3):
            for x in range(3):
                sum += fil[y][x]*pat[y][x]            
        end = time.perf_counter() # 시간 끝
        ave_time += ((end - start) * 1000)/10
    return sum, ave_time

# 사용자로부터 3X3의 배열을 하나 받아오기(+예외 처리도 포함)
def user_input(prompt):
    print(f'\n{prompt}')
    matrix = []
    for x in range(3):
        while True:
            try:            
                row = list(map(float, input().split()))
                if len(row) != 3:
                    print("숫자를 정확히 3개 입력하세요")
                    continue

                matrix.append(row)
                break

            except ValueError:
                print("숫자만 입력하세요")
    return matrix
            
def main():

    filters = [] # 2개의 필터를 저장하는 리스트
    patter = [] # 판별 하고 싶은 패턴을 저장하는 리스트
    print("\n\n\n#---------------------------------------")
    print("# [1] 필터 입력")
    print("#---------------------------------------")
    for x in range(2):
        filters.append(user_input(f"필터 {chr(x+65)} (3줄 입력, 공백 구분)"))

    print("\n\n\n#---------------------------------------")
    print("# [2] 패턴 입력")
    print("#---------------------------------------")
    patter = user_input(f"패턴 (3줄 입력, 공백 구분)")

    # 계산 함수를 활용해서 평균 시간, 각 점수 받아오기
    A_score, ave_time = calculate(filters[0],patter)
    B_score, ave_time = calculate(filters[1],patter)

    # 리턴 받은 값을 통해서 두 캐이스 중 어느것인지 판정하기
    if abs(A_score - B_score) < 1e-9:
        result = "판정 불가 (|A-B| < 1e-9)"
    elif A_score > B_score:
        result = "A"
    else:
        result = "B"

    # MAC 결과 출력
    print(f'''
        #----------------------------------------
        # [3] MAC 결과 (판정 불가)
        #---------------------------------------
        A 점수:{A_score}
        B 점수:{B_score}
        연산 시간(평균/10회):{ave_time}
        판정:{result}
        ''')
    
if __name__ == "__main__":
    main()
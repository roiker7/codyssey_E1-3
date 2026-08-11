import function1
import function2
from exception import get_int_input
from generator import create_pattern_dataset


def Menu():
    while True:
        print(
            """
=== Mini NPU Simulator ===

[모드 선택]

1. 사용자 입력 (3x3)
2. data.json 분석
3. N x N 패턴 자동 생성 및 분석 
4. 프로그램 종료
        """
        )
        choice = get_int_input("선택: ", min_val=1, max_val=4)

        if choice == 1:
            function1.main()

        elif choice == 2:
            function2.main()

        elif choice == 3:
            try:
                n = int(
                    input(
                        "\n생성할 패턴 크기 N을 입력하세요 (예: 5, 9, 13): "
                    ).strip()
                )
                if n < 3:
                    print("N은 최소 3 이상이어야 합니다.")
                    continue

                # auto_generator_data/generated_data_N.json 경로로 파일 자동 생성
                file_path = create_pattern_dataset(n)
                print(
                    f"\n[성공] 크기 {n}x{n} 패턴 파일('{file_path}') 생성 완료"
                )

                # 생성된 파일 경로로 모듈 2 연산 파이프라인 수행
                function2.validate_and_process_patterns(file_path)
                function2.calculate(file_path)

            except ValueError:
                print("올바른 정수를 입력해주세요.")

        elif choice == 4:
            print("\n프로그램을 종료합니다")
            break


if __name__ == "__main__":
    Menu()
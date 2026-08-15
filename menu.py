from exception import get_int_input
import function1
import function2
import generator
import math

datapath = "data.json"

def Menu():
    while True:  
        print('''
=== Mini NPU Simulator ===

[모드 선택]

1. 사용자 입력 (3x3)
2. data.json 분석
3. 패턴 자동 생성
4. 프로그램 종료
        ''')
        choice = int(get_int_input("선택:",1,4))
        if choice == 1: 
            function1.main()

        elif choice == 2:
            function2.main()

        elif choice == 3:
            n = int(get_int_input("만들고 싶은 배열의 크기 입력:",3,math.inf))
            generator.make_patterns_filters(datapath,n)

        elif choice == 4:
            print("\n프로그램을 종료합니다")
            break
   
if __name__ == "__main__":
    Menu()


  
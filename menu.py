from exception import get_int_input

def menu():
    print('''
        === Mini NPU Simulator ===

        [모드 선택]

        1. 사용자 입력 (3x3)
        2. data.json 분석
    ''')
    while True:  
        choice = int(get_int_input("선택:"))
        if choice == 1: 
            pass
            #1번으로 가는 코드 구현
        elif choice == 2:
            pass
            #2번으로 가는 코드 구현
        elif choice == 3:
            print("\n프로그램을 종료합니다")
            break
   
    
if __name__ == "__main__":
    menu()


  
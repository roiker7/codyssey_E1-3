import sys

def handle_exit():
    try:
        check = input("\n\n작업을 중단하고 이전 메뉴로 돌아가시겠습니까? (y/n): ").strip().lower()
        if check in ['y', 'yes', 'ㅛ']:
            return True
        else:
            print("이전 작업으로 돌아갑니다\n")
            return False
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다")
        sys.exit(0)

# min_val, max_val 기본값 및 범위 동적 설정
def get_int_input(prompt, min_val=1, max_val=3):
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                print("아무것도 입력되지 않았습니다. 다시 입력해 주세요\n")
                continue
            
            val = int(user_input)
            if not (min_val <= val <= max_val):
                print(f"{min_val} ~ {max_val}번 중에 골라주세요\n")
                continue

            return val

        except ValueError:
            print("숫자만 입력해 주세요\n")
        except (KeyboardInterrupt, EOFError):
            if handle_exit():
                return None
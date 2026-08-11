import json

def validate_and_process_patterns(json_file_path):

    # 1. 파일 읽기 ('r' 모드)
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return {"file_error": f"JSON 파일을 읽는 중 오류가 발생했습니다: {e}"}

    filters = data.get("filters", {})
    patterns = data.get("patterns", {})
    results = {}

    # 2. patterns 항목 순회
    for pattern_key, pattern_val in patterns.items():
        # 키 파싱 (size_{N}_{idx} 형태)
        parts = pattern_key.split('_')
        
        # 키 형식이 잘못된 경우
        if len(parts) < 3 or parts[0] != "size":
            results[pattern_key] = {
                "status": "FAIL",
                "reason": f"잘못된 패턴 키 형식입니다: '{pattern_key}'"
            }
            continue

        try:
            target_n = int(parts[1])
        except ValueError:
            results[pattern_key] = {
                "status": "FAIL",
                "reason": f"키에서 N을 숫자로 추출할 수 없습니다: '{parts[1]}'"
            }
            continue

        expected_filter_key = f"size_{target_n}"

        # 3. 매칭되는 필터 존재 여부 확인
        if expected_filter_key not in filters:
            results[pattern_key] = {
                "status": "FAIL",
                "reason": f"필터키 '{expected_filter_key}'가 filters 항목에 존재하지 않습니다."
            }
            continue

        # 4. 패턴 크기 검증 (N x N)
        input_matrix = pattern_val.get("input", [])
        if not isinstance(input_matrix, list):
            results[pattern_key] = {
                "status": "FAIL",
                "reason": "input 필드가 배열 형태가 아닙니다."
            }
            continue

        rows = len(input_matrix)
        if rows != target_n:
            results[pattern_key] = {
                "status": "FAIL",
                "reason": f"행 크기 불일치 (expected: {target_n}, actual: {rows})"
            }
            continue

        # 열 크기 검증
        invalid_cols = [idx for idx, row in enumerate(input_matrix) if not isinstance(row, list) or len(row) != target_n]
        if invalid_cols:
            results[pattern_key] = {
                "status": "FAIL",
                "reason": f"열 크기 불일치 (행 인덱스: {invalid_cols}, expected col size: {target_n})"
            }
            continue

        # 5. 필터 크기 검증 (filters 내 cross, x 등의 크기가 N x N 인지)
        target_filter = filters[expected_filter_key]
        filter_size_error = None

        for filter_type, filter_matrix in target_filter.items():
            if len(filter_matrix) != target_n or any(len(r) != target_n for r in filter_matrix):
                filter_size_error = f"필터 '{expected_filter_key}.{filter_type}'의 크기가 {target_n}x{target_n}과 일치하지 않습니다."
                break

        if filter_size_error:
            results[pattern_key] = {
                "status": "FAIL",
                "reason": filter_size_error
            }
            continue

        # 모든 검증 통과 시
        results[pattern_key] = {
            "status": "PASS",
            "matched_filter": expected_filter_key,
            "expected": pattern_val.get("expected")
        }

    # 결과 출력
    print("\n#--------------------------------------")
    print("# [1] 필터 로드")
    print("#--------------------------------------")
    for key, info in results.items():
        if info["status"] == "FAIL":
            print(f"[{key}]로드 실패 - 원인: {info['reason']}")
        else:
            print(f"[{key}] 필터 로드 성공")


if __name__ == "__main__":
    validate_and_process_patterns("data.json")
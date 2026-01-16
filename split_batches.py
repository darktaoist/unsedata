#!/usr/bin/env python3
"""
tojung.sql 파일을 num별로 배치 분할하는 스크립트
"""
import re
import os

INPUT_FILE = 'input/tojung.sql'
BATCH_DIR = 'input/batches'

def main():
    # SQL 파일 읽기
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # INSERT문 패턴 매칭
    # INSERT INTO public.tojung (...) VALUES (...);
    pattern = r"INSERT INTO public\.tojung \([^)]+\) VALUES \([^;]+\);"
    inserts = re.findall(pattern, content, re.DOTALL)

    print(f"총 INSERT문 갯수: {len(inserts)}")

    # num별로 그룹핑
    batches = {}
    for insert in inserts:
        # num 값 추출 (예: '000', '001', ...)
        num_match = re.search(r"VALUES \(\d+,'(\d{3})'", insert)
        if num_match:
            num = num_match.group(1)
            if num not in batches:
                batches[num] = []
            batches[num].append(insert)

    print(f"num 코드 종류: {len(batches)}개")

    # 배치별로 파일 저장
    os.makedirs(BATCH_DIR, exist_ok=True)

    for num, insert_list in sorted(batches.items()):
        batch_file = os.path.join(BATCH_DIR, f'batch_{num}.sql')
        with open(batch_file, 'w', encoding='utf-8') as f:
            for insert in insert_list:
                f.write(insert + '\n\n')
        print(f"  batch_{num}.sql: {len(insert_list)}개 INSERT문")

    print(f"\n배치 분할 완료! {BATCH_DIR} 폴더 확인")

if __name__ == '__main__':
    main()

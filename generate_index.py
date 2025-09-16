import json
import os

# 'create_database_and_index' 함수 정의 시작 (여기부터는 들여쓰기 필요)
def create_database_and_index():
    all_hanja_data = []
    data_folder = 'data'
    
    if not os.path.exists(data_folder):
        print(f"오류: '{data_folder}' 폴더를 찾을 수 없습니다. 먼저 폴더를 만들고 JSON 파일들을 넣어주세요.")
        return

    print("데이터 파일들을 읽기 시작합니다...")
    for i in range(1, 11):
        file_path = os.path.join(data_folder, f'volume_{i}.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                volume_data = json.load(f)
                all_hanja_data.extend(volume_data)
                print(f"  - {file_path} 로드 완료.")
        except FileNotFoundError:
            print(f"경고: {file_path} 파일을 찾을 수 없어 건너뜁니다.")
        except Exception as e:
            print(f"오류: {file_path} 파일을 처리하는 중 문제가 발생했습니다: {e}")
            return

    db_output_path = os.path.join(data_folder, 'hanja_db.json')
    with open(db_output_path, 'w', encoding='utf-8') as f:
        json.dump(all_hanja_data, f, ensure_ascii=False, indent=2)
    print(f"✅ 성공: 마스터 데이터베이스가 '{db_output_path}'에 저장되었습니다.")

    search_index = []
    for item in all_hanja_data:
        vocab_list = [v.get("title", "") for v in item.get("vocabulary", [])] + \
                     [adv.get("word", "") for adv in item.get("advancedVocabulary", [])]
        index_item = {
            "id": item.get("id"), "hanja": item.get("hanja"),
            "huneum": item.get("huneum"), "sound": item.get("sound"),
            "vocabulary": [v.split('(')[0] for v in vocab_list if v]
        }
        search_index.append(index_item)
    
    search_output_path = os.path.join(data_folder, 'search_index.json')
    with open(search_output_path, 'w', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False)
    print(f"✅ 성공: 검색용 인덱스가 '{search_output_path}'에 저장되었습니다.")
# 함수 정의 끝

# ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
# 이 아래 두 줄은 절대로! 앞에 띄어쓰기(들여쓰기)가 있으면 안 됩니다.
if __name__ == '__main__':
    create_database_and_index()
# ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
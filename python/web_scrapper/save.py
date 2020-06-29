import csv


def save_to_file(jobs):
    # 파일을 열고, mode를 설정(mode="w" 이면 이전 내용 모두 삭제)
    file = open("jobs.csv", mode="w", encoding='UTF-8')

    # csv writer 열기
    writer = csv.writer(file)
    # 가장 윗 줄 이름 적어주기 - 리스트로 넣어줄 것
    writer.writerow(["title", "company", "location", "link"])
    
    for job in jobs:
        # 딕셔너리의 값만 dict_values로 불러와서 list 변환 후 row 단위로 작성
        writer.writerow(list(job.values()))
    return
import os

def info_file(filename: str) -> Dict:
    file_info = {}
    
    # 파일 존재 유무 확인
    if not os.path.exists(filename):
        file_info['error'] = 'File not found'
        return file_info

    # 파일 경로
    file_info['path'] = filename
    
    # 전체 파일명
    file_info['filename'] = os.path.basename(filename)

    # 확장자
    file_info['ext'] = os.path.splitext(filename)[1]

    # 마지막 변경 시간
    file_info['date_lastchanged'] = str(os.path.getmtime(filename))

    # 마지막 접근 시간
    file_info['date_lastaccess'] = str(os.path.getatime(filename))

    # 만든 시간
    file_info['date_create'] = str(os.path.getctime(filename))
    
    return file_info

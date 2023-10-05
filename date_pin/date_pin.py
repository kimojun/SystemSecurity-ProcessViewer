import os
from datetime import datetime

def add_pin(filename:str):
    try:
        # 파일 열기
        with open(filename, 'r+') as file:
            # 파일 내용 읽기
            content = file.read()
            
            # 파일 내용을 수정하여 상단에 핀 추가
            modified_content = f'PINNED: {content}'
            
            # 파일 포인터를 파일의 시작으로 이동
            file.seek(0)
            
            # 수정된 내용을 파일에 쓰기
            file.write(modified_content)
            
            print(f'{filename}에 핀이 추가되었습니다.')
    except FileNotFoundError:
        print(f'Error: {filename}을(를) 찾을 수 없습니다.')
    except Exception as e:
        print(f'Error: {e}')


def has_pin_in_directory(directory:str) -> bool:
    try:
        # 디렉토리 내 모든 파일 리스트 가져오기
        files = os.listdir(directory)
        
        # 디렉토리 내 파일 순회
        for file_name in files:
            # 파일의 전체 경로 생성
            file_path = os.path.join(directory, file_name)
            
            # 파일인지 확인
            if os.path.isfile(file_path):
                # 파일 내용 읽기
                with open(file_path, 'r') as file:
                    content = file.read()
                    
                    # 핀이 있는지 확인
                    if content.startswith('PINNED: '):
                        return True
        return False
    except Exception as e:
        print(f'Error: {e}')
        return False

def get_inspect_date(filename:str) -> datetime:
    try:
        # 파일 열기
        with open(filename, 'r') as file:
            # 파일 내용 읽기
            content = file.read()
            
            # 'inspect_date' 값을 추출
            inspect_date_str = content.split('inspect_date: ')[1].split('\n')[0]
            
            # 날짜 문자열을 datetime 객체로 변환
            inspect_date = datetime.strptime(inspect_date_str, '%Y-%m-%d %H:%M:%S')
            
            return inspect_date
    except FileNotFoundError:
        print(f'Error: {filename}을(를) 찾을 수 없습니다.')
        return None
    except Exception as e:
        print(f'Error: {e}')
        return None

def has_pin(filename:str) -> bool:
    try:
        # 파일 열기
        with open(filename, 'r') as file:
            # 파일 내용 읽기
            content = file.read()
            
            # 핀이 있는지 확인
            return content.startswith('PINNED: ')
    except FileNotFoundError:
        print(f'Error: {filename}을(를) 찾을 수 없습니다.')
        return False
    except Exception as e:
        print(f'Error: {e}')
        return False


def remove_pin(filename:str):
    try:
        # 파일 열기
        with open(filename, 'r+') as file:
            # 파일 내용 읽기
            content = file.read()
            
            # 핀이 있는지 확인하고 있다면 제거
            if content.startswith('PINNED: '):
                modified_content = content[len('PINNED: '):]  # "PINNED: " 부분을 제외한 나머지 내용
                
                # 파일 포인터를 파일의 시작으로 이동
                file.seek(0)
                
                # 수정된 내용을 파일에 쓰기
                file.write(modified_content)
                
                print(f'{filename}의 핀이 제거되었습니다.')
            else:
                print(f'{filename}에는 핀이 존재하지 않습니다.')
    except FileNotFoundError:
        print(f'Error: {filename}을(를) 찾을 수 없습니다.')
    except Exception as e:
        print(f'Error: {e}')

def set_inspect_date(filename:str, date:datetime):
    try:
        # 파일 열기
        with open(filename, 'a') as file:
            # 현재 날짜 및 시간을 문자열로 변환하여 파일에 추가
            file.write(f'\ninspect_date: {date.strftime("%Y-%m-%d %H:%M:%S")}\n')
            
        print(f'{filename}에 분석 날짜가 추가되었습니다.')
    except Exception as e:
        print(f'Error: {e}')








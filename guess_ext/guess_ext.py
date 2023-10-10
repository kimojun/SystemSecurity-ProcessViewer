import binascii
import os


def guess_ext(filename)->list[str]: # filename:str - 파일 경로
    enable_list = []
    
    # 파일 시그니처와 해당 확장자 매핑
    header_signatures = {
        b'\xFF\xD8\xFF': 'jpg',
        b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': 'png',
        b'\x47\x49\x46\x38\x39\x61': 'gif',
        b'\x42\x4D': 'bmp',
        b'\x49\x20\x49': 'tif',
        b'\x49\x20\x2A\x00': 'tiff',
        b'\x50\x4B\x03\x04': 'zip',
        b'\x50\x4B\x05\x06': 'zip',
        b'\x50\x4B\x07\x08': 'zip',
        b'\x7B\x5C\x72\x74\x66': 'rtf',
        b'\x25\x50\x44\x46': 'pdf',
        b'\x4D\x5A': 'exe',
        b'\x4D\x5A\x90\x00\x03\x00\x00\x00': 'exe',
        b'\x4D\x5A\x50\x00\x02\x00\x00\x00': 'exe',
        b'\x4D\x5A\x4E\x00\x02\x00\x00\x00': 'exe',
        b'\x4D\x5A\x6E\x00\x00\x00\x00\x00': 'exe',
        b'\x25\x21\x50\x53\x2D\x41\x64\x6F': 'ps',
        b'\x25\x21\x50\x45\x0D\x0A': 'eps',
        b'\x1F\x8B\x08': 'gz',
        b'\x42\x5A\x68': 'bz2',
        b'\x50\x4B\x03\x04': 'zip',
        b'\x50\x4B\x05\x06': 'zip',
        b'\x50\x4B\x07\x08': 'zip',
        b'\x1F\x9D': 'jar',
        b'\x4D\x5A\x49\x53': 'cab',
        b'\x4D\x44\x4D\x50': 'msi',
        b'\x43\x30\x30\x31': 'iso',
        b'\x21\x3C\x61\x72\x63\x68\x3E': 'arc',
        b'\x1A\x45\xDF\xA3': 'mkv',
        b'\x1F\x43\x4F\x4D': 'z',
        b'\x75\x73\x74\x61\x72': 'tar',
        b'\x4C\x5A\x49\x50': 'lz',
        b'\x28\x54\x68\x69\x73\x20\x66\x69\x6C\x65': 'hqx',
        # 다른 파일 형식의 시그니처를 여기에 추가할 수 있습니다.
    }
    footer_signature = {
        # 다른 파일 형식의 시그니처를 여기에 추가할 수 있습니다.
    }

    try:
        f = open(filename, "rb")
        filelen_byte = os.path.getsize(filename)

        # 파일 초반 1~30바이트를 읽어들여 파일 헤더 시그니처 목록에 매핑하여 가능한 파일 확장자 분류 
        for i in range(1, 30):
            file_signature = f.read(i)
            enable_value = header_signatures.get(file_signature)
            if enable_value:
                enable_list.append(enable_value)
            f.seek(0)
        # 파일 후반 1~30바이트를 읽어들여 파일 푸터 시그니처 목록에 매핑하여 가능한 파일 확장자 분류
        for i in range(1, 30):
            f.seek(filelen_byte - i)
            file_signature = f.read(i)
            enable_value = footer_signature.get(file_signature)
            if enable_value:
                enable_list.append(enable_value)
            f.seek(0)
        f.close()
    # '분석 날짜, 핀 지정' 폴더 내부 함수 코드 참조
    except FileNotFoundError: 
        print(f'Error: {filename}을(를) 찾을 수 없습니다.')
    except Exception as e:
        print(f'Error: {e}')
    
    return enable_list # list[str] - 가능한 확장자명을 리스트에 담아 출력


if __name__ == "__main__":
    # 테스팅 코드
    fd = "파일 경로"
    flist = guess_ext(fd)
    print(flist)



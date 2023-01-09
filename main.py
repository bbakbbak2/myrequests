#-*- encoding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

def getPriv(SESSION, member):
    print("기존 사용자 권한 값과 사용자 고유 값 요청")
    url = "URL입력"+member

    url_get = SESSION.get(url)
    parser = url_get.content
    #print(parser)
    soup = BeautifulSoup(parser, "html.parser")
    # 체크박스(권한이 부여된 권한 가져옴)
    privs = soup.find_all(checked="checked")
    craftPrivs = ""
    for priv in range(len(privs)):
        craftPrivs+='&파라미터[]='+privs[priv].attrs['value']
    
    # 사용자 고유 필수 값 가져오기
    필수값1 = soup.find('input', {'name': '태그이름1'}).get('value')
    필수값2 = soup.find('input', {'name': '태그이름2'}).get('value')

    # Post Payloads
    print("기존 권한부여 POST 파라미터 페이로드 확인")
    result = f'필요한 POST 파라미터 String 값 입력'
    return result

def addPriv(SESSION, USER, oldPriv, addPrivCode):
    url = "URL입력"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    newPriv = oldPriv+f'&파라미터[]={addPrivCode}'
    
    # Redirect 끄기가 중요함
    # 여기서는 인코딩 헤더 값을 필수로 넣어주어야 작동함
    res= SESSION.post(url, data=newPriv, headers=headers)
    if(res.status_code == 200 and int(res.headers['Content-length']) <= 300):
        print(f'{USER} 권한부여 성공 완료')
    else:
        print(f'Error: {res.status_code}, 에러 발생')
        print(res.headers)

# 리스트를 리턴함
def loadMembers():
    f = open('멤버 아이디가 라인 단위로 명시된 텍스트 파일명 입력')
    members = f.readlines()
    members = list(map(lambda s: s.strip(), members))
    return members

def getCredential():
    USER = input("ID: ")
    PASS = input("PWD: ")
    return USER,PASS

def getMFA(SESSION, USER):
    url = "URL입력"
    data = {
        "id": USER,
        "type":"email"
    }
    res = SESSION.post(url, data = data)
    if(res.status_code == 200):
        print("MFA 요청함")
    elif(res.status_code != 200):
        print(f'Error: {res.status_code}, MFA 호출시 에러 발생')
        exit()
    MFA = input("MFA: ")
    return MFA
    

def adminLogin(SESSION, USER,PASS,MFA):

    url = "URL입력"
    data = {
        "id": USER,
        "pass": PASS,
        "verification_code": MFA
    }

    # Redirect 끄기가 중요함
    res= SESSION.post(url, data=data, allow_redirects=False)
    #print(res.cookies.get_dict())

    if(res.status_code == 302):
        print("어드민 로그인 성공하여 세션 받음")
        #리스판스 쿠키로 변경
        SESSION.cookies.update(res.cookies)
    else:
        print(f'Error: {res.status_code}, 로그인시 에러 발생')
        exit()  

if __name__ == "__main__":
    USER = ""
    PASS = ""
    MFA = ""
    MEMBERS = ""
    oldPriv = ""
    print("세션 생성 시작")
    with requests.session() as SESSION:
        # 권한 있는 사용자로 로그인
        USER, PASS = getCredential()
        MFA = getMFA(SESSION, USER)
        adminLogin(SESSION, USER, PASS, MFA)

        addPrivCode = input("Add PrivCode: ")
        # 메모장에 명시된 사용자 계정을 가져옴
        MEMBERS = loadMembers()
        for member in MEMBERS:
            oldPriv = getPriv(SESSION, member)
            addPriv(SESSION, member, oldPriv, addPrivCode)
    

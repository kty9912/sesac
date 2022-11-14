from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.mime.base import MIMEBase
from email import encoders
from os.path import basename

import smtplib

# 이메일 발송을 위한 상수변수들 설정
SMTP_SERVER = 'smtp.naver.com'
SMTP_PORT = 465
SMTP_USER = 'kty9912@naver.com'
SMTP_PASSWORD = open('./email_config','r').read().rstrip()


# 이메일 발송 함수
def send_mail(from_user:str, to_users:list, subject:str, content:str, attachments:list=[], cc_targets=[]) -> bool:
    ''' 
    메일을 발송하는 함수입니다.
    
    **필수값**
    from_user: 보내는 사람의 이메일 주소
    to_users: 받는 사람의 이메일 주소들 (list)
    subject: 메일 제목
    content: 메일 내용

    **선택**
    attachments: 첨부 파일들 (파일경로 리스트)
    cc_targets: 참조 이메일 주소들 (list)
    '''
    try:
        # 이메일 전송서버에 접속
        smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        print('메일 전송 서버 접속 성공')
        smtp.login(SMTP_USER,SMTP_PASSWORD)
        print('로그인 성공')

        # 편지봉투 만들기
        msg = MIMEMultipart('alternative')

        # 첨부파일여부
        # True : 1, ['result.xlsx'],'a'
        # False : 0, [], ''
        if attachments:
            msg = MIMEMultipart('mixed')

            for attachment in attachments:
                # 파일 담을 공간 (첨부 파일)
                email_file = MIMEBase('application', 'octet-stream')

                # 파일 읽어오기
                with open(attachment, 'rb') as f:
                    file_data = f.read()
                
                # 파일 데이터를 첨부파일에 담아준다.
                email_file.set_payload(file_data)
                # base64 인코딩형식으로 인코딩
                encoders.encode_base64(email_file)

                file_name = basename(attachment)
                email_file.add_header('Content-Disposition', 'attachment', filename=file_name)

                msg.attach(email_file)
        
        msg['From'] = from_user
        msg['To'] = ','.join(to_users)
        if cc_targets:
            msg['CC'] = ','.join(cc_targets)
        msg['Subject'] = subject

        # 편지지를 편지봉투에 담아준다
        text = MIMEText(content)
        msg.attach(text)

        # sendmail('보내는 사람', '받는 사람', msg.as_string())
        smtp.sendmail(from_user, set(to_users+cc_targets),msg.as_string())
        print('이메일 발송 성공')

        return True
        
    except Exception as e:
        # 에러났을때 실행할 코드
        print('#### 에러 발생 ####')
        print(e)
        
    finally:
        # 에러 여부 상관없이 무조건 실행할 코드
        # smtp 연결 해제
        smtp.close()
        print('파이널리')
    
    return False

if __name__== '__main__':
    send_mail('kty9912@naver.com', 
    ['kty9912@gmail.com','kty9912@naver.com'], 
    subject='과거는 과거에', content='이제는 앞으로', 
    attachments=['./실습5/커리큘럼.xlsx', './result.xlsx'])
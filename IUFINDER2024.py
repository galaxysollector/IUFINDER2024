from os import system as cmd   #터미널 화면
from time import sleep,localtime #대기
from getpass import getpass  #ENTER 또는 비밀번호
from selenium import webdriver  #브라우저 선택
from selenium.webdriver.common.by import By #요소 찾기
from selenium.common.exceptions import NoSuchWindowException,JavascriptException    #강제 종료 오류
import requests #자동 업데이트
import platform #운영체제 지원 여부 확인
import unicodedata  #자모 분리 방지
import traceback

try:
    cmd('cls')    #최초 실행 터미널 비우기

    version='12.1.1'
    cmd('color 0a')
    print('IUFINDER2024 [Version',version+']')
    print('(c) galaxysollector. All rights reserved.')
    sleep(2)

    cmd('cls')    #다음 화면 터미널 비우기
    sleep(1)

    #시작
    
    off=0   #종료 확인 카운터
    errorlevel=1    #오류 발생 카운터
    end=0   #Chrome 종료 카운터
    usepast=0   #이전 사용자 유뮤 카운터
    usernamed=''    #디버그 모드 전용 사용자 이름
    arm=2   #ARM Edge 브라우저 사용 여부
    loginerrorlevel=0   #로그인 오류 발생 카운터
    checkupdate=0   #업데이트 완료 여부
    logincount=0    #로그인 성공 여부
    start=0 #브라우저 시작 여부
    headless=0  #브라우저 표시 여부
    remove=0  #언팔로워 제거 여부
    save=0  #파일 저장 여부
    ossupport=1   #운영체제 지원 여부
    loginstart=0    #로그인 시작 여부
    theme=0 #터미널 테마
    loginlink='https://www.instagram.com/accounts/login/'
    
    debugging=0 #디버그 모드
    debuggingerrorlevel=0   #디버그 모드 오류 발생 카운터

    def noossupport():  #미지원 운영체제
        print('오류: 지원하지 않는 운영체제입니다. (Windows 11/10 64-bit, Windows 10 32-bit, Windows 11 ARM 만을 지원합니다.)')
        getpass('종료하려면 ENTER 키를 입력하세요.')
        global count
        global ossupport
        global off
        count=0
        ossupport=0
        off=1

    def skipupdate():   #업데이트 건너뛰기
        print('오류: 업데이트를 다운로드할 수 없습니다.')
        print('자동 업데이트를 건너뜁니다...')
        sleep(2)

    def scrollFrom(browser,total_num,option_num): #목록 스크롤
        if len(browser.find_elements(By.CLASS_NAME,'html-div.xdj266r.x14z9mp.xat24cr.x1lziwak.xyri2b.x1c1uobl.x9f619.xjbqb8w.x78zum5.x15mokao.x1ga7v0g.x16uus16.xbiv7yw.xwib8y2.x1y1aw1k.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1'))>0:    #추천 요소 삭제
            browser.execute_script("document.querySelector('.html-div.xdj266r.x14z9mp.xat24cr.x1lziwak.xyri2b.x1c1uobl.x9f619.xjbqb8w.x78zum5.x15mokao.x1ga7v0g.x16uus16.xbiv7yw.xwib8y2.x1y1aw1k.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1').remove()")
        while len(browser.find_elements(By.CLASS_NAME,'xemfg65.xa4qsjk.x1ka1v4i.xbv57ra'))==1:
            browser.execute_script("document.querySelector('.x6nl9eh.x1a5l9x9.x7vuprf.x1mg3h75.x1lliihq.x1iyjqo2.xs83m0k.xz65tgg.x1rife3k.x1n2onr6').scrollTo(0,document.querySelector('.x6nl9eh.x1a5l9x9.x7vuprf.x1mg3h75.x1lliihq.x1iyjqo2.xs83m0k.xz65tgg.x1rife3k.x1n2onr6').scrollHeight)")
            if option_num==0:
                print('\r팔로워 목록을 불러옵니다...',end=' ')
            elif option_num==1:
                print('\r팔로잉 목록을 불러옵니다...',end=' ')
            else:
                print('\r목록을 다시 불러옵니다...',end=' ')
            if round(len(browser.find_elements(By.CLASS_NAME,'x1qnrgzn.x1cek8b2.xb10e19.x19rwo8q.x1lliihq.x193iq5w.xh8yej3'))*100/total_num,2)>100:
                print('(100% 완료)    ',end='')
            else:
                print('('+str(round(len(browser.find_elements(By.CLASS_NAME,'x1qnrgzn.x1cek8b2.xb10e19.x19rwo8q.x1lliihq.x193iq5w.xh8yej3'))*100/total_num,2))+'% 완료)    ',end='')
            if len(browser.find_elements(By.CLASS_NAME,'_a9--._ap36._a9_1'))==1:    #자동화 감지 우회
                browser.find_element(By.CLASS_NAME,'_a9--._ap36._a9_1').click()
                if debugging==1:
                    print('디버그 모드: 자동화 감지를 우회하였습니다!')
        if option_num==0:
            print('\r팔로워 목록을 불러옵니다...',end=' ')
        elif option_num==1:
            print('\r팔로잉 목록을 불러옵니다...',end=' ')
        else:
            print('\r목록을 다시 불러옵니다...',end=' ')
        print('(100% 완료)    ')

    def elementsList(browser,flist):  #목록 리스트
        f_text_temp=[]   #사용자 이름 임시
        f_text=[]   #사용자 이름
        fname_text=[]   #이름
        f=browser.find_elements(By.CLASS_NAME,'html-div.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x9f619.xjbqb8w.x78zum5.x15mokao.x1ga7v0g.x16uus16.xbiv7yw.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1')
        fname=browser.find_elements(By.CLASS_NAME,'x1lliihq.x1plvlek.xryxfnj.x1n2onr6.xyejjpt.x15dsfln.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x1roi4f4.x10wh9bi.xpm28yp.x8viiok.x1o7cslx')
        for i in range(len(f)): #사용자 이름 임시 리스트 생성
            f_text_temp.append(f[i].text)
        for i in f_text_temp:   #사용자 이름 중복 검사, 사용자 이름 리스트 생성
            if i not in f_text:
                f_text.append(i)
        for i in range(len(f_text)):    #사용자 이름 외 텍스트 제거
            if len(f_text[i].split('\n'))>1:
                f_text[i]=f_text[i].split('\n')[0]
                if debugging==1:
                    print('디버그 모드: 사용자 이름 리스트에서 사용자 이름 외 텍스트를 제거하였습니다.')
        for i in range(len(f_text)):    #본인 사용자 이름 제거
            if debugging==0:
                if f_text[i]==username:
                    f_text.remove(username)
            else:
                if f_text[i]==usernamed:
                    f_text.remove(usernamed)
                    print('디버그 모드: 사용자 이름 리스트에서 본인 사용자 이름을 제거하였습니다.')
            break
        for i in range(len(f_text)):    #이름 리스트 생성
            converted=unicodedata.normalize('NFC',fname[i].text)
            fname_text.append(converted)
        for i in range(len(f_text)):    #중복 제외 추가
            if f_text[i] not in flist[0]:
                flist[0].append(f_text[i])
                flist[1].append(fname_text[i])
        return [flist[0],flist[1]]

    #운영체제 지원 여부 확인

    if platform.version()[0]!='1' or platform.version()[1]!='0':
        noossupport()
    
    #ARM 자동 확인

    if platform.machine()=='ARM64':
        arm=1
    elif platform.machine()=='AMD64':
        arm=0
    else:
        noossupport()

    #자동 업데이트

    if ossupport==1:
        try:
            print('자동 업데이트')
            print('\n업데이트를 확인합니다...')
            GITHUB_REPO='galaxysollector/IUFINDER2024'
            API_SERVER_URL=f'https://api.github.com/repos/{GITHUB_REPO}'
            response=requests.get(f'{API_SERVER_URL}/releases/latest')
            if response.status_code!=200:
                skipupdate()
            else:
                receive=response.json()
                latest=1
                if int(receive['tag_name'].split('.')[0][1:])>int(version.split('.')[0]):
                    latest=0
                elif int(receive['tag_name'].split('.')[1])>int(version.split('.')[1]):
                    latest=0
                elif int(receive['tag_name'].split('.')[2])>int(version.split('.')[2]):
                    latest=0
                if latest==0:
                    print('새로운 업데이트가 있습니다!')
                    download_url=receive['assets'][0]['url']
                    response=requests.get(download_url,headers={'Accept':'application/octet-stream'},stream=True)
                    if response.status_code==200:
                        print('업데이트를 다운로드합니다...')
                        update_newFile='IUFINDER2024-'+receive['tag_name'][1:]+'.exe' 
                        download_url='https://github.com/galaxysollector/IUFINDER2024/releases/download/'+receive['tag_name']+'/'+update_newFile
                        response=requests.get(download_url,headers={'Accept':'application/octet-stream'},stream=True)
                        if response.status_code==200:
                            with open(update_newFile,'wb') as update_file:
                                update_file.write(response.content)
                            print('업데이트를 적용하였습니다!')
                            print('다시 시작합니다...')
                            sleep(2)
                            cmd(update_newFile)
                            checkupdate=1
                            off=1
                        else:
                            skipupdate()
                    else:
                        skipupdate()
                else:
                    print('최신 버전을 사용 중입니다!')
                    print('시작합니다...')
                    sleep(2)
        except:
            skipupdate()
    
        if checkupdate==0:  #업데이트 완료 여부 확인
            cmd('cls')    #다음 화면 터미널 비우기

            if localtime().tm_mon==1 and localtime().tm_mday==1:    #날짜 공지
                print('공지: 새해 복 많이 받으세요!\n')
                sleep(1)
            elif localtime().tm_mon==3 and localtime().tm_mday==19:
                theme=1
                cmd('color 0b')
                print('공지: 오늘은 개발자의 생일입니다!\n')
                sleep(1)
            elif localtime().tm_mon==4 and localtime().tm_mday==1:
                theme=2
                cmd('color a0')
                print('공지: 오늘은 만우절입니다!\n')
                sleep(1)

            print('인스타그램 언팔로워 파인더 [버전',version+']') #출력 시작
            sleep(1)
            print('\n인터넷 연결 상태를 먼저 확인하세요.')
            print('목록을 불러오기 위하여 로그인이 필요하며 Chrome이 사용됩니다.')
            sleep(1)
            print('\n시작하려면 ENTER 키를, 종료하려면 다른 키를 입력하세요.')
            count=input('> ')
    
    #시작

    while off==0:
        if count=='':   #시작
            errorlevel=0    #저장 오류 방지
        
            if logincount==0:
                cmd('cls')    #다음 화면 터미널 비우기

            #옵션 선택

            count=0 #입력 확인 카운터
            while count==0:
                if debugging==1:
                    print('디버그 모드\n')
                print('인스타그램 언팔로워 파인더 [버전',version+']\n')
                print('아래의 코드를 입력하여 해당 옵션을 활성화 또는 비활성화하세요.')
                print('아무것도 입력하지 않거나 다른 키를 입력하면 시작됩니다.\n')
                print('HEADLESS > Chrome 브라우저를 표시하지 않습니다. (상태:',end=' ')
                if headless==0:
                    print('비활성화됨)')
                else:
                    print('활성화됨)')
                print('REMOVE > 모든 언팔로워를 자동으로 제거합니다. (상태:',end=' ')
                if remove==0:
                    print('비활성화됨)')
                else:
                    print('활성화됨)')
                print('SAVE > 불러온 목록을 텍스트 파일로 저장합니다. (상태:',end=' ')
                if save==0:
                    print('비활성화됨)')
                else:
                    print('활성화됨)')
                if headless==1:
                    print('(HEADLESS 옵션을 사용할 경우 브라우저 로그가 표시됩니다.)')
                if debugging==1:
                    print('디버그 모드: (기기:',platform.machine()+') (ARM:',end=' ')
                    if arm==0:
                        print('비활성화됨)')
                    else:
                        print('할성화됨)')
                count=input('> ')
                if len(count)==8 and count.upper()=='HEADLESS':  #브라우저 표시 여부
                    count=0
                    if headless==0:
                        headless=1
                    else:
                        headless=0
                    cmd('cls')
                elif len(count)==6 and count.upper()=='REMOVE':  #언팔로워 제거 여부
                    count=0
                    if remove==0:
                        remove=1
                    else:
                        remove=0
                    cmd('cls')
                elif len(count)==4 and count.upper()=='SAVE':  #파일 저장 여부
                    count=0
                    if save==0:
                        save=1
                    else:
                        save=0
                    cmd('cls')
                elif count.upper()=='IAMDEV' or count.upper()=='IAMDEVELOPER' or count=='ㅑ믕ㄷㅍ'or count=='ㅑ믕ㄷㅍ디ㅐㅔㄷㄱ':  #디버그 모드
                    count=0
                    if debugging==0:
                        debugging=1
                        cmd('color 0c')
                    else:
                        debugging=0
                        if platform.machine()=='ARM64':
                            arm=1
                        else:
                            arm=0
                        if theme==1:
                            cmd('color 0b')
                        elif theme==2:
                            cmd('color a0')
                        else:
                            cmd('color 0a')
                    cmd('cls')
                elif debugging==1 and (count.upper()=='ARM' or count=='ㅁ그'):    #디버그 모드 ARM 사용 여부
                    count=0
                    if arm==0:
                        arm=1
                    else:
                        arm=0
                    cmd('cls')
                else:
                    print('시작합니다...')
                    start=0

            #Chrome 시작

            if arm==0:  #브라우저 선택
                from selenium.webdriver.chrome.options import Options
            else:
                from selenium.webdriver.edge.options import Options
            
            options=Options()
            options.add_experimental_option('excludeSwitches',['enable-logging'])
            options.add_argument('window-size=1280,720')
            if headless==1: #headless Chrome 전용 옵션
                options.add_argument('headless')
                options.add_argument('log-level=3')
            
            try:
                if arm==0:  #브라우저 선택
                    browser=webdriver.Chrome(options=options)
                else:
                    browser=webdriver.Edge(options=options)
                count=0
                start=1
            except:
                print('오류: Chrome이 강제로 종료되었습니다.')
                errorlevel=1
                if debugging==1:
                    print(traceback.format_exc())
            
            if errorlevel==0:
                print('\n인스타그램을 시작합니다...')

            while count==0:
                try:
                    browser.get(loginlink)   #인스타그램 로그인 시작
                    count=1
                except NoSuchWindowException:
                    print('오류: Chrome이 강제로 종료되었습니다.')
                    count=1
                    errorlevel=1
                except:
                    print('오류: 인스타그램을 실행하지 못하였습니다.\n팁: 인터넷 연결을 확인한 후 다시 시도해보세요.')
                    count=1
                    errorlevel=1
                    if debugging==1:
                        print(traceback.format_exc())

            #로그인
            
            if errorlevel==0:
                print()
                logincount=0
                while logincount==0:
                    count=0
                    while count==0:
                        if end==0:
                            username=input('사용자 이름을 입력하세요. > ')
                        else:
                            if loginerrorlevel==0 and loginstart==1:
                                print('이전에 입력한 사용자 정보를 다시 사용하려면 R 키를 입력하세요.')
                                print('아무것도 입력하지 않거나 다른 키를 입력하면 처음부터 다시 입력해야 합니다.')
                                usepast=input('> ')
                            if usepast!='R' and usepast!='r':
                                usepast=0
                                if loginerrorlevel==0:
                                    if loginstart==1:
                                        print()
                                    username=input('사용자 이름을 입력하세요. > ')
                                elif loginerrorlevel==1:
                                    username=input('> ')
                                else:
                                    username=input('사용자 이름을 입력하세요. > ')
                        if len(username)==0:
                            print('사용자 이름을 입력하지 않았습니다. 다시 입력하세요.')
                            loginerrorlevel=1
                        else:
                            count=1
                            loginerrorlevel=0
                    if usepast==0:
                        count=0
                        while count==0:
                            password=getpass('비밀번호를 입력하세요. > ')
                            if len(password)<6:
                                if len(password)==0:
                                    print('비밀번호를 입력하지 않았습니다. 다시 입력하세요.')
                                else:
                                    print('6자리 미만의 비밀번호로는 로그인할 수 없습니다. 다시 입력하세요.')
                            else:
                                count=1
                            
                    #자동 로그인 시작
                        
                    print('입력된 정보로 자동으로 로그인합니다...')
                    loginstart=1
                
                    try:
                        while len(browser.find_elements(By.NAME,'username'))==0 and len(browser.find_elements(By.NAME,'email'))==0:    #로그인 창 대기
                            pass
                        if len(browser.find_elements(By.NAME,'username'))==1:   #구형
                            browser.find_element(By.NAME,'username').send_keys(username)    #사용자 이름
                            browser.find_element(By.NAME,'password').send_keys(password)    #비밀번호
                            browser.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[3]/button').click() #로그인 버튼
                            while len(browser.find_elements(By.CLASS_NAME,'x78zum5.xdt5ytf.xl56j7k.x1nrll8i.x10l6tqk.xwa60dl.x11lhmoz'))==1 and browser.current_url==loginlink:    #로그인 판정 대기
                                pass
                        else:   #신형
                            browser.find_element(By.NAME,'email').send_keys(username)    #사용자 이름
                            browser.find_element(By.NAME,'pass').send_keys(password)    #비밀번호
                            browser.find_element(By.CLASS_NAME,'x1i10hfl.xjbqb8w.x1ejq31n.x18oe1m7.x1sy0etr.xstzfhl.x972fbf.x10w94by.x1qhh985.x14e42zd.x1ypdohk.x3ct3a4.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x16tdsg8.x1hl2dhg.xggy1nq.x1fmog5m.xu25z0z.x140muxe.xo1y3bh.x87ps6o.x1lku1pv.x1a2a7pz.x9f619.x3nfvp2.xdt5ytf.xl56j7k.x1n2onr6.xh8yej3').click() #로그인 버튼
                            while len(browser.find_elements(By.CLASS_NAME,'x1c74tu6.xa4qsjk.x1kfoseq.x1a2a7pz.x1bndym7.x1u6ievf.x1wnkzza.x5r0ow9'))==1 and browser.current_url==loginlink:    #로그인 판정 대기
                                pass
                    except:
                        print('오류: Chrome이 강제로 종료되었습니다.')
                        errorlevel=1
                        logincount=1
                        loginerrorlevel=2
                        if debugging==1:
                            print(traceback.format_exc())
                    if logincount==0:
                        try:
                            if browser.current_url[:42]=='https://www.instagram.com/accounts/onetap/':    #완료 (로그인 성공)
                                count=0
                                logincount=1
                            elif browser.current_url=='https://www.instagram.com/':
                                while len(browser.find_elements(By.CLASS_NAME,'x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x87ps6o.x1lku1pv.x1a2a7pz.x14yjl9h.xudhj91.x18nykt9.xww2gxu.x3nfvp2.x1y1aw1k.x1sxyh0.xwib8y2.xurb0ha'))==0:
                                    pass
                                browser.find_element(By.CLASS_NAME,'x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x87ps6o.x1lku1pv.x1a2a7pz.x14yjl9h.xudhj91.x18nykt9.xww2gxu.x3nfvp2.x1y1aw1k.x1sxyh0.xwib8y2.xurb0ha').click()
                                count=0
                                logincount=1
                            elif browser.current_url[:42]=='https://www.instagram.com/accounts/login/two_factor': #완료 (2단계 인증)
                                cmd('cls')    #다음 화면 터미널 비우기
                                print('오류: 이 계정은 2단계 인증이 활성화된 계정입니다.\n팁: 계정 설정에서 2단계 인증을 해제한 후 프로그램을 다시 시작해보세요.')
                                errorlevel=1
                                logincount=1
                            elif browser.current_url==loginlink: #실패 (변화 없음)
                                print('주의: 로그인하지 못하였습니다. ('+browser.find_element(By.CLASS_NAME,'xkmlbd1.xvs91rp.xd4r4e8.x1anpbxc.x11gldyt.xyorhqc.x11hdunq.x2b8uid').text+')')
                                browser.get(loginlink)
                                loginerrorlevel=2
                                usepast=0
                            else:   #실패 (다른 url)
                                if debugging==1:
                                    print(browser.current_url)
                                browser.get(loginlink)
                                if browser.current_url==loginlink:  #로그인 실패
                                    print('오류: 로그인하지 못하였습니다. 사용자 정보를 다시 입력하세요.')
                                    loginerrorlevel=2
                                else:   #로그인 성공
                                    count=0
                                    logincount=0
                        except NoSuchWindowException:
                            print('오류: Chrome이 강제로 종료되었습니다.')
                            errorlevel=1
                            logincount=1
                            loginerrorlevel=2
                        except:
                            print('오류: 로그인하지 못하였습니다. 수동으로 로그인하세요.')
                            if debugging==1:
                                print(traceback.format_exc())
                            getpass('로그인이 완료되면 ENTER 키를 입력하세요.')
                            nextcount=0
                            try:
                                while nextcount==0:
                                    if browser.current_url[:42]=='https://www.instagram.com/accounts/onetap/':
                                        nextcount=1
                                        count=0
                                        logincount=1
                                    elif browser.current_url=='https://www.instagram.com/':
                                        while len(browser.find_elements(By.CLASS_NAME,'x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x87ps6o.x1lku1pv.x1a2a7pz.x14yjl9h.xudhj91.x18nykt9.xww2gxu.x3nfvp2.x1y1aw1k.x1sxyh0.xwib8y2.xurb0ha'))==0:
                                            pass
                                        browser.find_element(By.CLASS_NAME,'x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x87ps6o.x1lku1pv.x1a2a7pz.x14yjl9h.xudhj91.x18nykt9.xww2gxu.x3nfvp2.x1y1aw1k.x1sxyh0.xwib8y2.xurb0ha').click
                                        count=0
                                        logincount=1
                                    else:
                                        print('주의: 로그인이 완료되지 않았습니다.')
                                        getpass('로그인이 완료되면 ENTER 키를 입력하세요.')
                            except:
                                print('오류: Chrome이 강제로 종료되었습니다.')
                                errorlevel=1
                                logincount=1
                                loginerrorlevel=2
                                if debugging==1:
                                    print(traceback.format_exc())

            #팔로워
        
            if errorlevel==0:
                if debugging==1 and debuggingerrorlevel==0:
                    print('디버그 모드: 다른 사용자 이름을 입력하세요. 아무것도 입력하지 않으면 로그인한 사용자 이름으로 진행됩니다.')
                    usernamed=input('> ')
                    if usernamed=='':
                        usernamed=username

                cmd('cls')    #다음 화면 터미널 비우기
                if debugging==1:
                    print('디버그 모드\n')
                print('인스타그램 언팔로워 파인더 [버전',version+']')
                print('\n팔로워 목록을 불러옵니다...',end='')

                try:
                    if debugging==0:
                        profilebutton=browser.find_elements(By.CLASS_NAME,'x1i10hfl.xjbqb8w.x1ejq31n.x18oe1m7.x1sy0etr.xstzfhl.x972fbf.x10w94by.x1qhh985.x14e42zd.x9f619.x1ypdohk.xt0psk2.x3ct3a4.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x4gyw5p._a6hd')    #프로필 버튼
                        browser.execute_script("arguments[0].click();",profilebutton[-3])    #프로필 버튼 클릭
                    else:
                        browser.get('https://www.instagram.com/'+usernamed+'/')
                    while len(browser.find_elements(By.CLASS_NAME,'x1i10hfl.xjbqb8w.x1ejq31n.x18oe1m7.x1sy0etr.xstzfhl.x972fbf.x10w94by.x1qhh985.x14e42zd.x9f619.x1ypdohk.xt0psk2.x3ct3a4.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x5n08af.x9n4tj2._a6hd'))<2:
                        pass
                    button=browser.find_elements(By.CLASS_NAME,'x1i10hfl.xjbqb8w.x1ejq31n.x18oe1m7.x1sy0etr.xstzfhl.x972fbf.x10w94by.x1qhh985.x14e42zd.x9f619.x1ypdohk.xt0psk2.x3ct3a4.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x5n08af.x9n4tj2._a6hd')
                    button[0].click()
                    while len(browser.find_elements(By.CLASS_NAME,'x1qnrgzn.x1cek8b2.xb10e19.x19rwo8q.x1lliihq.x193iq5w.xh8yej3'))==0:
                        pass
                except NoSuchWindowException:
                    print('\n오류: Chrome이 강제로 종료되었습니다.')
                    errorlevel=1
                except Exception as e:
                    if str(e)[9:21]=='disconnected':
                        print('\n오류: Chrome이 강제로 종료되었습니다.')
                        errorlevel=1
                    else:
                        print('\n오류: 알 수 없는 오류가 발생하였습니다.')
                        if debugging==1:
                            print(traceback.format_exc())
                    errorlevel=1
                        
                if errorlevel==0:
                    try:
                        try:
                            name=browser.find_element(By.CLASS_NAME,'html-div.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x9f619.xjbqb8w.x15mokao.x1ga7v0g.x16uus16.xbiv7yw.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1oa3qoh.x6s0dn4.x1amjocr.x78zum5.xl56j7k').text #이름
                            if debugging==1:
                                print('디버그 모드: 이름 요소 1')
                        except:
                            name=browser.find_element(By.CLASS_NAME,'html-div.xdj266r.x14z9mp.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x9f619.xjbqb8w.x15mokao.x1ga7v0g.x16uus16.xbiv7yw.x1e56ztr.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1oa3qoh.x6s0dn4.xmixu3c.x78zum5.xl56j7k').text #이름
                            if debugging==1:
                                print('디버그 모드: 이름 요소 2')
                        followers_num=int(browser.find_elements(By.CLASS_NAME,'x5n08af.x1s688f')[1].text)  #팔로워
                        followings_num=int(browser.find_elements(By.CLASS_NAME,'x5n08af.x1s688f')[2].text) #팔로잉
                    except Exception as e:
                        if str(e)[9:21]=='disconnected':
                            print('\n오류: Chrome이 강제로 종료되었습니다.')
                        else:
                            print('\n오류: 입력된 사용자의 정보를 불러올 수 없습니다.')
                        if debugging==1:
                            print(traceback.format_exc())
                        errorlevel=1
                    
                if errorlevel==0:
                    try:
                        scrollFrom(browser,followers_num,0)
                        followers_text,followersname_text=elementsList(browser,[[],[]])
                        if len(followers_text)!=followers_num:
                            if len(followers_text)==0:
                                print('\n오류: 팔로워 목록이 존재하지 않습니다.\n팁: 일시적인 오류일 수 있습니다. 나중에 다시 시도해보세요.')
                                errorlevel=1
                            else:
                                followersall_num_past=0
                                listpass=0
                                while listpass==0:
                                    if followersall_num_past<len(followers_text) and len(followers_text)<followers_num:
                                        print('주의: 수가 일치하지 않습니다. (목록:',str(len(followers_text))+', 서버:',str(followers_num)+')')
                                        if followersall_num_past<len(followers_text):
                                            followersall_num_past=len(followers_text)
                                            print('목록을 다시 불러옵니다...',end='')
                                            browser.find_element(By.CLASS_NAME,'_abl-').click() #닫기 버튼
                                            while len(browser.find_elements(By.CLASS_NAME,'x1i10hfl.xjbqb8w.x1ejq31n.x18oe1m7.x1sy0etr.xstzfhl.x972fbf.x10w94by.x1qhh985.x14e42zd.x9f619.x1ypdohk.xt0psk2.x3ct3a4.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x5n08af.x9n4tj2._a6hd'))<2:
                                                pass
                                            button=browser.find_elements(By.CLASS_NAME,'x1i10hfl.xjbqb8w.x1ejq31n.x18oe1m7.x1sy0etr.xstzfhl.x972fbf.x10w94by.x1qhh985.x14e42zd.x9f619.x1ypdohk.xt0psk2.x3ct3a4.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x5n08af.x9n4tj2._a6hd')
                                            button[0].click()
                                            while len(browser.find_elements(By.CLASS_NAME,'x1qnrgzn.x1cek8b2.xb10e19.x19rwo8q.x1lliihq.x193iq5w.xh8yej3'))==0:
                                                pass
                                            scrollFrom(browser,followers_num,2)
                                            followers_text,followersname_text=elementsList(browser,[followers_text,followersname_text])
                                    else:
                                        listpass=1
                                        if len(followers_text)!=followers_num:
                                            print('주의: 수가 일치하지 않습니다. (목록:',str(len(followers_text))+', 서버:',str(followers_num)+')')

                        followersall=[] #팔로워 목록
                        for i in range(len(followers_text)):
                            followersall.append([])
                            followersall[i].append(followers_text[i])
                            followersall[i].append(followersname_text[i])
                    except JavascriptException:
                        print('\n오류: 팔로워 목록이 존재하지 않습니다.')
                        errorlevel=1
                    except NoSuchWindowException:
                        print('\n오류: Chrome이 강제로 종료되었습니다.')
                        errorlevel=1
                    except Exception as e:
                        if str(e)[9:21]=='disconnected':
                            print('\n오류: Chrome이 강제로 종료되었습니다.')
                        else:
                            print('\n오류: 알 수 없는 오류가 발생하였습니다.')
                            if debugging==1:
                                print(traceback.format_exc())
                        errorlevel=1

            #팔로잉
        
            if errorlevel==0:
                print('팔로워 수:',str(len(followers_text)))
                if debugging==1:
                    print(followersall)
        
                print('\n팔로잉 목록을 불러옵니다...',end='')
            
                if errorlevel==0:
                    try:
                        if debugging==0:
                            browser.find_element(By.CLASS_NAME,'_abl-').click() #닫기 버튼
                        else:
                            browser.get('https://www.instagram.com/'+usernamed+'/')
                        while len(browser.find_elements(By.CLASS_NAME,'x1i10hfl.xjbqb8w.x1ejq31n.x18oe1m7.x1sy0etr.xstzfhl.x972fbf.x10w94by.x1qhh985.x14e42zd.x9f619.x1ypdohk.xt0psk2.x3ct3a4.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x5n08af.x9n4tj2._a6hd'))<2:
                            pass
                        button=browser.find_elements(By.CLASS_NAME,'x1i10hfl.xjbqb8w.x1ejq31n.x18oe1m7.x1sy0etr.xstzfhl.x972fbf.x10w94by.x1qhh985.x14e42zd.x9f619.x1ypdohk.xt0psk2.x3ct3a4.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x5n08af.x9n4tj2._a6hd')
                        button[1].click()
                        while len(browser.find_elements(By.CLASS_NAME,'x1qnrgzn.x1cek8b2.xb10e19.x19rwo8q.x1lliihq.x193iq5w.xh8yej3'))==0:
                            pass
                    except NoSuchWindowException:
                        print('오류: Chrome이 강제로 종료되었습니다.')
                        errorlevel=1
                    except Exception as e:
                        if str(e)[9:21]=='disconnected':
                            print('오류: Chrome이 강제로 종료되었습니다.')
                            errorlevel=1
                        else:
                            print('오류: 알 수 없는 오류가 발생하였습니다.')
                            if debugging==1:
                                print(traceback.format_exc())
                        errorlevel=1
                    
                if errorlevel==0:
                    try:
                        scrollFrom(browser,followings_num,1)
                        followings_text,followingsname_text=elementsList(browser,[[],[]])
                        if len(followings_text)!=followings_num:
                            if len(followings_text)==0:
                                print('\n오류: 팔로잉 목록이 존재하지 않습니다.\n팁: 일시적인 오류일 수 있습니다. 나중에 다시 시도해보세요.')
                                errorlevel=1
                            else:
                                followingsall_num_past=0
                                listpass=0
                                while listpass==0:
                                    if followingsall_num_past<len(followings_text) and len(followings_text)<followings_num:
                                        print('주의: 수가 일치하지 않습니다. (목록:',str(len(followings_text))+', 서버:',str(followings_num)+')')
                                        if followingsall_num_past<len(followings_text):
                                            followingsall_num_past=len(followings_text)
                                            print('목록을 다시 불러옵니다...',end='')
                                            browser.find_element(By.CLASS_NAME,'_abl-').click() #닫기 버튼
                                            while len(browser.find_elements(By.CLASS_NAME,'x1i10hfl.xjbqb8w.x1ejq31n.x18oe1m7.x1sy0etr.xstzfhl.x972fbf.x10w94by.x1qhh985.x14e42zd.x9f619.x1ypdohk.xt0psk2.x3ct3a4.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x5n08af.x9n4tj2._a6hd'))<2:
                                                pass
                                            button=browser.find_elements(By.CLASS_NAME,'x1i10hfl.xjbqb8w.x1ejq31n.x18oe1m7.x1sy0etr.xstzfhl.x972fbf.x10w94by.x1qhh985.x14e42zd.x9f619.x1ypdohk.xt0psk2.x3ct3a4.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x5n08af.x9n4tj2._a6hd')
                                            button[1].click()
                                            while len(browser.find_elements(By.CLASS_NAME,'x1qnrgzn.x1cek8b2.xb10e19.x19rwo8q.x1lliihq.x193iq5w.xh8yej3'))==0:
                                                pass
                                            scrollFrom(browser,followings_num,2)
                                            followings_text,followingsname_text=elementsList(browser,[followings_text,followingsname_text])
                                    else:
                                        listpass=1
                                        if len(followings_text)!=followings_num:
                                            print('주의: 수가 일치하지 않습니다. (목록:',str(len(followings_text))+', 서버:',str(followings_num)+')')

                        followingsall=[] #팔로잉 목록
                        for i in range(len(followings_text)):
                            followingsall.append([])
                            followingsall[i].append(followings_text[i])
                            followingsall[i].append(followingsname_text[i])
                    except JavascriptException:
                        print('\n오류: 팔로잉 목록이 존재하지 않습니다.')
                        errorlevel=1
                    except NoSuchWindowException:
                        print('\n오류: Chrome이 강제로 종료되었습니다.')
                        errorlevel=1
                    except Exception as e:
                        if str(e)[9:21]=='disconnected':
                            print('\n오류: Chrome이 강제로 종료되었습니다.')
                        else:
                            print('\n오류: 알 수 없는 오류가 발생하였습니다.')
                            if debugging==1:
                                print(traceback.format_exc())
                        errorlevel=1

            #결과
        
            if errorlevel==0:
                print('팔로잉 수:',str(len(followings_text)))
                if debugging==1:
                    print(followingsall)
                
                print('\n불러온 목록을 확인합니다...')
            
                try:
                    unfollower=[]
                    for i in followingsall:
                        if i not in followersall:
                            unfollower.append(i)
                        
                    if len(unfollower)==0:
                        print('언팔로워가 없습니다!')
                    else:
                        print('언팔로워:',end=' ')
                        for i in range(len(unfollower)):
                            if len(unfollower[i][1])==0:
                                print(unfollower[i][0],end='   ')
                            else:
                                print(unfollower[i][0],'('+unfollower[i][1]+')',end='   ')
                        print('('+str(len(unfollower))+')')
                    
                        if remove==1:   #언팔로워 제거
                            print('언팔로워를 제거합니다...')
                            button=browser.find_elements(By.CLASS_NAME,'_aswp._aswr._aswv._asw_._asx2')
                            for i in range(len(unfollower)):
                                button[followingsall.index(unfollower[i])].click()   #팔로잉 버튼
                                browser.find_element(By.CLASS_NAME,'_a9--._ap36._a9-_').click()    #팔로우 취소 버튼
                            for i in range(len(unfollower)):
                                followingsall.remove(unfollower[i]) #팔로잉 목록 업데이트
                            unfollower=[]
                            print('언팔로워를 제거했습니다!')
            
                    unfollowing=[]
                    for i in followersall:
                        if i not in followingsall:
                            unfollowing.append(i)
            
                    if len(unfollowing)==0:
                        print('언팔로잉이 없습니다!')
                    else:
                        print('언팔로잉:',end=' ')
                        for i in range(len(unfollowing)):
                            if len(unfollowing[i][1])==0:
                                print(unfollowing[i][0],end='   ')
                            else:
                                print(unfollowing[i][0],'('+unfollowing[i][1]+')',end='   ')
                        print('('+str(len(unfollowing))+')')
                except:
                    if debugging==1:
                        print(traceback.format_exc())
                    print('오류: 목록이 존재하지 않습니다.')
                    errorlevel=1
                
                if errorlevel==0:   #이전 저장 파일
                    pastfileskip=0
                    if debugging==0:
                        saveusername=username
                    else:
                        saveusername=usernamed
            
                    print('\n이전에 저장된 파일을 확인합니다...')
                    try:
                        saved=open('IUFINDER2024_saved_'+saveusername+'.txt','r',encoding='utf-8')
                        lines=saved.readlines()
                        saved.close()
                    except:
                        if debugging==1:
                            print(traceback.format_exc())
                        print('이전에 저장된 파일이 없습니다. 이 항목을 건너뜁니다...')
                        pastfileskip=1

                    if pastfileskip==0: #이전 팔로워 목록 확인
                        try:
                            linecount=0
                            while True:
                                if len(lines[linecount])>5:
                                    if lines[linecount][0]+lines[linecount][1]+lines[linecount][2]+lines[linecount][3]+lines[linecount][4]=='팔로워: ':
                                        break
                                linecount+=1
                        
                            followersinfile=[]
                            for i in range(int(lines[linecount][5:])):
                                line=lines[i+linecount+2][:-1]
                                linesplit=line.split(maxsplit=1)
                                followersinfile.append([])
                                if len(linesplit)==1:
                                    followersinfile[i].append(line)
                                    followersinfile[i].append('')
                                else:
                                    followersinfile[i].append(linesplit[0])
                                    followersinfile[i].append(linesplit[1][1:-1])
                            linecount=i+linecount+2
                        except:
                            if debugging==1:
                                print(traceback.format_exc())
                            print('올바른 파일이 아닙니다. 이 항목을 건너뜁니다...')
                            pastfileskip=1

                    if pastfileskip==0: #이전 팔로잉 목록 확인
                        try:
                            linecount=0
                            while True:
                                if len(lines[linecount])>5:
                                    if lines[linecount][0]+lines[linecount][1]+lines[linecount][2]+lines[linecount][3]+lines[linecount][4]=='팔로잉: ':
                                        break
                                linecount+=1
                        
                            followingsinfile=[]
                            for i in range(int(lines[linecount][5:])):
                                line=lines[i+linecount+2][:-1]
                                linesplit=line.split(maxsplit=1)
                                followingsinfile.append([])
                                if len(linesplit)==1:
                                    followingsinfile[i].append(line)
                                    followingsinfile[i].append('')
                                else:
                                    followingsinfile[i].append(linesplit[0])
                                    followingsinfile[i].append(linesplit[1][1:-1])
                            linecount=i+linecount+2
                        except:
                            if debugging==1:
                                print(traceback.format_exc())
                            print('올바른 파일이 아닙니다. 이 항목을 건너뜁니다...')
                            pastfileskip=1

                    if pastfileskip==0: #이전 저장 파일 출력
                        afollower=[]
                        for i in followersall:
                            if i not in followersinfile:
                                afollower.append(i)
                        dfollower=[]
                        for i in followersinfile:
                            if i not in followersall:
                                dfollower.append(i)
                        afollowing=[]
                        for i in followingsall:
                            if i not in followingsinfile:
                                afollowing.append(i)
                        dfollowing=[]
                        for i in followingsinfile:
                            if i not in followingsall:
                                dfollowing.append(i)

                        if len(afollower)==0:
                            print('추가된 팔로워가 없습니다!')
                        else:
                            print('추가된 팔로워:',end=' ')
                            for i in range(len(afollower)):
                                if len(afollower[i][1])==0:
                                    print(afollower[i][0],end='   ')
                                else:
                                    print(afollower[i][0],'('+afollower[i][1]+')',end='   ')
                            print('(+'+str(len(afollower))+')')
                        if len(dfollower)==0:
                            print('삭제된 팔로워가 없습니다!')
                        else:
                            print('삭제된 팔로워:',end=' ')
                            for i in range(len(dfollower)):
                                if len(dfollower[i][1])==0:
                                    print(dfollower[i][0],end='   ')
                                else:
                                    print(dfollower[i][0],'('+dfollower[i][1]+')',end='   ')
                            print('(-'+str(len(dfollower))+')')
                        if len(afollowing)==0:
                            print('추가된 팔로잉이 없습니다!')
                        else:
                            print('추가된 팔로잉:',end=' ')
                            for i in range(len(afollowing)):
                                if len(afollowing[i][1])==0:
                                    print(afollowing[i][0],end='   ')
                                else:
                                    print(afollowing[i][0],'('+afollowing[i][1]+')',end='   ')
                            print('(+'+str(len(afollowing))+')')
                        if len(dfollowing)==0:
                            print('삭제된 팔로잉이 없습니다!')
                        else:
                            print('삭제된 팔로잉:',end=' ')
                            for i in range(len(dfollowing)):
                                if len(dfollowing[i][1])==0:
                                    print(dfollowing[i][0],end='   ')
                                else:
                                    print(dfollowing[i][0],'('+dfollowing[i][1]+')',end='   ')
                            print('(-'+str(len(dfollowing))+')')

                    bls=[]
                    blscount=0
                    unfollowercount=0
                    for i in unfollower:    #블랙리스트 생성
                        if i in dfollower:
                            bls.append([])
                            bls[blscount].append(unfollower[unfollowercount][0])
                            bls[blscount].append(unfollower[unfollowercount][1])
                            blscount+=1
                        unfollowercount+=1
                    if len(bls)>0:  #블랙리스트 파일 생성
                        blsinfile=[]
                        blsfile=0
                        try:
                            blacklist=open('IUFINDER2024_BlackList_'+saveusername+'.txt','r',encoding='utf-8')
                            print('언팔로워 블랙리스트 파일을 불러옵니다...')
                            lines=blacklist.readlines()
                            blacklist.close()
                            linecount=0
                            for i in range(1,len(lines)):
                                line=lines[i][:-1]
                                if line!='':
                                    linesplit=line.split(maxsplit=1)
                                    blsinfile.append([])
                                    if len(linesplit)==1:
                                        blsinfile[linecount].append(line)
                                        blsinfile[linecount].append('')
                                    else:
                                        blsinfile[linecount].append(linesplit[0])
                                        blsinfile[linecount].append(linesplit[1][1:-1])
                                    linecount+=1
                            blsfile=1
                            blacklist=open('IUFINDER2024_BlackList_'+saveusername+'.txt','a',encoding='utf-8')
                        except:
                            if debugging==1:
                                print(traceback.format_exc())
                            print('언팔로워 블랙리스트 파일을 생성합니다...')
                            blacklist=open('IUFINDER2024_BlackList_'+saveusername+'.txt','w',encoding='utf-8')
                        try:
                            if blsfile==0:
                                blacklist.write('언팔로워 블랙리스트\n\n')
                            for i in range(len(bls)):
                                for j in range(len(blsinfile)):
                                    if bls[i][0] in blsinfile[j]:
                                        bls.remove(bls[i])
                                        break
                            for i in range(len(bls)):
                                blacklist.write(bls[i][0])
                                if bls[i][1]!='':
                                    blacklist.write(' ('+bls[i][1]+')')
                                blacklist.write('\n')
                            print('언팔로워 블랙리스트를 업데이트하였습니다.')
                        except:
                            if debugging==1:
                                print(traceback.format_exc())
                            print("언팔로워 블랙리스트를 저장할 수 없습니다. 이 항목을 건너뜁니다...")
                        blacklist.close()

            #Chrome 종료
                
            if start==1:
                browser.quit()
            print()
            end=1
        else:   #종료
            off=1

        #파일 저장

        if errorlevel==0 and save==1:
            print('목록을 저장합니다...')
            txt=open('IUFINDER2024_saved_'+saveusername+'.txt','w',encoding='utf-8')
            try:
                txt.write('사용자 이름: '+saveusername+'\n\n\n')
            except:
                print("'사용자 이름'",end=' ')
                print('항목을 저장할 수 없습니다. 이 항목을 건너뜁니다...')
            try:
                if len(name)>0:
                    txt.write('이름: '+name+'\n\n\n')
                else:
                    print('이름이 없습니다. 이 항목을 건너뜁니다...')
            except:
                print("'이름' 항목을 저장할 수 없습니다. 이 항목을 건너뜁니다...")
            try:
                txt.write('팔로워: '+str(len(followersall))+'\n\n')
                for i in range(len(followersall)):
                    txt.write(followersall[i][0])
                    if followersall[i][1]!='':
                        txt.write(' ('+followersall[i][1]+')')
                    txt.write('\n')
                txt.write('\n')
                if len(followersall)>0:
                    txt.write('\n')
            except:
                print("'팔로워' 항목을 저장할 수 없습니다. 이 항목을 건너뜁니다...")
            try:
                txt.write('팔로잉: '+str(len(followingsall))+'\n\n')
                for i in range(len(followingsall)):
                    txt.write(followingsall[i][0])
                    if followingsall[i][1]!='':
                        txt.write(' ('+followingsall[i][1]+')')
                    txt.write('\n')
                txt.write('\n')
                if len(followingsall)>0:
                    txt.write('\n')
            except:
                print("'팔로잉' 항목을 저장할 수 없습니다. 이 항목을 건너뜁니다...")
            try:
                txt.write('언팔로워: '+str(len(unfollower))+'\n\n')
                for i in range(len(unfollower)):
                    txt.write(unfollower[i][0])
                    if unfollower[i][1]!='':
                        txt.write(' ('+unfollower[i][1]+')')
                    txt.write('\n')
                txt.write('\n')
                if len(unfollower)>0:
                    txt.write('\n')
            except:
                print("'언팔로워' 항목을 저장할 수 없습니다. 이 항목을 건너뜁니다...")
            try:
                txt.write('언팔로잉: '+str(len(unfollowing))+'\n\n')
                for i in range(len(unfollowing)):
                    txt.write(unfollowing[i][0])
                    if unfollowing[i][1]!='':
                        txt.write(' ('+unfollowing[i][1]+')')
                    txt.write('\n')
                txt.write('\n')
                if len(unfollowing)>0:
                    txt.write('\n')
            except:
                print("'언팔로잉' 항목을 저장할 수 없습니다. 이 항목을 건너뜁니다...")
            if pastfileskip==0:
                txt.write('추가된 팔로워: '+str(len(afollower))+'\n\n')
                for i in range(len(afollower)):
                    txt.write(afollower[i][0])
                    if afollower[i][1]!='':
                        txt.write(' ('+afollower[i][1]+')')
                    txt.write('\n')
                if len(afollower)>0:
                    txt.write('\n')
                txt.write('\n삭제된 팔로워: '+str(len(dfollower))+'\n\n')
                for i in range(len(dfollower)):
                    txt.write(dfollower[i][0])
                    if dfollower[i][1]!='':
                        txt.write(' ('+dfollower[i][1]+')')
                    txt.write('\n')
                if len(dfollower)>0:
                    txt.write('\n')
                txt.write('\n추가된 팔로잉: '+str(len(afollowing))+'\n\n')
                for i in range(len(afollowing)):
                    txt.write(afollowing[i][0])
                    if afollowing[i][1]!='':
                        txt.write(' ('+afollowing[i][1]+')')
                    txt.write('\n')
                if len(afollowing)>0:
                    txt.write('\n')
                txt.write('\n삭제된 팔로잉: '+str(len(dfollowing))+'\n')
                if len(dfollowing)>0:
                    txt.write('\n')
                for i in range(len(dfollowing)):
                    txt.write(dfollowing[i][0])
                    if dfollowing[i][1]!='':
                        txt.write(' ('+dfollowing[i][1]+')')
                    txt.write('\n')
            txt.close()
            print('저장을 완료하였습니다. 저장된 파일을 보려면 S 키를 입력하세요.')
            count=input('> ')
            if count.upper()=='S':
                print('저장된 파일을 엽니다... (파일을 확인하고 메모장 프로그램을 닫으세요.)')
                cmd('notepad IUFINDER2024_saved_'+saveusername+'.txt')
            print()
        
        if off==0:
            print('다시 시작하려면 R 키를 입력하세요. 다른 키를 입력하면 종료됩니다.')
            count=input('> ')   #다시 시작 대기
        
            if count.upper()=='R':    #다시 시작
                print('다시 시작합니다...')
                count=''
                sleep(1)
                cmd('cls')
            else:
                off=1
        
    #종료

    if checkupdate==0:  #업데이트 완료 여부 확인
        print('종료합니다...')
        sleep(1)

        cmd('cls')
        cmd('color 07')
except:
    cmd('cls')
    cmd('color 07')
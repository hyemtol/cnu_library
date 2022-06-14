import pymysql

from config.config_db import connection_db
from service.MemberService import member_match

# 도서목록 조회
def get_books():

    # 1. MariaDB와 Connection 성공하면
    conn = connection_db()  # Connection -> MariaDB

    try:
        curs = conn.cursor()             # 2. cursor() 객체를 사용해서 작업(노동자)
        sql = "SELECT * FROM tbl_book;"  # 3. MariaDB에서 실행할 SQL문(실행X)
        curs.execute(sql)                # 4. cursor() 객체를 통해서 SQL문 실행(실행O)

        # fetchall() -> 모든 row 반환
        # fetchone() -> 1개 row 반환
        # fetchmany(n) -> n개 row 반환
        rows = curs.fetchall()           # 5. 실행 결과 받기
    finally:
        conn.close()                     # 6. MariaDB Connection 끊기

    print('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    print(':: ISBN\tTITLE\tWRITER\tPUBLISHER\tPRICE\tDATE')
    print('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    for row in rows:
        print(f':: {row.values()}')
    print('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')


# 도서 검색
# 도서 검색
def search_books():
    print(':: 검색하고 싶은 책 이름을 입력해주세요')
    keyword = input('>> 검색 키워드: ')
    conn = connection_db()
    try:
        curs = conn.cursor()
        sql = f'''
                SELECT *
                FROM tbl_book
                WHERE book_name LIKE '%{keyword}%'
                      OR book_writer LIKE '%{keyword}%'
              '''
        curs.execute(sql)
        rows = curs.fetchall()
    finally:
        conn.close()

    print('::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    print(':: ISBN\tTITLE\tWRITER\tPUBLISHER\tPRICE\tDATE')
    print('::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    for row in rows:
        print(f':: {row.values()}')
    print('::::::::::::::::::::::::::::::::::::::::::::::::::::::')


# keyword = "파이썬'
# SELECT문 (DB로부터 데이터를 GET)
# 3: SELECT *      # 데이터의 어떤 Column을 가져올지 # *의 의미 = 전부(book_name , book_LSBN 등등)
# 1: FROM tbl_book # table 설정
# 2: WHERE book_name LIKE '%{keyword}%' # 필터: book_name에 keyword 포함된 것!
# LIKE는 포함을 의미
# WHERE절은 2줄이상 중복불가 but OR을 이용해서 사용



# 도서 대출
def rental_books():
    print('::회원번호를 입력하세요.')
    member_num = input('>>회원번호: ')

    result = member_match(member_num)
    # result = 1(회원) 0(비회원)

    if result == 1:
        # 대출가능책 여부 확인
        print(':: 대출하고싶은 도서 ISBN을 입력하세요.')
        book_isbn = input('>> ISBN: ')
        count = book_yn(book_isbn, 'y') #도서대출 가능 확인

        if count == 1: #대출 가능!
            conn = connection_db()
            try:
                curs = conn.cursor()
                sql = f'''
                        INSERT INTO tbl_rental(book_ISBN, member_id)
                        VALUES({book_isbn}, {member_num})
                    '''
                curs.execute(sql)

                print(f'#MSG: "{member_num}"회원님 도서 "{book_isbn}" 1권 대출 완료하였습니다.')
                # 3.도서 보유 정보 수정 => 대출학 책 COunt -1 (tbl_book)
                book_update_yn(book_isbn, 'n')

            finally:
                conn.close()
        else:  # 대출 불가
            # 경고 메세지 출력 후 메인으로 돌아가기
            print(f'#Warning: "{book_isbn}"도서는 대출이 불가능합니다')
            return

    else:
        #경고 메세지 출력 후 메인으로 돌아가기
        print('#waring: 회원이 아닙니다. 회원등록을 먼저 해주세요.')
        return



# 1. 회원조회
# 2. 도서대출( -> 대출정보 저장 (tbl_rental))
# 3. 도서보유정보 -> 대출한책 Count -1


#도서 대출 가능 확인
#함수끼리는 두줄씩 띄어쓰기

def book_yn(book_isbn, use_yn):
    conn = connection_db()
    try:
        curs = conn.cursor()
        sql = f'''
                SELECT *
                FROM tbl_book
                WHERE book_isbn = "{book_isbn}"
                AND useyn = "{use_yn}"
            '''
        # 해석 from-> where-> select
        curs.execute(sql)
        result = curs.rowcount
    finally:
        conn.close()
    return result


# tbl_book 테이블의 도서의 대출 유무를 변경(y -> n or n-> y)
def book_update_yn(book_isbn, use_yn):
    conn = connection_db()
    try:
        curs = conn.cursor()
        sql = f'''
                UPDATE tbl_book
                SET useyn = '{use_yn}'
                WHERE book_isbn = '{book_isbn}'
                '''
        curs.execute(sql)
    finally:
        conn.closed()




from config.config_db import connection_db


# 회원 목록 조회
def get_members():
    conn = connection_db()

    try:
        curs = conn.cursor()
        sql = '''
                SELECT * 
                FROM tbl_member;
              '''
        curs.execute(sql)
        rows = curs.fetchall()
    finally:
        conn.close()

    print('::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    print(':: ID\tNAME\tPHONE\tDATE')
    print('::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    for row in rows:
        print(f':: {row.values()}')
    print('::::::::::::::::::::::::::::::::::::::::::::::::::::::')


# 회원 유무 판단
def member_match(member_num):
    conn = connection_db()

    try:
        curs = conn.cursor()
        sql = f'''
                SELECT *
                FROM tbl_member
                WHERE member_id = "{member_num}"
               '''
        curs.execute(sql)
        result = curs.rowcount
    finally:
        conn.close()

    return result


# 회원 검색
def search_members():
    print(':: 회원 이름이나 아이디를 입력해주세요')
    keyword = input('>> 검색 키워드: ')
    conn = connection_db()
    try:
        curs = conn.cursor()
        sql = f'''
                SELECT *
                FROM tbl_member
                WHERE member_id LIKE '%{keyword}%'
                      OR member_name LIKE '%{keyword}%'
              '''
        curs.execute(sql)
        rows = curs.fetchall()
    finally:
        conn.close()

    print('::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    print(':: ID\tNAME\tPHONE\tDATE')
    print('::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    for row in rows:
        print(f':: {row.values()}')
    print('::::::::::::::::::::::::::::::::::::::::::::::::::::::')


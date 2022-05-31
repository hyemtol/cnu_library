import pymysql

from config.config_db import connection_db


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


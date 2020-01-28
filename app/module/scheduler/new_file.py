import datetime
def file_create_test(a,b):
    dtm = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    with open(dtm, mode='w', encoding='utf-8') as f:
        f.write('현재시분초 {dtm}'.format(dtm=dtm))
        f.write('p1={a}, p2={b}'.format(a=a, b=b))
    
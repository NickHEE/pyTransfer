import csv, time, random, os

NUM_DATA_FILES = 5
NUM_EMPLOYEES = 3
DATE_START = "20190101_010000"
DATE_END = "20200101_010000"

def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y%d%m_%H%M%S', prop)


if __name__ == '__main__':

    fields = ['Timestamp', 'MagData']

    for _ in range(NUM_EMPLOYEES):

        employeeID = f'{random.randint(1000,10000)}'
        os.mkdir(f'./csvs/{employeeID}')

        for __ in range(NUM_DATA_FILES):

            with open(f'./csvs/{employeeID}/'+str(random_date(DATE_START, DATE_END, random.random()))+'.csv', 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fields)

                writer.writeheader()
                for ___ in range(random.randrange(100, 500)):
                    writer.writerow({'Timestamp': f'{random.random()*100000}', 'MagData': f'{random.random()*2000}'})




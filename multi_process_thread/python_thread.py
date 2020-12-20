import time
import threading


def get_detail_html():
    print("start get detail html ")
    time.sleep(2)
    print("get detail html completed. ")


def get_detail_url():
    print("start get detail url ")
    time.sleep(2)
    print("get detail url completed. ")


if __name__ == '__main__':
    t1 = threading.Thread(target=get_detail_html, args="")
    t2 = threading.Thread(target=get_detail_url, args="")
    print("start time {}".format(time.time()))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    t1.setDaemon()
    t2.setDaemon()
    print("end_time {}".format(time.time()))

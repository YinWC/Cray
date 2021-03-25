# -*- coding: utf-8 -*-
# Author:V1ZkRA
# Time:2021/3/25

from config import *
import multiprocessing
import os
import queue
import subprocess
import sys
import simplejson
import requests



def getTime():
    return time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
def getMtime():
    msg_time = getTime()
    return time_coclor.format(msg_time)


def Xraylog(func):
    def Xraylog(*args):
        with open(log_name, 'a') as log_file:
            log_file.write((template.format(func.__name__, args[0], getMtime())) + "\n")
        func(*args)
    return Xraylog


class Cray():
    '''
      输出类
    '''

    @staticmethod
    @Xraylog
    def info(string):
        print(template.format(info_color.format("info"), msg_color.format(string), getMtime()))

    @staticmethod
    @Xraylog
    def err(string):
        print(template.format(err_color.format("error"), msg_color.format(string), getMtime()))

    @staticmethod
    @Xraylog
    def get(string):
        print(template.format(get_color.format("get"), msg_color.format(string), getMtime()))


def sendrequestsuests(requestsuest_queue):
    '''
    发送请求
    '''
    Cray.info("Send requestsuests")
    proxies = xray_proxies
    while True:
        if requestsuest_queue.empty() == True:
            return
        else:
            requestsuest_data = requestsuest_queue.get()
            requests_url = requestsuest_data['url']
            Cray.info("Processing {}, Remaining requestsuest: {}".format(requests_url, requestsuest_queue.qsize()))
            requests_header = requestsuest_data['headers']
            requests_method = requestsuest_data['method']
            requests_data = requestsuest_data['data']
            try:
                if (requests_method == 'GET'):
                    requests.get(requests_url, headers=requests_header, proxies=proxies, timeout=10, verify=False)
                elif (requests_method == 'POST'):
                    requests.post(requests_url, headers=requests_header, data=requests_data, proxies=proxies, timeout=10, verify=False)
            except:
                continue
    return

def Crawlergorun(command, requestsuest_queue):
    try:
        res = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        cmd_output = bytes()
        while res.poll() is None:
            line = res.stdout.readline()
            line = line.strip()
            if line:
                cmd_output += line
        try:
            crawler_data = simplejson.loads(cmd_output.decode().split("--[Mission Complete]--")[1])
        except Exception as e:
            Cray.err(e)
            return
        requestsuest_list = crawler_data["requests_list"]
        # sub_domain_list = crawler_data["sub_domain_list"] # 子域名
        for requests in requestsuest_list:
            requestsuest_queue.put(requests)
        Cray.info("Crawlergo Done")
        sendrequestsuests(requestsuest_queue)
    except Exception as e:
        Cray.err(e)
        return


def Xrayrun(command):
    try:
        Cray.info("Xray Started")
        res = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while res.poll() is None:
            line = res.stdout.readline()
            line = line.strip()
            if line:
                print(line.decode())
    except Exception as e:
        Cray.err(e)
        return


def urlCheck(url):
    try:
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            return True
    except Exception as e:
        Cray.err("Problem with {}".format(url))
        Cray.err(e)
        return False

def start(url):
    global firstStart
    requestsuest_queue = queue.Queue()
    cmd_xray = [configure["xray_path"]] + args["xray_args"]  # xray 参数
    if firstStart == 1:  # 启动 xray
        background_process = multiprocessing.Process(target=Xrayrun, args=(cmd_xray,))
        background_process.daemon = False
        background_process.start()
        firstStart = 0
    Cray.info("Target: " + url)
    Cray.info("Starting crawlergo")
    cmd_crawlergo = [configure["crawlergo_path"]] + args["crawlergo_args"]  # crawlergo 参数
    cmd_crawlergo.append(url)
    Crawlergorun(cmd_crawlergo, requestsuest_queue)
    Cray.get(url + " Done")


if __name__ == "__main__":
    '''
    python3 Cray.py [url/url_file]
    '''
    if len(sys.argv) == 2:
        para = sys.argv[1]
        if os.path.isfile(para):
            with open(para, 'r') as urlfile:
                for url in urlfile.readlines():
                    url = url.strip()
                    if urlCheck(url):
                        start(url)
        else:
            if urlCheck(para):
                start(para)
    else:
        print("help: python3 Cray.py [url/url_file]")

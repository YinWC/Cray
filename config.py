# -*- coding: utf-8 -*-
# Author:V1ZkRA
# Time:2021/3/25

import time
from colorama import Back, Fore, Style, init

'''
一些配置参数
'''
log_name = "Craylog.log"
xray_proxy =  "127.0.0.1:4780"
close_request = 0
firstStart = 1
xray_output = "{}.html".format(time.strftime("%Y.%m.%d_%H-%M-%S", time.localtime()))
xray_proxies = {
'http': 'http://127.0.0.1:4780',
'https': 'http://127.0.0.1:4780',
}

configure = {
	"chromium_path":"/Users/v1zkra/Desktop/Tools/Others/chrome-mac/Chromium.app/Contents/MacOS/Chromium", # path to Chromium
	"crawlergo_path":"/Users/v1zkra/Desktop/Tools/Pentest/autovul/crawlergo/crawlergo", # path to crawlergo executable file
	"xray_path":"/Users/v1zkra/Desktop/Tools/Pentest/autovul/Xray/xray_darwin_amd64", # path to xray executable file
	}

args = {
	"xray_args":["webscan", "--listen", xray_proxy, "--html-output", xray_output],
	"crawlergo_args":["-c", configure["chromium_path"], "-t", "10", "-f", "smart", "--fuzz-path", "--output-mode", "json"]
	#"crawlergo_args":["-c", configure["chromium_path"], "--push-to-proxy", "http://127.0.0.1:6666", "-t", "10", "-f", "smart", "--fuzz-path", "--output-mode", "json"]
	}

template = "===> [{}] - - \"{}\" {}"
time_coclor = Fore.YELLOW + "{}" + Style.RESET_ALL
info_color = Fore.BLUE + "{}" + Style.RESET_ALL
err_color = Fore.RED + "{}" + Style.RESET_ALL
get_color = Fore.GREEN + "{}" + Style.RESET_ALL
msg_color = Fore.CYAN + "{}" + Style.RESET_ALL
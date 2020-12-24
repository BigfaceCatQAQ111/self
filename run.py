# -*- encoding=utf-8 -*-
# Run Airtest in parallel on multi-device
import os
import traceback
import subprocess
import webbrowser
import time
import json
import shutil
from airtest.core.android.adb import ADB
from jinja2 import Environment, FileSystemLoader
import sendmail
import xlrd
import paramiko
from bs4 import BeautifulSoup


def run(devices, air, run_all=False):
    """"
        run_all
            = True: 从头开始完整测试 (run test fully) ;
            = False: 续着data.json的进度继续测试 (continue test with the progress in data.jason)
    """
    file = os.getcwd() + '\\' + air
    json_file = os.path.join(file, 'data.json')
    project_name = os.getcwd().split('\\')[1]
    romote = "/home/autotest" + '/' +project_name
    try:
        results = load_json_data(air, run_all)
        tasks = run_on_multi_device(devices, air, results, run_all)
        for task in tasks:
            status = task['process'].wait()
            results['tests'][task['dev']] = run_one_report(task['air'], task['dev'])
            results['tests'][task['dev']]['status'] = status
            json.dump(results, open(json_file, "w"), indent=4)
        run_summary(results)
        ftp_dir = copy_log(air)
        change_url(devices, air, ftp_dir)
        sftp_upload(ftp_dir, romote, air)
    except Exception as e:
        traceback.print_exc()


def run_on_multi_device(devices, air, results, run_all):
    """
        在多台设备上运行airtest脚本
        Run airtest on multi-device
    """
    tasks = []
    for dev in devices:
        if (not run_all and results['tests'].get(dev) and
                results['tests'].get(dev).get('status') == 0):
            print("Skip device %s" % dev)
            continue
        log_dir = get_log_dir(dev, air)
        cmd = [
            "airtest",
            "run",
            air,
            "--device",
            "Android:///" + dev,
            "--log",
            log_dir,
            "--recording",
            dev + ".mp4"
        ]
        try:
            tasks.append({
                'process': subprocess.Popen(cmd, cwd=os.getcwd()),
                'dev': dev,
                'air': air
            })
        except Exception as e:
            traceback.print_exc()
    return tasks


def run_one_report(air, dev):
    """"
        生成一个脚本的测试报告
        Build one test report for one air script
    """
    now = time.strftime('%Y-%m-%d_%H_%M_%S')
    # noinspection PyBroadException
    try:
        log_dir = get_log_dir(dev, air)
        log = os.path.join(log_dir, 'log.txt')
        log_dir_new = os.getcwd() + '\\' + log_dir
        if os.path.isfile(log):
            cmd = [
                "airtest",
                "report",
                air,
                "--log_root",
                log_dir,
                "--outfile",
                os.path.join(log_dir, 'log.html'),
                "--lang",
                "zh"
            ]
            ret = subprocess.call(cmd, shell=True, cwd=os.getcwd())
            datapath = os.path.join(os.getcwd(), "device.xls")
            data = xlrd.open_workbook(datapath)
            # 读取第一个工作表
            table = data.sheets()[0]
            # 统计行数
            rows = table.nrows
            data = []  # 存放数据
            for i in range(1, rows):
                values = table.row_values(i)
                data.append(
                    (
                        {
                            "code": values[1],
                            "name": values[0],
                        }
                    )
                )
            # print(data)
            for i in range(0, len(data)):
                if dev == data[i]["code"]:
                    name = data[i]["name"]
            return {
                'status': ret,
                'path': os.path.join(log_dir_new, 'log.html'),
                'name': name
            }
        else:
            print("Report build Failed. File not found in dir %s" % log)
    except Exception as e:
        traceback.print_exc()
    return {'status': -1, 'device': dev, 'path': ''}


def run_summary(data):
    """"
        生成汇总的测试报告
        Build sumary test report
    """

    try:
        summary = {
            'time': "%.3f" % (time.time() - data['start']),
            'success': [item['status'] for item in data['tests'].values()].count(0),
            'count': len(data['tests'])
        }
        summary.update(data)
        summary['start'] = time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.localtime(data['start']))
        print(summary)
        env = Environment(loader=FileSystemLoader(os.getcwd()),
                          trim_blocks=True)
        html = env.get_template('report_tpl.html').render(data=summary)
        report_dir = os.path.join(os.getcwd(), 'summary_report')
        report = report_dir + '\\' + data['script'] + '_report.html'
        # report = data['script'] + '_report.html'
        with open(report, "w", encoding="utf-8") as f:
            f.write(html)
        webbrowser.open(report)
    except Exception as e:
        traceback.print_exc()


def load_json_data(air, run_all):
    """"
        加载进度
            如果data.json存在且run_all=False，加载进度
            否则，返回一个空的进度数据
        Loading data
            if data.json exists and run_all=False, loading progress in data.json
            else return an empty data
    """
    file = os.getcwd() + '\\' + air
    json_file = os.path.join(file, 'data.json')
    if (not run_all) and os.path.isfile(json_file):
        data = json.load(open(json_file))
        data['start'] = time.time()
        return data
    else:
        clear_log_dir(air)
        return {
            'start': time.time(),
            'script': air,
            'tests': {}
        }


def clear_log_dir(air):
    """"
        清理log文件夹
        Remove folder
    """
    log = os.path.join(os.getcwd(), air, 'log')
    if os.path.exists(log):
        shutil.rmtree(log)


def get_log_dir(device, air):
    """"
        在log文件夹下创建每台设备的运行日志文件夹
        Create log folder based on device name under log
    """
    log_dir = os.path.join(air, 'log', device.replace(".", "_").replace(':', '_'))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir


def copy_log(air):
    """
    创建报告的副本，用来修改报告文件中的参数
    """
    now = time.strftime('%Y-%m-%d_%H_%M_%S')
    log_dir = os.path.join(os.getcwd(), air, 'log')
    ftp_dir = os.path.join(os.getcwd(), "FTP_report", air, "report" + now)
    report_dir = os.path.join(os.getcwd(), 'summary_report')
    list = os.listdir(report_dir)
    list.sort(key=lambda fn: os.path.getmtime(report_dir + '\\' + fn))
    report = os.path.join(report_dir, list[-1])
    # if not os.path.exists(ftp_dir):
    #     os.makedirs(ftp_dir)
    # for log_dir_1 in  os.listdir(log_dir):
    #     path = os.path.join(log_dir, log_dir_1)

    shutil.copytree(log_dir, ftp_dir)
    shutil.copy(report, ftp_dir)
    return ftp_dir


def change_url(device, air, ftp):
    global solo_report
    project_name = os.getcwd().split('\\')[1]
    folder_name = ftp.split('\\')[-1]
    file_data = " "
    file_data_1 = " "
    sum_report = ftp + "\\" + air + "_report.html"
    for dev in device:
        solo_report = ftp + "\\" + dev + "\\" + "log.html"

    old_str = r"D:\multi-device-runner-master\test_oppo.air\log"
    old_str_1 = r"c:/users/c/appdata/local/programs/python/python37/lib/site-packages/airtest"
    old_str_2 = r"D:\\multi-device-runner-master\\test_oppo.air\\log"
    old_str_3 = r"c://users//c//appdata//local//programs//python//python37//lib//site-packages//airtest"
    new_str = "http://47.108.203.157:15000/" + r"/" + project_name + r"/" + air + r"/" + folder_name
    new_str_1 = r"http://47.108.203.157:15000/airtest"
    with open(sum_report, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str, new_str)
                line = line.replace("\\", "/")
            file_data += line
    with open(sum_report, "w", encoding="utf-8") as f:
        f.write(file_data)
    if os.path.exists(solo_report):
        with open(solo_report, "r", encoding="utf-8") as p:
            for line1 in p:
                if old_str_1 in line1:
                    line1 = line1.replace(old_str_1, new_str_1)
                    # line1 = line1.replace("\\", "/")
                if old_str in line1:
                    line1 = line1.replace(old_str, new_str)
                    line1 = line1.replace("\\", "/")
                if old_str_2 in line1:
                    line1 = line1.replace(old_str_2, new_str)
                if old_str_3 in line1:
                    line1 = line1.replace(old_str_3, new_str_1)
                file_data_1 += line1
        with open(solo_report, "w", encoding="utf-8") as p:
            p.write(file_data_1)
    else:
        print(solo_report)


def sftp_upload( local, remote, air):
    host = "47.108.203.157"
    port  = 22
    username='autotest'
    pwd='12345,Asdf'
    folder_name = local.split('\\')[-1]
    sf = paramiko.Transport((host, port))
    sf.connect(username=username, password=pwd)
    sftp = paramiko.SFTPClient.from_transport(sf)

    try:
        for f in os.listdir(local):
            # 遍历本地目录
            local_1 = local + "\\" + f
            if os.path.isdir(local_1):
                fwq_dir = remote+ '/' + air
                fwq_dir_1 = remote + '/' + air + '/' + folder_name
                fwq_dir_2 = fwq_dir_1 + '/' + f
                # if os.path.exists(fwq_dir):
                #     continue
                # else:
                #     sftp.mkdir(fwq_dir)
                # if not os.path.exists(fwq_dir):
                #     sftp.mkdir(fwq_dir)
                if not os.path.exists(fwq_dir_1):
                    sftp.mkdir(fwq_dir_1)
                        # sftp.mkdir(os.path.split(fwq_dir)[1])
                if not os.path.exists(fwq_dir_2):
                    sftp.mkdir(fwq_dir_2)
            if os.path.isdir(local_1):
                for p in os.listdir(local_1):
                    upload_file = os.path.join(local_1, p)
                    fwq_dir_3 = fwq_dir_2 + '/' + p
                    sftp.put(upload_file, fwq_dir_3)  # 上传目录中的文件
            else:
                fwq_dir_4 = fwq_dir_1 + '/' + f
                sftp.put(local_1, fwq_dir_4)
    except Exception as e:
        print('upload exception:', e)
    sf.close()


if __name__ == '__main__':
    """
        初始化数据
        Init variables here
    """
    devices = [tmp[0] for tmp in ADB().devices()]
    airs = os.listdir(os.getcwd())

    # with open(report, "r", encoding="utf-8") as f:
    #     f.read()
    #     print(f)
    # soup = BeautifulSoup(open(report), features='html.parser')
    # print(soup)
    # for tag in soup.find_all('D:\multi-device-runner-master'):
    #     print(tag)

    for air in airs:
        if '.air' in air:
            run(devices, air, run_all=True)

            mail = sendmail.SendMail()
            mail.send(air)
        else:
            print('没有找到测试脚本')

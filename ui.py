import atexit
import json
import tkinter
import time
import requests
from tkinter import Tk, BOTH, Canvas, ttk
from demo import get_qr_ticket, call_scan, call_confirm, load_users, User



def qr_frame():
    def on_resize(evt):
        global info
        tk.configure(width=evt.width, height=evt.height)
        canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill='gray', outline='gray')
        info = (canvas.winfo_rootx() - 5, canvas.winfo_rooty() - 5,
                canvas.winfo_width() + 10, canvas.winfo_height() + 10)
        tk.title(f'{info}')
        tk.wm_attributes('-topmost', 1)
        # tk.after(10, on_start)
    
    def on_buttonrelease(evt):
        tk.after(10, on_start)
        
    def on_start():
        if tk.poll:
            print("Polling")
            info = (canvas.winfo_rootx() - 5, canvas.winfo_rooty() - 5,
                    canvas.winfo_width() + 10, canvas.winfo_height() + 10)
            print('canvas: {}'.format(info))
            t0 = time.time()
            ticket = get_qr_ticket(1, info)
            if not ticket:
                print("no ticket")
            else:
                print(ticket)
                tk.count += 1
                print(f'第{tk.count}次detect{ticket}成功')
                # 扫码
                t1 = time.time()
                session = requests.Session()
                session.headers = headers
                res = call_scan(ticket, sess=session, slat=salt)
                t2 = time.time()
                    # 确认
                res = json.loads(res.text)
                print(f'第{tk.count}次call_scan返回{res["retcode"]}：{ticket}，用时：{t1 - t0:.4f}')
                # if login_sleep:
                #     time.sleep(random.random() + 1)
                if res['retcode'] == 0:
                    print(f'抢码成功：{t2 - t1:.4f}')
                    res = call_confirm(tk.user, ticket, session, slat=salt)
                    t3 = time.time()
                    res = json.loads(res.text)
                    if res['retcode'] == 0:
                        print(f'登录成功，耗时：{t3 - t2:.4f}')
                    else:
                        print(f'登录失败：{res}')
                else:
                    print(f'抢码失败{res}')
            print("end")
            tk.after(10, on_start)
        else:
            tk.poll = True
            print("Stopped long running process.")

    def on_stop():
        tk.count = 0
        tk.poll = False
    
    tk = Tk()
    tk.user = user
    tk.poll = True
    tk.count = 0
    tk.geometry('320x320')
    # tk.wm_attributes('-transparentcolor', 'gray')
    # tk.wm_attributes('-topmost', 1)
    tk.attributes('-transparent', True)
   
    tk.attributes('-alpha', 0.8)
    canvas = Canvas(tk)
    canvas.pack(fill=BOTH, expand=True, padx=10, pady=10)
    # button1 = tkinter.Button(tk, text='Button 1', command=print_position)
    # button1.pack()
    # 添加按钮以开始/停止循环
    start = ttk.Button(tk, text="Start", command=on_start)
    start.pack(padx=10)

    stop = ttk.Button(tk, text="Stop", command=on_stop)
    stop.pack(padx=10)
    
    tk.bind('<Configure>', on_resize)
    # tk.bind('<ButtonRelease-1>', on_buttonrelease)
    tk.bind('<B1-Motion>', on_buttonrelease)
    tk.mainloop()



def save():
    with open('region.txt', 'w', encoding='u8') as f:
        json.dump(info, f)


if __name__ == '__main__':
    atexit.register(save)
    info = [0, 0, 0, 0]
    cookies = {
        'stuid': '',
        'stoken': '',
        'mid': '043co169fb_mhy'
    }
    salt = 'A4lPYtN0KGRVwE5M5Fm0DqQiC5VVMVM3'
    app_version = '2.50.1'
    users = load_users()
    user = users[0]
    cookies['stuid'] = user.uid
    cookies['stoken'] = user.stoken
    headers = {
        'DS': '',
        'x-rpc-client_type': '2',
        'x-rpc-app_version': app_version,
        'x-rpc-sys_version': '7.1.2',
        'x-rpc-channel': 'miyousheluodi',
        'x-rpc-device_id': 'd9951154-6eea-35e8-9e46-20c53f440ac7',
        'x-rpc-device_fp': '38d7ed301ed62',
        'x-rpc-device_name': 'HUAWEI LIO-AN00',
        'x-rpc-device_model': 'LIO-AN00',
        'Referer': 'https://app.mihoyo.com',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'api-sdk.mihoyo.com',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3'
    }
    qr_frame()

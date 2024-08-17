import requests
URL = "http://8.137.121.212:65132"
def send_group_msg(group_id, message):
        times = 1
        if type(group_id) != str:
            group_id = str(group_id)
        response = requests.get(URL + '/send_group_msg?group_id=' + group_id + '&message=' + message)
        while response.status_code != 200:
            response = requests.get(URL + '/send_group_msg?group_id=' + group_id + '&message=' + message)
            times += 1
            if times > 3:
                print("发送失败")
                return False
        print("发送成功")
        return True

def reply_group_msg(group_id, message_id, message):
        return send_group_msg(group_id, f"[CQ:reply,id={message_id}] {message}")

def set_group_ban(group_id, user_id, duration):
        if type(group_id) != str:
            group_id = str(group_id)
        if type(user_id) != str:
            user_id = str(user_id)
        if type(duration) != str:
            duration = str(duration)
        return requests.get(URL + '/set_group_ban?group_id=' + group_id + '&user_id=' + user_id + '&duration=' + duration)

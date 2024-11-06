import time
import random
from datetime import datetime

class Util:

    @staticmethod
    def getCurrentTimeRandom():
        # 获取当前时间并生成随机后缀
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        random_suffix = random.randint(1000, 9999)  # 生成4位随机数
        return f'{current_time}_{random_suffix}'

    @staticmethod
    def getRandomSleep(min_seconds=1, max_seconds=3):
        # 随机休眠，避免频繁请求
        sleep_time = random.uniform(min_seconds, max_seconds)
        print(f'休眠 {sleep_time:.2f} 秒')
        time.sleep(sleep_time)

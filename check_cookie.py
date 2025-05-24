import requests
import configparser
import sys
from urllib.parse import urlparse
import time

def load_config():
    """加载配置文件"""
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    return config['config']['Cookie']

def check_cookie(cookie):
    """检查cookie是否有效"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'Cookie': cookie
    }
    
    # 测试URL (使用南京首页作为测试)
    test_url = 'https://www.dianping.com/nanjing'
    
    try:
        response = requests.get(test_url, headers=headers, timeout=10)
        
        # 检查响应状态
        if response.status_code != 200:
            return False, f"HTTP状态码错误: {response.status_code}"
            
        # 检查是否被重定向到验证页面
        final_url = urlparse(response.url)
        if 'verify' in final_url.path:
            return False, "Cookie已失效：需要验证码"
            
        # 检查页面内容是否包含特定标记
        if '验证中心' in response.text:
            return False, "Cookie已失效：需要验证"
            
        return True, "Cookie有效"
        
    except requests.RequestException as e:
        return False, f"请求异常: {str(e)}"

def main():
    print("开始验证Cookie...")
    cookie = load_config()
    
    if not cookie:
        print("错误：未在config.ini中找到Cookie配置")
        sys.exit(1)
    
    print("正在测试Cookie...")
    is_valid, message = check_cookie(cookie)
    
    if is_valid:
        print("✅ " + message)
    else:
        print("❌ " + message)
        print("\n建议操作：")
        print("1. 重新登录大众点评网站")
        print("2. 从浏览器开发者工具中复制新的Cookie")
        print("3. 更新config.ini中的Cookie值")

if __name__ == "__main__":
    main()
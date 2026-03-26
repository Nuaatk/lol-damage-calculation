import requests
import json
import subprocess
import re
import time
import warnings

# 消除SSL验证警告
warnings.filterwarnings('ignore', category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

class LCUAPI:
    def __init__(self):
        self.base_url = None
        self.headers = None
        self.session = requests.Session()
        self._connect()
    
    def _connect(self):
        """连接到LCU API，获取认证信息"""
        try:
            # 尝试读取锁定文件（最可靠的方法）
            import os
            
            # 标准锁定文件路径
            lock_path = os.path.expanduser(r"~\AppData\Local\Riot Games\Riot Client\Config\lockfile")
            
            if os.path.exists(lock_path):
                try:
                    with open(lock_path, 'r') as f:
                        lock_content = f.read().strip()
                    
                    # lockfile格式: process-name:pid:port:password:protocol
                    parts = lock_content.split(':')
                    if len(parts) >= 4:
                        port = parts[2]
                        password = parts[3]
                        self.base_url = f"https://127.0.0.1:{port}"
                        self.headers = {
                            'Content-Type': 'application/json',
                            'Accept': 'application/json',
                            'Authorization': f'Basic {self._encode_auth(password)}'
                        }
                        # 禁用SSL验证
                        self.session.verify = False
                        return
                except Exception as e:
                    print(f"读取锁定文件失败: {str(e)}")
            
            # 如果锁定文件方法失败，使用PowerShell命令获取进程信息
            print("使用PowerShell命令获取LCU凭证...")
            
            # 使用PowerShell命令获取进程信息
            ps_command = "Get-CimInstance -ClassName Win32_Process -Filter \"name='LeagueClientUx.exe'\" | ForEach-Object { $_.CommandLine }"
            result = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)
            
            # 从命令行参数中提取端口和密码
            port_pattern = r'--app-port=(\d+)'
            password_pattern = r'--remoting-auth-token=([^\s]+)'
            
            port_match = re.search(port_pattern, result.stdout)
            password_match = re.search(password_pattern, result.stdout)
            
            if port_match and password_match:
                port = port_match.group(1)
                password = password_match.group(1)
                # 移除密码中的引号
                password = password.strip('"')
                self.base_url = f"https://127.0.0.1:{port}"
                self.headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Authorization': f'Basic {self._encode_auth(password)}'
                }
                # 禁用SSL验证
                self.session.verify = False
                print(f"成功获取LCU凭证: 端口={port}")
            else:
                print("无法获取LCU凭证，请确保英雄联盟客户端已启动")
                print("调试信息:")
                print(f"命令输出: {result.stdout}")
                print(f"错误信息: {result.stderr}")
                raise Exception("无法获取League Client进程信息")
        except Exception as e:
            raise Exception(f"连接失败: {str(e)}")
    
    def _encode_auth(self, password):
        """编码认证信息"""
        import base64
        return base64.b64encode(f'riot:{password}'.encode()).decode()
    
    def get(self, endpoint):
        """发送GET请求"""
        try:
            response = self.session.get(f"{self.base_url}{endpoint}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"GET请求失败: {e}")
            return None
    
    def post(self, endpoint, data=None):
        """发送POST请求"""
        try:
            response = self.session.post(f"{self.base_url}{endpoint}", headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"POST请求失败: {e}")
            return None
    
    def get_client_state(self):
        """获取客户端状态"""
        return self.get("/lol-gameflow/v1/gameflow-phase")
    
    def get_champ_select(self):
        """获取英雄选择信息"""
        return self.get("/lol-champ-select/v1/session")
    
    def get_match_history(self, count=1):
        """获取匹配历史"""
        return self.get(f"/lol-match-history/v1/products/lol/{self.get_summoner_id()}/matches?count={count}")
    
    def get_summoner_id(self):
        """获取当前召唤师ID"""
        summoner = self.get("/lol-summoner/v1/current-summoner")
        return summoner['summonerId'] if summoner else None
    
    def get_match_details(self, match_id):
        """获取匹配详情"""
        return self.get(f"/lol-match-history/v1/matches/{match_id}")
    
    def get_gameflow_session(self):
        """获取游戏流程会话信息"""
        return self.get("/lol-gameflow/v1/session")

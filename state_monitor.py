import time
import threading

class StateMonitor:
    def __init__(self, lcu_api):
        self.lcu_api = lcu_api
        self.running = False
        self.state = None
        self.last_state = None
        self.champ_select_data = None
        self.match_end_data = None
        self.on_champ_select_start = None
        self.on_game_end = None
    
    def start(self):
        """开始状态监控"""
        self.running = True
        thread = threading.Thread(target=self._monitor_loop)
        thread.daemon = True
        thread.start()
    
    def stop(self):
        """停止状态监控"""
        self.running = False
    
    def _monitor_loop(self):
        """监控循环"""
        while self.running:
            try:
                # 获取当前状态
                current_state = self.lcu_api.get_client_state()
                self.state = current_state
                
                # 状态变化检测
                if current_state != self.last_state:
                    print(f"状态变化: {self.last_state} -> {current_state}")
                    self._handle_state_change(current_state)
                
                # 英雄选择状态处理
                if current_state == "ChampSelect":
                    self._handle_champ_select()
                
                # 游戏结束状态处理
                if current_state == "EndOfGame":
                    self._handle_game_end()
                
                self.last_state = current_state
            except Exception as e:
                print(f"监控错误: {e}")
            
            time.sleep(2)  # 每2秒检查一次
    
    def _handle_state_change(self, new_state):
        """处理状态变化"""
        pass
    
    def _handle_champ_select(self):
        """处理英雄选择状态"""
        try:
            champ_select = self.lcu_api.get_champ_select()
            gameflow_session = self.lcu_api.get_gameflow_session()
            
            if champ_select:
                self.champ_select_data = champ_select
                # 将gameflow_session也传递给回调函数
                if self.on_champ_select_start:
                    self.on_champ_select_start(champ_select, gameflow_session)
        except Exception as e:
            print(f"处理英雄选择错误: {e}")
    
    def _handle_game_end(self):
        """处理游戏结束状态"""
        try:
            # 获取最近的比赛记录
            match_history = self.lcu_api.get_match_history(count=1)
            if match_history and match_history.get('games'):
                latest_match = match_history['games'][0]
                match_id = latest_match['gameId']
                match_details = self.lcu_api.get_match_details(match_id)
                if match_details:
                    self.match_end_data = match_details
                    if self.on_game_end:
                        self.on_game_end(match_details)
        except Exception as e:
            print(f"处理游戏结束错误: {e}")

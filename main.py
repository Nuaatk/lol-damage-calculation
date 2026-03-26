import time
from lcu_api import LCUAPI
from state_monitor import StateMonitor
from champ_select_parser import ChampSelectParser
from match_parser import MatchParser
from damage_calculator import DamageCalculator
from result_display import ResultDisplay

class HextechDamageCalculator:
    def __init__(self):
        self.lcu_api = None
        self.state_monitor = None
        self.team_formation = None
        self.players_info = None
        self.running = True
    
    def start(self):
        """启动程序"""
        try:
            print("正在连接到英雄联盟客户端...")
            
            # 尝试连接，直到成功
            while self.running:
                try:
                    self.lcu_api = LCUAPI()
                    print("连接成功！")
                    break
                except Exception as e:
                    print(f"连接失败: {e}")
                    print("等待英雄联盟客户端启动...")
                    time.sleep(5)
            
            if not self.running:
                return
            
            # 初始化状态监控
            self.state_monitor = StateMonitor(self.lcu_api)
            self.state_monitor.on_champ_select_start = self.handle_champ_select
            self.state_monitor.on_game_end = self.handle_game_end
            self.state_monitor.start()
            
            print("监控已启动，等待游戏开始...")
            print("按 Ctrl+C 退出程序")
            
            # 主循环
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n程序正在退出...")
            self.stop()
        except Exception as e:
            print(f"错误: {e}")
            self.stop()
    
    def stop(self):
        """停止程序"""
        if self.state_monitor:
            self.state_monitor.stop()
        self.running = False
    
    def handle_champ_select(self, champ_select_data, gameflow_session=None):
        """处理英雄选择事件"""
        print("\n=== 检测到英雄选择阶段 ===")
        
        # 解析英雄选择数据
        self.players_info = ChampSelectParser.parse_champ_select_data(champ_select_data)
        
        # 尝试从gameflow_session获取更多信息
        if gameflow_session:
            print("\n=== 从游戏流程会话获取信息 ===")
            if 'gameData' in gameflow_session:
                print(f"gameData结构: {list(gameflow_session['gameData'].keys())}")
                
                # 尝试从playerChampionSelections获取
                if 'playerChampionSelections' in gameflow_session['gameData']:
                    selections = gameflow_session['gameData']['playerChampionSelections']
                    print(f"playerChampionSelections数量: {len(selections)}")
                    if selections:
                        print(f"第一个选择的结构: {list(selections[0].keys())}")
                        # 尝试更新玩家信息
                        for selection in selections:
                            summoner_name = selection.get('summonerName') or selection.get('summonerInternalName')
                            cell_id = selection.get('cellId')
                            if summoner_name and cell_id:
                                for player in self.players_info:
                                    if player['cell_id'] == cell_id:
                                        player['summoner_name'] = summoner_name
                                        print(f"更新玩家信息: cell_id={cell_id}, summoner_name={summoner_name}")
        
        if self.players_info:
            # 显示玩家信息
            ResultDisplay.display_player_info(self.players_info)
            
            # 确定队伍组成
            self.team_formation = ChampSelectParser.get_team_formation(self.players_info)
            ResultDisplay.display_team_formation(self.team_formation)
            
            print("\n队伍信息已保存，等待游戏结束...")
    
    def handle_game_end(self, match_details):
        """处理游戏结束事件"""
        print("\n=== 检测到游戏结束 ===")
        
        if not self.team_formation:
            print("错误：未获取到队伍信息，请确保在英雄选择阶段程序已运行")
            return
        
        # 解析比赛数据
        players_damage = MatchParser.parse_match_details(match_details)
        
        if players_damage:
            # 显示玩家伤害数据
            ResultDisplay.display_player_damage(players_damage)
            
            # 计算队伍伤害
            team_damage = DamageCalculator.calculate_team_damage(self.team_formation, players_damage)
            
            # 排名队伍
            ranks = DamageCalculator.rank_teams(team_damage)
            
            # 显示结果
            ResultDisplay.display_damage_results(team_damage, ranks)
            
            print("\n计算完成！")

if __name__ == "__main__":
    calculator = HextechDamageCalculator()
    calculator.start()

class ResultDisplay:
    @staticmethod
    def display_player_info(players):
        """显示玩家信息"""
        print("\n=== 玩家楼层信息 ===")
        for player in players:
            summoner_name = player['summoner_name'] if player['summoner_name'] else '未知玩家'
            print(f"楼层 {player['floor']}: {summoner_name}")
    
    @staticmethod
    def display_team_formation(team_formation):
        """显示队伍组成"""
        print("\n=== 队伍组成 ===")
        for team_key, players in team_formation.items():
            team_name = DamageCalculator.get_team_display_name(team_key)
            player_names = [p['summoner_name'] if p['summoner_name'] else '未知玩家' for p in players]
            print(f"{team_name}: {', '.join(player_names)}")
    
    @staticmethod
    def display_damage_results(team_damage, ranks):
        """显示伤害计算结果"""
        print("\n=== 伤害计算结果 ===")
        for team_key, damage in team_damage.items():
            team_name = DamageCalculator.get_team_display_name(team_key)
            print(f"{team_name}: {damage} 伤害")
        
        print("\n=== 排名 ===")
        for rank_info in ranks:
            team_name = DamageCalculator.get_team_display_name(rank_info['team'])
            print(f"第 {rank_info['rank']} 名: {team_name} - {rank_info['damage']} 伤害")
    
    @staticmethod
    def display_player_damage(players_damage):
        """显示每个玩家的伤害数据"""
        print("\n=== 玩家伤害数据 ===")
        for player in players_damage:
            print(f"{player['summoner_name']} ({player['champion_name']}): {player['damage_dealt_to_champions']} 伤害")

# 导入需要的类
from damage_calculator import DamageCalculator

class DamageCalculator:
    @staticmethod
    def calculate_team_damage(team_formation, players_damage, damage_adjustments=None):
        """计算每个队伍的伤害总和"""
        if not team_formation or not players_damage:
            return None, {}
        
        team_damage = {
            'team1': 0,  # 1楼和2楼
            'team2': 0,  # 3楼
            'team3': 0   # 4楼和5楼
        }
        
        # 记录应用了伤害调整的玩家
        adjusted_players = {}
        
        # 如果没有提供伤害调整，使用空字典
        if damage_adjustments is None:
            damage_adjustments = {}
        
        # 创建伤害数据字典，方便查找
        damage_dict = {player['summoner_name']: player['damage_dealt_to_champions'] 
                      for player in players_damage}
        
        # 计算team1伤害
        for player in team_formation['team1']:
            if player['summoner_name'] in damage_dict:
                damage = damage_dict[player['summoner_name']]
                original_damage = damage
                # 应用伤害调整
                if player['summoner_name'] in damage_adjustments:
                    damage *= damage_adjustments[player['summoner_name']]
                    adjusted_players[player['summoner_name']] = {
                        'original_damage': original_damage,
                        'adjusted_damage': damage,
                        'factor': damage_adjustments[player['summoner_name']]
                    }
                team_damage['team1'] += damage
        
        # 计算team2伤害（3楼乘以2）
        for player in team_formation['team2']:
            if player['summoner_name'] in damage_dict:
                damage = damage_dict[player['summoner_name']]
                original_damage = damage
                # 应用伤害调整
                if player['summoner_name'] in damage_adjustments:
                    damage *= damage_adjustments[player['summoner_name']]
                    adjusted_players[player['summoner_name']] = {
                        'original_damage': original_damage,
                        'adjusted_damage': damage,
                        'factor': damage_adjustments[player['summoner_name']]
                    }
                team_damage['team2'] += damage * 2
        
        # 计算team3伤害
        for player in team_formation['team3']:
            if player['summoner_name'] in damage_dict:
                damage = damage_dict[player['summoner_name']]
                original_damage = damage
                # 应用伤害调整
                if player['summoner_name'] in damage_adjustments:
                    damage *= damage_adjustments[player['summoner_name']]
                    adjusted_players[player['summoner_name']] = {
                        'original_damage': original_damage,
                        'adjusted_damage': damage,
                        'factor': damage_adjustments[player['summoner_name']]
                    }
                team_damage['team3'] += damage
        
        return team_damage, adjusted_players
    
    @staticmethod
    def rank_teams(team_damage):
        """对队伍进行排名"""
        if not team_damage:
            return None
        
        # 排序队伍
        sorted_teams = sorted(team_damage.items(), 
                             key=lambda x: x[1], 
                             reverse=True)
        
        # 生成排名
        ranks = []
        for i, (team, damage) in enumerate(sorted_teams, 1):
            ranks.append({
                'rank': i,
                'team': team,
                'damage': damage
            })
        
        return ranks
    
    @staticmethod
    def get_team_display_name(team_key):
        """获取队伍的显示名称"""
        team_names = {
            'team1': '1楼和2楼',
            'team2': '3楼',
            'team3': '4楼和5楼'
        }
        return team_names.get(team_key, team_key)

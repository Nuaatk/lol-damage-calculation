class MatchParser:
    @staticmethod
    def parse_match_details(match_details):
        """解析匹配详情，获取玩家伤害数据"""
        if not match_details:
            return None
        
        players_damage = []
        
        # 获取参与者数据
        participants = match_details.get('game', {}).get('participants', [])
        
        for participant in participants:
            player_info = {
                'summoner_name': participant.get('summonerName'),
                'champion_name': participant.get('championName'),
                'damage_dealt_to_champions': participant.get('stats', {}).get('totalDamageDealtToChampions', 0),
                'kills': participant.get('stats', {}).get('kills', 0),
                'deaths': participant.get('stats', {}).get('deaths', 0),
                'assists': participant.get('stats', {}).get('assists', 0)
            }
            players_damage.append(player_info)
        
        return players_damage
    
    @staticmethod
    def get_player_damage(players_damage, summoner_name):
        """根据召唤师名称获取伤害数据"""
        for player in players_damage:
            if player['summoner_name'] == summoner_name:
                return player
        return None

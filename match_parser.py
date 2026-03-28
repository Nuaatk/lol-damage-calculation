class MatchParser:
    @staticmethod
    def parse_match_details(match_details):
        """解析匹配详情，获取玩家伤害数据"""
        if not match_details:
            return None
        
        players_damage = []
        
        # 尝试不同的匹配详情格式
        # 格式1: 直接包含participants和participantIdentities
        if 'participants' in match_details and 'participantIdentities' in match_details:
            participants = match_details['participants']
            participant_identities = match_details['participantIdentities']
            
            # 创建召唤师ID到名称的映射
            summoner_name_map = {}
            for identity in participant_identities:
                if 'player' in identity:
                    player = identity['player']
                    summoner_id = player.get('summonerId')
                    summoner_name = player.get('gameName', '未知')
                    if summoner_id:
                        summoner_name_map[summoner_id] = summoner_name
            
            # 解析每个参与者的伤害数据
            for participant in participants:
                # 获取召唤师名称
                summoner_name = '未知'
                participant_id = participant.get('participantId')
                for identity in participant_identities:
                    if identity.get('participantId') == participant_id:
                        if 'player' in identity:
                            summoner_name = identity['player'].get('gameName', '未知')
                        break
                
                # 获取伤害数据
                damage_dealt = 0
                if 'stats' in participant:
                    damage_dealt = participant['stats'].get('totalDamageDealtToChampions', 0)
                
                player_info = {
                    'summoner_name': summoner_name,
                    'champion_name': participant.get('championName', '未知'),
                    'damage_dealt_to_champions': damage_dealt,
                    'kills': participant.get('stats', {}).get('kills', 0),
                    'deaths': participant.get('stats', {}).get('deaths', 0),
                    'assists': participant.get('stats', {}).get('assists', 0)
                }
                players_damage.append(player_info)
        
        # 格式2: 包含在game字段中
        elif 'game' in match_details:
            participants = match_details['game'].get('participants', [])
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

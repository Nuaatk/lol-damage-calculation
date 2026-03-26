class ChampSelectParser:
    @staticmethod
    def parse_champ_select_data(champ_select_data):
        """解析英雄选择数据，获取玩家信息和楼层"""
        if not champ_select_data:
            return None
        
        players = []
        
        # 打印调试信息
        print("\n=== 英雄选择数据解析 ===")
        print(f"Actions数量: {len(champ_select_data.get('actions', []))}")
        print(f"MyTeam数量: {len(champ_select_data.get('myTeam', []))}")
        print(f"TheirTeam数量: {len(champ_select_data.get('theirTeam', []))}")
        
        # 直接从myTeam和theirTeam获取所有玩家信息
        all_participants = champ_select_data.get('myTeam', []) + champ_select_data.get('theirTeam', [])
        print(f"总参与者数量: {len(all_participants)}")
        
        for i, participant in enumerate(all_participants):
            # 打印第一个参与者的完整信息，查看字段结构
            if i == 0:
                print("\n第一个参与者的完整信息:")
                for key, value in participant.items():
                    print(f"  {key}: {value}")
            
            # 尝试不同的字段名获取玩家名称
            summoner_name = participant.get('gameName') or participant.get('summonerName') or participant.get('summoner_name') or participant.get('displayName') or participant.get('name')
            print(f"参与者{i}: cellId={participant.get('cellId')}, 名称={summoner_name}")
            
            # 创建玩家信息
            player_info = {
                'cell_id': participant.get('cellId'),
                'summoner_name': summoner_name,
                'team': participant.get('team', 0),
                'pick_turn': participant.get('pickTurn', 0)
            }
            players.append(player_info)
        
        print(f"\n解析到的玩家数量: {len(players)}")
        
        # 按照pickTurn排序确定楼层
        players.sort(key=lambda x: x['pick_turn'] if x['pick_turn'] else 999)
        
        # 分配楼层
        for i, player in enumerate(players):
            player['floor'] = i + 1
        
        return players
    
    @staticmethod
    def get_team_formation(players):
        """根据楼层确定队伍组成"""
        if not players:
            return None
        
        teams = {
            'team1': [],  # 1楼和2楼
            'team2': [],  # 3楼
            'team3': []   # 4楼和5楼
        }
        
        for player in players:
            if player['floor'] in [1, 2]:
                teams['team1'].append(player)
            elif player['floor'] == 3:
                teams['team2'].append(player)
            elif player['floor'] in [4, 5]:
                teams['team3'].append(player)
        
        return teams

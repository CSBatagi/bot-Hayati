from __future__ import print_function
from asyncio import create_task, gather
from googleapiclient.discovery import Resource, build
from google.oauth2 import service_account
from funs import format_matrix 
import constants as c
from itertools import chain
from typing import List, Tuple 

class GSheet(object):
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        secret_file = 'credentials.json'
        self.creds = service_account.Credentials.from_service_account_file(secret_file, scopes=SCOPES)    
        
        self.service: Resource = build('sheets', 'v4', credentials=self.creds)
        

    async def update(self, sheetid:str, sheetrange:str, values:str):
        # Call the Sheets API
        sheet = self.service.spreadsheets()
        body = {
            'values': values
        }
        return sheet.values().update(
            spreadsheetId=sheetid, range=sheetrange,
            valueInputOption='USER_ENTERED', body=body).execute()
        
    async def get(self, sheetid:str , sheet_range: str):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheetid,
                                range=sheet_range).execute()
        return result.get('values', [])
    
    async def get_player_status(self, typ: str = "darla") -> Tuple:
        tasks = [
         create_task(self.get_name_to_steam_map()),
         create_task(self.get(c.SPREADSHEET_ID, c.DRAFT_RANGE)),
        ]

        (name_to_steam_map, draft_matrix) = await gather(*tasks)
        names, steamids, join_list, not_join_list = format_matrix(draft_matrix)
        
        if typ == "darla":
            response_list =  [join_list[i] or not_join_list[i]  for i in range(len(join_list))]
        else:
            response_list =  [join_list[i] for i in range(len(join_list))]
        
        #nested looplari azaltalim
        player_status_steam = {}
        player_status_name = {}

        for i, name in enumerate(names):
            if name in name_to_steam_map:
                steam_id = name_to_steam_map[name]
                player_status_steam[steam_id] = response_list[i]
                player_status_name[name] = response_list[i]

        return player_status_steam, player_status_name 

    async def not_coming(self) -> Tuple:

        draft_matrix = await self.get(c.SPREADSHEET_ID, c.DRAFT_RANGE)
        names, steamids, join_list, not_join_list = format_matrix(draft_matrix)

        msg_bck ="\n" #+ "\n".join(["".join(a) for i, a  in enumerate(liste) if join_list[i]])
        toplam = 0

        for i, isim in enumerate(names):
            if not_join_list[i]:
                msg_bck += "".join(isim) + "\n"
                toplam += 1

        return msg_bck, toplam
    async def add(self, steam_id = None, msg = None) -> str:
        tasks = [
        create_task(self.get_steam_to_name_map()),
        create_task(self.get(c.SPREADSHEET_ID, c.DRAFT_RANGE)), 
        ]

        (mapp, draft_matrix) = await gather(*tasks)
        if steam_id:
            name = mapp[steam_id].strip()
        
        names, steamids, join_list, not_join_list = format_matrix(draft_matrix)

        for i, isim in enumerate(names):
            #logger.debug(f"Steam Id:{steam_id}, Name from map: {name}, Match Candidate: {isim}")
            if (steam_id and "".join(isim).strip() == name) or (msg and "".join(isim).lower() in msg):
                join_list[i] = True 
                not_join_list[i] = False 
                draft_matrix = [list(x) for x in zip(join_list, not_join_list)]
                await self.update(c.SPREADSHEET_ID, c.DRAFT_UPDATE_RANGE, draft_matrix)
                return isim
        return None
    async def remove (self, steam_id:str = None, msg: str = None) -> str:
        tasks = [
            create_task(self.get_steam_to_name_map()),
            create_task(self.get(c.SPREADSHEET_ID, c.DRAFT_RANGE)), 
        ]

        (mapp, draft_matrix) = await gather(*tasks)
        if steam_id:
            name = mapp[steam_id].strip()

        names, steamids, join_list, not_join_list = format_matrix(draft_matrix)
        for i, isim in enumerate(names):
            if (steam_id and "".join(isim).strip() == name) or (msg and "".join(isim).lower() in msg):
                join_list[i] = False
                not_join_list[i] = True
                draft_matrix = [list(x) for x in zip(join_list, not_join_list)]
                await self.update(c.SPREADSHEET_ID, c.DRAFT_UPDATE_RANGE, draft_matrix)
                return isim

        return None 
    async def darla(self, members: List) -> str:
        steamid_map, _ = await self.get_player_status()

        darla_msg = f""
        for member in members:
            if not member.id in c.PLAYER_DISCORD:
                continue
            steam_id = c.PLAYER_DISCORD[member.id] 
            if steam_id in steamid_map and (not steamid_map[steam_id]):
                darla_msg += f"{member.mention}\n"

        return darla_msg

    async def get_steam_to_name_map(self) -> dict:
    
        player_ids = await self.get(c.SPREADSHEET_ID, c.PLAYER_IDS)
        steam_to_name_map = {}
        for row in player_ids:
            steam_to_name_map[row[0]] = row[1]
        return steam_to_name_map 

    async def get_name_to_steam_map(self) -> dict:
    
        player_ids = await self.get(c.SPREADSHEET_ID, c.PLAYER_IDS)
        name_to_steam_map = {}
        for row in player_ids:
            name_to_steam_map[row[1]] = row[0]
        return name_to_steam_map
       
   

from __future__ import print_function

from typing import List, Tuple

from google.oauth2 import service_account
from googleapiclient.discovery import build

import constants as c
from funs import format_matrix


class GSheet(object):
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        secret_file = 'secrets/credentials.json'
        self.creds = service_account.Credentials.from_service_account_file(secret_file, scopes=SCOPES)

        self.service = build('sheets', 'v4', credentials=self.creds)

    async def update(self, sheet_id: str, sheet_range: str, values: list[list[str]]):
        # Call the Sheets API
        sheet = self.service.spreadsheets()
        body = {
            'values': values
        }
        return sheet.values().update(
            spreadsheetId=sheet_id, range=sheet_range,
            valueInputOption='USER_ENTERED', body=body).execute()

    async def get(self, sheet_id: str, sheet_range: str):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id,
                                    range=sheet_range).execute()
        return result.get('values', [])

    async def get_player_status(self, typ: str = "darla") -> Tuple:

        draft_matrix = await self.get(c.SPREADSHEET_ID, c.DRAFT_RANGE)

        names, steam_ids, join_list, not_join_list = format_matrix(draft_matrix)

        if typ == "darla":
            response_list = [join_list[i] or not_join_list[i] for i in range(len(join_list))]
        else:
            response_list = [join_list[i] for i in range(len(join_list))]

        player_status_steam = {}
        player_status_name = {}

        for i, name in enumerate(names):
            steam_id = steam_ids[i]
            player_status_steam[steam_id] = response_list[i]
            player_status_name[name] = response_list[i]

        return player_status_steam, player_status_name

    async def not_coming(self) -> Tuple:

        draft_matrix = await self.get(c.SPREADSHEET_ID, c.DRAFT_RANGE)
        names, _, _, not_join_list = format_matrix(draft_matrix)

        msg_bck = "\n"  # + "\n".join(["".join(a) for i, a  in enumerate(liste) if join_list[i]])
        toplam = 0

        for i, isim in enumerate(names):
            if not_join_list[i]:
                msg_bck += "".join(isim) + "\n"
                toplam += 1

        return msg_bck, toplam

    async def add(self, steam_id=None, msg=None) -> [str, None]:
        draft_matrix = await self.get(c.SPREADSHEET_ID, c.DRAFT_RANGE)

        names, steamids, join_list, not_join_list = format_matrix(draft_matrix)

        for i, isim in enumerate(names):
            # logger.debug(f"Steam Id:{steam_id}, Name from map: {name}, Match Candidate: {isim}")
            if steam_id == steamids[i] or (msg and "".join(isim).lower() in msg):
                join_list[i] = True
                not_join_list[i] = False
                draft_matrix = [list(x) for x in zip(join_list, not_join_list)]
                await self.update(c.SPREADSHEET_ID, c.DRAFT_UPDATE_RANGE, draft_matrix)
                return isim
        return None

    async def remove(self, steam_id: str = None, msg: str = None) -> [str, None]:
        draft_matrix = await self.get(c.SPREADSHEET_ID, c.DRAFT_RANGE)

        names, steam_ids, join_list, not_join_list = format_matrix(draft_matrix)
        for i, isim in enumerate(names):
            if steam_id == steam_ids[i] or (msg and "".join(isim).lower() in msg):
                join_list[i] = False
                not_join_list[i] = True
                draft_matrix = [list(x) for x in zip(join_list, not_join_list)]
                await self.update(c.SPREADSHEET_ID, c.DRAFT_UPDATE_RANGE, draft_matrix)
                return isim

        return None

    async def darla(self, members: List) -> str:
        steam_id_map, _ = await self.get_player_status()

        darla_msg = f""
        for member in members:
            if member.id not in c.PLAYER_DISCORD:
                continue
            steam_id = c.PLAYER_DISCORD[member.id]
            if steam_id in steam_id_map and (not steam_id_map[steam_id]):
                darla_msg += f"{member.mention}\n"

        return darla_msg

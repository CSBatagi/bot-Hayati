from asyncio.tasks import sleep
from googleapiclient import discovery
from google.oauth2 import service_account
import constants as c


class GcpCompute:
    def __init__(self, zone, instance, subdomain):
        SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
        secret_file = 'secrets/credentials.json'
        self.creds = service_account.Credentials.from_service_account_file(secret_file, scopes=SCOPES)

        self.service = discovery.build('compute', 'v1')
        self.start_request = self.service.instances().start(project=c.project, zone=zone, instance=instance)
        self.stop_request = self.service.instances().stop(project=c.project, zone=zone, instance=instance)
        self.get_request = self.service.instances().get(project=c.project, zone=zone, instance=instance)
        self.subdomain = subdomain
        self.instance = instance

    async def start_instance(self, channel):

        if self.get_request.execute()['status'] != "RUNNING":
            await channel.send("Talimati verdim az beklicen.")
            time_elapsed = 0
            max_wait = 60 * 5
            while self.start_request.execute()['status'] != "DONE":
                await sleep(3)
                time_elapsed += 3
                if time_elapsed >= max_wait:
                    await channel.send("Serveri acamadim adminler bi baksin.")
                    return
            #server_ip = self.get_request.execute()['networkInterfaces'][0]['accessConfigs'][0]['natIP']
            if self.subdomain:
                connectstr = f"Konsola `connect {self.subdomain}.csbatagi.com;password hepayni` yazalim oyuna girelim."
            else: 
                connectstr = ""
            await channel.send(f"{self.instance} acildi." + connectstr)
        else:
            #server_ip = self.get_request.execute()['networkInterfaces'][0]['accessConfigs'][0]['natIP']
            await channel.send(f"Kardeslik, {self.instance} zaten acik. Konsola `connect {self.subdomain}.csbatagi.com;password hepayni` yazarsan isalleah.")

    async def stop_instance(self, channel):
        if self.get_request.execute()['status'] == "RUNNING":
            await channel.send("Talimati verdim uzun suruyor yanliz bu is.")
            time_elapsed = 0
            max_wait = 60 * 5
            self.stop_request.execute()
            while self.get_request.execute()['status'] != "TERMINATED":
                await sleep(3)
                time_elapsed += 3
                if time_elapsed >= max_wait:
                    await channel.send(f"{self.instance} kapanmiyor lan adminler bi baksin.")
                    return
            await channel.send(f"{self.instance} kapandi.")
        else:
            await channel.send(f"{self.instance} calismiyo ki olm.")


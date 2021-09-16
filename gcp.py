from googleapiclient import discovery 
from google.oauth2 import service_account
import constants as c

class GcpCompute:
    def __init__(self):
        secret_file = 'credentials.json'
        self.creds = service_account.Credentials.from_service_account_file(secret_file)    
        
        self.service = discovery.build('compute', 'v1')
     
    print('VM Instance started')
    def start_instance(self):
        print('VM Instance starting')
        request = self.service.instances().start(project=c.project, zone=c.zone, instance=c.instance)
        return request.execute()

    def stop_instance(self):
        request = self.service.instances().stop(project=c.project, zone=c.zone, instance=c.instance)
        return request.execute()

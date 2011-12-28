import unittest2
import helper
from hapi.leads import LeadsClient
import logger
import time

class LeadsClientTest(unittest2.TestCase):
    def setUp(self):
        self.client = LeadsClient(**helper.get_options())
    
    def tearDown(self):
        pass

    def test_camelcased_params(self):
        in_options = { 
                'sort': 'fce.convert_date', 
                'search': 'BlahBlah', 
                'time_pivot': 'last_modified_at', 
                'is_not_imported': True }
        out_options = { 
                'sort': 'fce.convertDate', 
                'search': 'BlahBlah', 
                'timePivot': 'lastModifiedAt', 
                'isNotImported': 'true' }
        self.assertEquals(out_options, self.client.camelcase_search_options(in_options))

    def test_get_leads(self):
        self.assertEquals(2, len(self.client.get_leads(max=2)))
        
    def test_open_lead(self):
        lead_guid = self.client.get_leads(timePivot='closedAt', startTime=0, max=1)[0]['guid']
        self.client.open_lead(lead_guid)
        time.sleep(3)
        self.assertEquals(False, self.client.get_lead(lead_guid)['isCustomer']) 
        
    def test_retrieve_lead(self):
        lead_guid = self.client.get_leads(timePivot='closedAt', startTime=0, max=1)[0]['guid']
        current_lead = self.client.retrieve_lead(lead_guid)
        time.sleep(3)
        lead_userToken = current_lead['userToken']
        #lead_conversionGuid = current_lead['conversionGuid']
        
        self.assertEquals(lead_guid, current_lead['guid'])
        self.assertEquals(lead_userToken, self.client.retrieve_lead(userToken="%s" %lead_userToken)['userToken'])
        #self.assertEquals(lead_conversionGuid, self.client.retrieve_lead(conversionGuid="%s" %lead_conversionGuid)['conversionGuid'])

        no_lead_guid = 0
        no_current_lead = self.client.retrieve_lead(no_lead_guid)
        time.sleep(3)
        self.assertEquals('-1', no_current_lead['guid'])

if __name__ == "__main__":
    unittest2.main()

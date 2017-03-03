import unittest
import subprocess
import json
import os.path

class OrcidBaseTest(unittest.TestCase):
    
    secrets_file_path = 'secrets'
    xml_data_files_path = '../ORCID-Source/orcid-integration-test/src/test/manual-test/'

    def orcid_curl(self, url, curl_opts):
        curl_call = ["curl"] + curl_opts + [url]
        #print " ".join(curl_call)
        p = subprocess.Popen(curl_call, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(subprocess.list2cmdline(curl_call))
        output,err = p.communicate()
        return output

    def save_secrets_to_file(self, content, code):
        with open(code + "." + self.secrets_file_path, 'w') as secrets_file:
            json.dump(content, secrets_file)

    def load_secrets_from_file(self, code):
        content = None
        with open(code + "." + self.secrets_file_path, 'r') as secrets_file:
            content = json.load(secrets_file)
        return content

    def orcid_exchange_auth_token(self, client_id, client_secret, code):
        json_response = None
        if not os.path.isfile(code + "." + self.secrets_file_path):
            exchange_data = ["-L", "-H", "Accept: application/json", "--data", "client_id=" + client_id + "&client_secret=" + client_secret + "&grant_type=authorization_code" + "&code=" + code + "&redirect_uri=https://developers.google.com/oauthplayground"]
            response = self.orcid_curl("http://pub.qa.orcid.org/oauth/token", exchange_data)
            json_response = json.loads(response)
        else:
            json_response = self.load_secrets_from_file(code)
        if(('access_token' in json_response) & ('refresh_token' in json_response)):
            self.save_secrets_to_file(json_response, code)
            return [json_response['access_token'],json_response['refresh_token']]
        else: 
            if('error-desc' in json_response):
                raise ValueError("No tokens found in response: " + json_response['error-desc']['value'])
        return [None, None]

    def orcid_generate_token(self, client_id, client_secret, scope="/read-public"):
        data = ['-L', '-H', 'Accept: application/json', '-d', "client_id=" + client_id, '-d', "client_secret=" + client_secret, '-d', 'scope=' + scope, '-d', 'grant_type=client_credentials']
        response = self.orcid_curl("http://pub.qa.orcid.org/oauth/token", data)
        json_response = json.loads(response)
        if('access_token' in json_response):
            return json_response['access_token']
        else: 
            if('error-desc' in json_response):
                print "No access token found in response: " + json_response['error-desc']['value']
        return None

    def orcid_generate_member_token(self, client_id, client_secret, scope="/read-public"):
        data = ['-L', '-H', 'Accept: application/json', '-d', "client_id=" + client_id, '-d', "client_secret=" + client_secret, '-d', 'scope=' + scope, '-d', 'grant_type=client_credentials']
        response = self.orcid_curl("http://api.qa.orcid.org/oauth/token", data)
        json_response = json.loads(response)
        if('access_token' in json_response):
            return json_response['access_token']
        else: 
            if('error-desc' in json_response):
                raise ValueError("No access token found in response: " + json_response['error-desc']['value'])
        return [None, None]

    def remove_by_putcode(self, putcode, activity_type = "work"):
        print "Deleting putcode: %s" % putcode
        curl_params = ['-L', '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml','-H', 'Authorization: Bearer ' + str(self.token), '-X', 'DELETE']
        response = self.orcid_curl("https://api.qa.orcid.org/v2.0/%s/%s/%s" % (self.orcid_id, activity_type, putcode), curl_params)
        return response

    def get_putcode_from_response(self, response):
        for header in response.split('\n'):
            if("Location:" in header):
                location_chunks = header.split('/')
                return location_chunks[-1]
        return False

    def post_activity(self, activity_type = "work", xml_file = "ma2_work.xml"):
        self.assertIsNotNone(self.access,"Bearer not recovered: " + str(self.access))
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + str(self.access), '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + xml_file, '-X', 'POST']
        response = self.orcid_curl("https://api.qa.orcid.org/v2.0/%s/%s" % (self.orcid_id, activity_type) , curl_params)
        return response
    
    def update_activity(self, putcode, updated_data, activity_type = "work"):
        update_curl_params = ['-i', '-L', '-k', '-H', 'Authorization: Bearer ' + str(self.access), '-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-d', updated_data, '-X', 'PUT']
        update_response = self.orcid_curl("https://api.qa.orcid.org/v2.0/%s/%s/%d" % (self.orcid_id, activity_type,int(putcode)), update_curl_params)
        return update_response
    
    def delete_activity(self, putcode, activity_type = "work"):
        delete_curl_params = ['-i', '-L', '-k', '-H', 'Authorization: Bearer ' + str(self.access), '-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-X', 'DELETE']
        delete_response = self.orcid_curl("https://api.qa.orcid.org/v2.0/%s/%s/%d" % (self.orcid_id, activity_type, int(putcode)), delete_curl_params)
        return delete_response
        
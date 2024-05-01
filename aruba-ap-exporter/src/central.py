import json
import os.path

from pycentral.base import ArubaCentralBase


class ArubaCentral(ArubaCentralBase):
    def __init__(self, token_folder):
        self.token_folder = token_folder
        central_info = self._findToken()
        super().__init__(central_info)

    def _findToken(self):
        for file in os.scandir(self.token_folder):
            if file.name[-4:] != 'json':
                continue
            with open(file.path) as fp:
                data = json.load(fp)
                if 'access_token' in data:
                    self.token_file = file.path
                    token = data
                if 'client_secret' in data:
                    self.secret_file = file.path
                    config = data
        central_info = config
        central_info['token']: token
        return central_info

    # def tokenLocalStoreUtil(self):
    #     path = os.path.dirname(__file__)
    #     return os.path.join(path, 'token.json')
    def loadToken(self):
        with open(self.token_file) as fp:
            token = json.load(fp)
        with open(self.secret_file) as fp:
            secret = json.load(fp)
            self.central_info.update(secret)
        return token

    def storeToken(self, token):
        with open(self.token_file, 'w') as fp:
            json.dump(token, fp)

    def get(self, apiPath, apiData={}, apiParams={}, headers={},
            files={}):
        return self.command('GET', apiPath, apiData, apiParams, headers, files)

    def command_helper(self, path, apiData={}, apiMethod='GET', **kwargs):
        response = self.command(apiMethod=apiMethod, apiPath=path, apiData=apiData, apiParams=kwargs)
        if response['code'] != 200:
            raise RuntimeError(response['msg']['error'])

        return response['msg']


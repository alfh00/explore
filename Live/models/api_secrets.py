

class ApiSecrets:
    def __init__(self, ob):
        self.public_api = ob['public_api']
        self.secret_api= ob['secret_api']
        self.password= ob['password']

    def __repr__(self):
        return str(vars(self))
    
    @classmethod
    def settings_to_str(cls, settings):
        ret_str = 'Api Secrets:\n'
        for _, v in settings.items():
            ret_str += f'{v}\n'
        ret_str += '\n'

        return ret_str
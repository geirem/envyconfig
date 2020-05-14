class Response:
    def __init__(self, s):
        self.payload = Payload(s)


class Payload:
    def __init__(self, s):
        self.data = bytearray(s, 'utf-8')


class MockSecrets:

    @staticmethod
    def access_secret_version(s: str):
        return Response(s)

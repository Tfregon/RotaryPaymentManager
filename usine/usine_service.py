from oads.oad_mensalidade import OADMensalidade
from services.service_mensalidade import ServiceMensalidade

class UsineService:
    @staticmethod
    def creer_service_mensalidade():
        uri = "SUA_STRING_DE_CONEXÃO_MONGODB_ATLAS"
        oad = OADMensalidade(uri)
        return ServiceMensalidade(oad)

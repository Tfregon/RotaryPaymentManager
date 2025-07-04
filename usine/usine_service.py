from oad.oad_payment import OADPayment
from service.service_payment import ServicePayment

class UsineService:
    @staticmethod
    def creer_service_mensalidade():
        uri = "mongodb+srv://root:root@cluster0.68qlr9t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        oad = OADPayment(uri)
        return ServicePayment(oad)
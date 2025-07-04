from tkinter import Tk
from usine.usine_service import UsineService
from interface.interface_main import InterfaceMensalidade

if __name__ == "__main__":
    root = Tk()
    service = UsineService.creer_service_mensalidade()
    app = InterfaceMensalidade(root, service)
    root.mainloop()

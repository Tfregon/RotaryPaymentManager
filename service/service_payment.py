class ServiceMensalidade:
    def __init__(self, oad_mensalidade):
        self.oad = oad_mensalidade

    def ajouter_mensalidade(self, nom, valeur, image_path=None):
        doc = {
            "nome_associado": nom,
            "valor_mensalidade": float(valeur),
            "imagem_comprovante": image_path or ""
        }
        return self.oad.inserer(doc)

    def lister(self):
        return self.oad.obtenir_tous()

    def supprimer(self, doc_id):
        return self.oad.supprimer(doc_id)

    def modifier(self, doc_id, champs):
        return self.oad.modifier(doc_id, champs)

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import base64
from PIL import Image, ImageTk
import io
from client.client_image import ClientImage  # Certifique-se de que esse import está certo

class InterfaceMensalidade:
    def __init__(self, root, service):
        self.root = root
        self.service = service
        self.root.title("Rotary Payment Manager")
        self.root.geometry("800x600")

        self.imagem_base64 = None

        # --- Formulário ---
        frame_form = tk.Frame(root)
        frame_form.pack(pady=10)

        tk.Label(frame_form, text="Nome do Associado").grid(row=0, column=0)
        self.entrada_nome = tk.Entry(frame_form, width=30)
        self.entrada_nome.grid(row=0, column=1, padx=5)

        tk.Label(frame_form, text="Valor (R$)").grid(row=1, column=0)
        self.entrada_valor = tk.Entry(frame_form, width=30)
        self.entrada_valor.grid(row=1, column=1, padx=5)

        btn_imagem = tk.Button(frame_form, text="Selecionar Imagem", command=self.selecionar_imagem)
        btn_imagem.grid(row=2, column=0, columnspan=2, pady=5)

        btn_salvar = tk.Button(frame_form, text="Salvar Mensalidade", command=self.salvar_mensalidade)
        btn_salvar.grid(row=3, column=0, columnspan=2, pady=10)

        btn_excluir = tk.Button(frame_form, text="Excluir Selecionado", command=self.excluir_mensalidade)
        btn_excluir.grid(row=4, column=0, columnspan=2, pady=5)

        # --- Lista de Registros ---
        frame_lista = tk.Frame(root)
        frame_lista.pack(fill="both", expand=True)

        self.tabela = ttk.Treeview(frame_lista, columns=("nome", "valor", "data"), show="headings")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("valor", text="Valor")
        self.tabela.heading("data", text="Data")
        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)

        # Evento de clique duplo para visualizar imagem
        self.tabela.bind("<Double-1>", self.ver_imagem)

        self.carregar_registros()

    def selecionar_imagem(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg")])
        if caminho:
            self.imagem_base64 = ClientImage.image_to_base64(caminho)
            messagebox.showinfo("Imagem", "Imagem carregada com sucesso!")

    def salvar_mensalidade(self):
        nome = self.entrada_nome.get()
        valor = self.entrada_valor.get()

        if not nome or not valor:
            messagebox.showwarning("Erro", "Preencha todos os campos.")
            return

        try:
            self.service.ajouter_mensalidade(nome, valor, self.imagem_base64)
            messagebox.showinfo("Sucesso", "Mensalidade salva com sucesso!")
            self.entrada_nome.delete(0, tk.END)
            self.entrada_valor.delete(0, tk.END)
            self.imagem_base64 = None
            self.carregar_registros()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    def carregar_registros(self):
        self.registros = self.service.lister()
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for r in self.registros:
            nome = r.get("nome_associado", "")
            valor = r.get("valor_mensalidade", 0)
            data = r.get("data_transacao", "")
            if isinstance(data, dict) and "$date" in data:
                data = data["$date"][:10]
            self.tabela.insert("", "end", values=(nome, f"R$ {valor:.2f}", data))

    def excluir_mensalidade(self):
        item = self.tabela.selection()
        if not item:
            messagebox.showwarning("Selecione", "Selecione um item para excluir.")
            return

        index = self.tabela.index(item)
        if index >= len(self.registros):
            return

        _id = self.registros[index].get("_id")
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta mensalidade?"):
            self.service.supprimer(str(_id))
            self.carregar_registros()

    def ver_imagem(self, event):
        item = self.tabela.selection()
        if not item:
            return

        index = self.tabela.index(item)
        if index >= len(self.registros):
            return

        registro = self.registros[index]
        imagem_b64 = registro.get("imagem_comprovante")
        if not imagem_b64:
            messagebox.showinfo("Sem imagem", "Este registro não possui comprovante.")
            return

        imagem = ClientImage.base64_to_image(imagem_b64)

        janela = tk.Toplevel(self.root)
        janela.title("Comprovante")
        imagem.thumbnail((400, 400))
        foto = ImageTk.PhotoImage(imagem)

        label = tk.Label(janela, image=foto)
        label.image = foto  # necessário manter referência para não apagar da memória
        label.pack(padx=10, pady=10)

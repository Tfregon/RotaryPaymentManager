import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import base64
from PIL import Image, ImageTk
import io

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

        # --- Lista de Registros ---
        frame_lista = tk.Frame(root)
        frame_lista.pack(fill="both", expand=True)

        self.tabela = ttk.Treeview(frame_lista, columns=("nome", "valor", "data"), show="headings")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("valor", text="Valor")
        self.tabela.heading("data", text="Data")
        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)

        self.carregar_registros()

    def selecionar_imagem(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg")])
        if caminho:
            with open(caminho, "rb") as img_file:
                self.imagem_base64 = base64.b64encode(img_file.read()).decode("utf-8")
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
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        try:
            registros = self.service.lister()
            for r in registros:
                nome = r.get("nome_associado", "")
                valor = r.get("valor_mensalidade", 0)
                data = r.get("data_transacao", "")
                if isinstance(data, dict) and "$date" in data:
                    data = data["$date"][:10]
                self.tabela.insert("", "end", values=(nome, f"R$ {valor:.2f}", data))
        except Exception as e:
            print(f"Erro ao carregar registros: {e}")



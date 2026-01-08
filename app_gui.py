import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
from datetime import datetime
import localPing
import query


class DeviceFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Device Finder - Localizador de Dispositivos")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.bg_color = "#f0f0f0"
        self.fg_color = "#333333"
        self.accent_color = "#2196F3"
        self.success_color = "#4CAF50"
        self.warning_color = "#FF9800"
        self.danger_color = "#f44336"
        
        self.root.config(bg=self.bg_color)
        
        query.inicializar_banco()
        
        self.criar_interface()
        
    def criar_interface(self):
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        self.aba_coleta = ttk.Frame(notebook)
        notebook.add(self.aba_coleta, text="📊 Coletar Dados")
        self.criar_aba_coleta()
        
        self.aba_historico = ttk.Frame(notebook)
        notebook.add(self.aba_historico, text="📋 Histórico")
        self.criar_aba_historico()
        
        self.aba_busca = ttk.Frame(notebook)
        notebook.add(self.aba_busca, text="🔎 Buscar")
        self.criar_aba_busca()
        
        self.aba_sobre = ttk.Frame(notebook)
        notebook.add(self.aba_sobre, text="ℹ️ Sobre")
        self.criar_aba_sobre()
    
    def criar_aba_coleta(self):

        main_frame = ttk.Frame(self.aba_coleta, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(
            main_frame, 
            text="Coletar Informações do Dispositivo",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=(0, 20))
        
        # Frame para botões
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.pack(pady=10)
        
        ttk.Button(
            botoes_frame,
            text="▶ Coletar e Salvar",
            command=self.coletar_dados
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            botoes_frame,
            text="👁️ Visualizar Dados",
            command=self.visualizar_dados_atuais
        ).pack(side=tk.LEFT, padx=5)
        
        # Text widget para resultado
        self.text_resultado = tk.Text(main_frame, height=20, width=80, font=("Courier", 10))
        self.text_resultado.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.aba_coleta, command=self.text_resultado.yview)
        self.text_resultado['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Pronto", foreground="green")
        self.status_label.pack(pady=(10, 0))
    
    def criar_aba_historico(self):
        main_frame = ttk.Frame(self.aba_historico, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(
            main_frame,
            text="Histórico de Pings",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=(0, 20))
        
        # Frame para botões
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.pack(pady=10)
        
        ttk.Button(
            botoes_frame,
            text="🔄 Atualizar",
            command=self.atualizar_historico
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            botoes_frame,
            text="🗑️ Limpar Banco",
            command=self.limpar_banco_dados
        ).pack(side=tk.LEFT, padx=5)
        
        # Treeview para mostrar dados
        cols = ("ID", "UUID", "Data/Hora", "Host", "IP Local", "IP Público", "SSID", "Internet", "Latitude", "Longitude")
        self.tree = ttk.Treeview(main_frame, columns=cols, height=15, show="headings")
        
        # Definir largura das colunas
        widths = [40, 100, 130, 80, 80, 80, 80, 50, 80, 80]
        for col, width in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
        
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree['xscrollcommand'] = scrollbar.set
        scrollbar.pack(fill=tk.X)
        
        # Status
        self.status_historico = ttk.Label(main_frame, text="Clique em 'Atualizar' para carregar dados")
        self.status_historico.pack(pady=(10, 0))
    
    def criar_aba_busca(self):
        main_frame = ttk.Frame(self.aba_busca, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(
            main_frame,
            text="Buscar Pings por UUID",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=(0, 20))
        
        # Frame de entrada
        entrada_frame = ttk.Frame(main_frame)
        entrada_frame.pack(pady=10)
        
        ttk.Label(entrada_frame, text="UUID:").pack(side=tk.LEFT, padx=5)
        self.entrada_uuid = ttk.Entry(entrada_frame, width=50)
        self.entrada_uuid.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            entrada_frame,
            text="🔎 Buscar",
            command=self.buscar_por_uuid
        ).pack(side=tk.LEFT, padx=5)
        
        # Treeview para resultados
        cols = ("ID", "UUID", "Data/Hora", "Host", "IP Local", "IP Público", "SSID", "Internet", "Latitude", "Longitude")
        self.tree_busca = ttk.Treeview(main_frame, columns=cols, height=15, show="headings")
        
        widths = [40, 100, 130, 80, 80, 80, 80, 50, 80, 80]
        for col, width in zip(cols, widths):
            self.tree_busca.heading(col, text=col)
            self.tree_busca.column(col, width=width)
        
        self.tree_busca.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.tree_busca.xview)
        self.tree_busca['xscrollcommand'] = scrollbar.set
        scrollbar.pack(fill=tk.X)
        
        # Status
        self.status_busca = ttk.Label(main_frame, text="Digite o UUID e clique em 'Buscar'")
        self.status_busca.pack(pady=(10, 0))
    
    def criar_aba_sobre(self):
        main_frame = ttk.Frame(self.aba_sobre, padding=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(
            main_frame,
            text="Device Finder",
            font=("Arial", 20, "bold")
        )
        titulo.pack(pady=(0, 20))
        
        # Texto sobre
        sobre_text = """
🔍 DEVICE FINDER - Localizador de Dispositivos

Versão 1.0

Um aplicativo para coletar e rastrear informações de dispositivos,
incluindo dados de rede, localização geográfica e configurações.

FUNCIONALIDADES:
• 📊 Coleta automática de dados do dispositivo
• 📋 Histórico completo de pings/localizações
• 🔎 Busca por UUID de hardware
• 🌐 Obtenção de IP local e público
• 📍 Localização geográfica via IP
• 💾 Armazenamento em banco de dados SQLite

DADOS COLETADOS:
✓ UUID do Hardware
✓ Nome do Host
✓ IP Local
✓ IP Público
✓ SSID (rede WiFi)
✓ Status da Internet
✓ Localização (Latitude/Longitude)
✓ Data e Hora (Fuso horário: São Paulo)

DESENVOLVIDO COM:
• Python 3.7+
• Tkinter (Interface Gráfica)
• SQLite (Banco de Dados)
• Socket (Conectividade)
        """
        
        texto = tk.Text(main_frame, height=20, width=80, font=("Arial", 10), wrap=tk.WORD)
        texto.insert(tk.END, sobre_text)
        texto.config(state=tk.DISABLED)
        texto.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def coletar_dados(self):
        """Coleta dados do dispositivo e salva no banco"""
        self.status_label.config(text="⏳ Coletando dados... Aguarde...", foreground="orange")
        
        def executar():
            try:
                # Coletar dados
                dados = localPing.montar_json_completo()
                
                # Inserir no banco
                sucesso, mensagem = query.inserir_ping(dados)
                
                if sucesso:
                    self.exibir_resultado(dados)
                    self.status_label.config(text="✅ Dados coletados e salvos com sucesso!", foreground="green")
                    messagebox.showinfo("Sucesso", mensagem)
                else:
                    self.status_label.config(text="❌ Erro ao salvar dados", foreground="red")
                    messagebox.showerror("Erro", mensagem)
                    
            except Exception as e:
                self.status_label.config(text="❌ Erro na coleta", foreground="red")
                messagebox.showerror("Erro", f"Erro ao coletar dados: {str(e)}")
        
        thread = threading.Thread(target=executar, daemon=True)
        thread.start()
    
    def visualizar_dados_atuais(self):
        """Visualiza os dados atuais sem salvar"""
        self.root.update()
        
        def executar():
            try:
                dados = localPing.montar_json_completo()
                self.exibir_resultado(dados)
                self.status_label.config(text="✅ Dados coletados!", foreground="green")
            except Exception as e:
                self.status_label.config(text="❌ Erro na coleta", foreground="red")
                messagebox.showerror("Erro", f"Erro: {str(e)}")
        
        thread = threading.Thread(target=executar, daemon=True)
        thread.start()
    
    def exibir_resultado(self, dados):
        """Exibe os dados coletados em formato JSON"""
        self.text_resultado.config(state=tk.NORMAL)
        
        resultado = json.dumps(dados, indent=4, ensure_ascii=False)
        self.text_resultado.insert("1.0", resultado)
        self.text_resultado.config(state=tk.DISABLED)
    
    def atualizar_historico(self):
        """Carrega e exibe o histórico de pings"""
        pings = query.obter_todos_pings()
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Inserir dados
        if pings:
            for ping in pings:
                self.tree.insert("", "end", values=ping)
            self.status_historico.config(text=f"✅ {len(pings)} ping(s) carregado(s)", foreground="green")
        else:
            self.status_historico.config(text="⚠️ Nenhum ping encontrado", foreground="orange")
    
    def buscar_por_uuid(self):
        """Busca pings de um UUID específico"""
        uuid = self.entrada_uuid.get().strip()
        
            messagebox.showwarning("Aviso", "Digite um UUID para buscar")
            return
        
        pings = query.obter_pings_por_uuid(uuid)
        
        # Limpar treeview
        for item in self.tree_busca.get_children():
            self.tree_busca.delete(item)
        
        # Inserir dados
        if pings:
            for ping in pings:
                self.tree_busca.insert("", "end", values=ping)
            self.status_busca.config(text=f"✅ {len(pings)} resultado(s) encontrado(s)", foreground="green")
        else:
            self.status_busca.config(text="❌ Nenhum ping encontrado com esse UUID", foreground="red")
    
    def limpar_banco_dados(self):
        """Limpa todos os dados do banco de dados"""
        resposta = messagebox.askyesno(
            "Confirmação",
        )
        
        if resposta:
            sucesso, mensagem = query.limpar_banco()
            
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.atualizar_historico()
            else:
                messagebox.showerror("Erro", mensagem)


def main():
    root = tk.Tk()
    app = DeviceFinderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

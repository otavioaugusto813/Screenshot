import os
import pyautogui
import sys
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkmacosx import Button

from constants import *


class PrintScreen:
    def __init__(self):
        self.root = Tk()
        self.root.resizable(0, 0)
        self.teste = {}
        self.funcionando = False
        self.contador = 0
        self.nome_arquivo = None  # incializa como None mas é alterada de acordo com o nome escolhido para o arquivo
        self.intervalo_tempo = None  # incializa como None mas é alterada de acordo com o intervalo escolhido
        self.current_directory = None

        # PRIMEIRA PARTE - INFORMAÇÕES INICIAIS
        app = tk.LabelFrame(self.root, text="Recadinho", borderwidth=4)
        app.grid()
        my_label_nome = tk.Label(app, text="Oi, gracinha! Digite o nome do seu print")
        my_label_nome.grid()
        my_label_tempo = tk.Label(app, text='Depois escolha o intervalo de tempo (:')
        my_label_tempo.grid()

        # SEGUNDA PARTE - ESCOLHA NOME ARQUIVO E INTERVALO DE TEMPO ENTRE OS PRINTS
        app2 = tk.LabelFrame(self.root, text="Opções", width=250, height=80, borderwidth=4)
        app2.grid()

        # NOME PASTA
        nome_print = tk.Label(app2, text='Nome do Print:')
        nome_print.grid()
        self.pasta = tk.Entry(app2, width=50)
        self.pasta.bind('<Return>', self.arquivo)
        self.pasta.grid(row=10, column=0)
        self.mostrar_nome = tk.Label(app2, text='')
        self.mostrar_nome.grid()

        # ESCOLHA TEMPO

        intervalo = tk.Label(app2, text='Intervalo:', justify='left')
        intervalo.grid()
        self.tempo = tk.Entry(app2, width=50)
        self.tempo.bind('<Return>', self.intervalo)
        self.tempo.grid(row=20, column=0)
        self.mostrar_tempo = tk.Label(app2, text='')
        self.mostrar_tempo.grid()

        escolher_pasta = Button(app2, text='Escolher pasta', bg='blue', fg='white', command=self.submit, borderwidth=3)

        escolher_pasta.grid(row=25, column=0)

        # TERCEIRA PARTE - EXECUÇÃO DOS PRINTS (INICIAR E INTERROMPER)

        app3 = tk.LabelFrame(self.root, text='Execução', height=200, width=200)

        botao_start = self.criar_botao(app3, "Iniciar!", '#24D34E', 'white', self.start)
        botao_interromper = self.criar_botao(app3, "Interromper", '#FF0A0A', 'white', self.stop)

        botao_start.grid(row=35, column=0)
        botao_interromper.grid(row=40, column=0)
        app3.grid()
        app4 = tk.LabelFrame(self.root, text="Status da Execução")
        self.status = tk.Label(app4, text="Inativo")
        self.status.grid()
        self.status_salvar = tk.Label(app4, text='')
        self.status_salvar.grid()
        app4.grid()

        # QUARTA PARTE - APAGAR VARIÁVEIS

        app5 = tk.LabelFrame(self.root, text='Apagar nome e tempo')
        botao_apagar = Button(app5, text='Zerar', command=self.apagar, bg='blue', fg='white', )
        botao_apagar.grid()
        self.mostrar_apagar = tk.Label(app5, text='')
        self.mostrar_apagar.grid()
        app5.grid()
        self.root.mainloop()

    def arquivo(self, evento):
        self.nome_arquivo = self.pasta.get().strip()
        if self.nome_arquivo in '' \
                or any(not c.isalnum() for c in self.nome_arquivo):  # Verifica se tem caracteres especiais
            self.mostrar_nome.config(text='Digite um nome válido',
                                     bg='red')
            self.nome_arquivo = None
            return self.nome_arquivo
        else:
            nome = f'O nome do seu arquivo é "{self.nome_arquivo}"'
            self.mostrar_nome.config(text=nome, bg='light green', borderwidth=5)
            self.mostrar_apagar.config(text='', bg='SystemButtonFace')
            print(self.nome_arquivo)
            return self.nome_arquivo

    def intervalo(self, evento):
        tempo = self.tempo.get().strip()
        teste = self.is_float(tempo)
        if teste:
            self.intervalo_tempo = float(tempo)
            self.intervalo_tempo = int(self.intervalo_tempo * UM_SEGUNDO)
            if self.intervalo_tempo == 0:
                self.mostrar_tempo.config(text='Valor inválido!', bg='red')
                self.intervalo_tempo = None
                self.tempo.delete(0, 'end')
                return False
            else:
                self.mostrar_tempo.config(text=f'Intervalo de {tempo} segundo(s)', bg='light green', borderwidth=5)
                self.mostrar_apagar.config(text='', bg='SystemButtonFace')
                print(self.intervalo_tempo)
                return self.intervalo_tempo
        else:
            self.mostrar_tempo.config(text='Valor inválido!', bg='red')
            self.intervalo_tempo = None
            self.tempo.delete(0, 'end')
            return False

    def submit(self):
        if self.nome_arquivo is not None and self.intervalo_tempo is not None:
            self.current_directory = filedialog.askdirectory()
            print(self.current_directory)
            return True
        if self.nome_arquivo is None and self.intervalo_tempo is None:
            self.mostrar_tempo.config(text='Digite o nome e o intervalo!', bg='yellow')
        elif self.nome_arquivo is not None and self.intervalo_tempo is not None:
            self.mostrar_tempo.config(text='Digite o intervalo')
        elif self.nome_arquivo is None and self.intervalo_tempo is not None:
            self.mostrar_tempo.config(text='Digite o nome do seu arquivo', bg='yellow')

    def start(self):
        """Permite o início da função tirar_print."""
        if self.nome_arquivo is None and self.intervalo_tempo is None:
            self.status.config(text='Escolha as opções primeiro!', bg='yellow')
        elif self.nome_arquivo is not None and self.intervalo_tempo is None:
            self.status.config(text='Falta o tempo!', bg='yellow')
        elif self.nome_arquivo is None and self.intervalo_tempo is not None:
            self.status.config(text='Falta o nome!', bg='yellow')
        elif self.nome_arquivo is not None and self.intervalo_tempo is not None \
                and self.current_directory is None:
            self.status.config(text='Escolha a pasta!', bg='yellow')
        elif self.nome_arquivo is not None and self.intervalo_tempo is not None \
                and self.current_directory is not None:
            self.funcionando = True
            self.status.config(text='Tirando prints!', bg='light green')
            self.atrasar_inicio()

    def atrasar_inicio(self):
        self.status.config(text='Tirando seus prints!', bg='light green')
        self.root.after(DOIS_SEGUNDOS, self.tirar_print)

    def tirar_print(self):
        if self.funcionando:
            self.contador += 1
            meu_print = pyautogui.screenshot()
            self.teste[f'{self.nome_arquivo}_{self.contador}'] = meu_print
            self.root.after(self.intervalo_tempo, self.tirar_print)  # em milissegundos

    def stop(self):
        self.root.after(TRES_SEGUNDOS, self.passar)
        """Muda a variável funcionando para False e interrompe a execução."""
        if self.funcionando and self.nome_arquivo is None and self.intervalo_tempo is None:
            self.status.config(text='Programa já parado', bg='yellow')
        elif self.funcionando:
            self.funcionando = False
            self.root.after(UM_SEGUNDO, self.interromper)
            self.salvar()
            self.teste.clear()

        elif not self.funcionando:
            self.status.config(text='Programa já parado', bg='yellow')

    def salvar(self):
        self.root.after(TRES_SEGUNDOS, self.passar)
        for k, v in self.teste.items():
            file_path = os.path.join(self.current_directory, f'{k}.png')
            v.save(file_path)
            self.root.after(MEIO_SEGUNDO, self.passar)
        self.status_salvar.config(text=f'Total de prints salvos: {len(self.teste)}', bg='light green')

    def interromper(self):
        """INÚTIL. FUNÇÃO VAZIA PARA O root.after"""
        self.status.config(text=f'Execução Interrompida!', bg='red')

    def apagar(self):
        """Apaga o nome do arquivo e o intervalo de tempo"""
        if self.nome_arquivo is not None or self.intervalo_tempo is not None:
            self.nome_arquivo = None
            self.intervalo_tempo = None
            self.pasta.delete(0, END)
            self.tempo.delete(0, END)
            self.mostrar_apagar.config(text='Nome e/ou intervalo zerados!', bg='light green')
            self.mostrar_nome.config(text='', bg="SystemButtonFace")
            self.mostrar_tempo.config(text='', bg="SystemButtonFace")
        elif self.nome_arquivo is None or self.intervalo_tempo is None:
            self.mostrar_apagar.config(text='As opções já estão zeradas', bg='yellow')

    def passar(self):
        ...

    @staticmethod
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    @staticmethod
    def criar_botao(app_name, text, bg, fg, cmd):
        if sys.platform == MAC_OS:
            return Button(app_name, text=text, bg=bg, fg=fg,
                          command=cmd)
        else:
            return tk.Button(app_name, text=text, bg=bg,
                             command=cmd, width=20, height=4, borderwidth=3)

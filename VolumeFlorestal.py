from tkinter import *
from tkinter import messagebox
import math
import pandas as pd

def calcular_volume():
    """Função para calcular o volume de uma árvore com base em inputs manuais."""
    try:
        get_diametro = float(diametro_altura_do_peito.get()) / 100  # Converter para metros
        get_altura = float(altura_maxima.get())
        get_fator_forma = float(fator_de_forma.get())

        # Validar se o fator de forma está dentro do intervalo permitido
        if get_fator_forma <= 0 or get_fator_forma > 1:
            raise ValueError("O fator de forma deve ser maior que 0 e menor ou igual a 1.")

        # Cálculo do volume
        volume = ((math.pi * get_diametro**2) / 4) * get_fator_forma * get_altura

        # Exibir o resultado
        resultado_label.config(text=f"Volume calculado: {volume:.2f} m³")
    except ValueError as ve:
        messagebox.showerror("Erro de Entrada", f"Entrada inválida: {ve}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def create_and_fetch_db():
    """Executar comandos SQL para criar a tabela e seus registros."""
    from sqlalchemy import create_engine, inspect

    engine = create_engine('sqlite:///:memory:')
    #engine = create_engine('sqlite:///dados_volume.db')
    url = "dados_volume.xlsx"
    dados = pd.read_excel(url)
    dados.to_sql('caracteres_especies', con=engine, index=False)
    inspector = inspect(engine)

    query = 'SELECT Especie FROM caracteres_especies'
    especies = pd.read_sql(query, engine)

    query = 'SELECT Diametro FROM caracteres_especies'
    diametros = pd.read_sql(query, engine)

    query = 'SELECT Altura FROM caracteres_especies'
    alturas = pd.read_sql(query, engine)

    query = 'SELECT FatorForma FROM caracteres_especies'
    fatores_de_forma = pd.read_sql(query, engine)

    return especies, diametros, alturas, fatores_de_forma

def calcular_volume_pela_tabela(diametros, alturas, fatores_de_forma):
    """Calcular o volume total da comunidade com base na tabela."""
    volumes = []
    for i in range(len(diametros)):
        volume_da_vez = ((math.pi * diametros.iloc[i, 0]**2) / 4) * fatores_de_forma.iloc[i, 0] * alturas.iloc[i, 0]
        volumes.append(volume_da_vez)
    volume_comunidade = sum(volumes)
    return volume_comunidade

if __name__ == "__main__":
    # Criar a base de dados e calcular o volume da comunidade
    especies, diametros, alturas, fatores_de_forma = create_and_fetch_db()
    volume_comunidade = calcular_volume_pela_tabela(diametros, alturas, fatores_de_forma)

    # Configuração da janela principal
    root = Tk()
    root.title("Calculador de Volume Florestal")
    root.geometry("500x400")
    root.config(padx=20, pady=20, bg="white")

    # Título principal
    titulo = Label(root, text="Cálculo de Volume", font=("Arial", 16, "bold"), bg="white")
    titulo.pack(pady=10)

    # Separador para cálculo manual
    frame_manual = LabelFrame(root, text="Cálculo Manual", font=("Arial", 12), bg="white", padx=10, pady=10)
    frame_manual.pack(fill="x", pady=10)

    # Inputs para cálculo manual
    Label(frame_manual, text="Diâmetro (cm):", bg="white").grid(row=0, column=0, sticky="w")
    diametro_altura_do_peito = Entry(frame_manual, width=10, highlightbackground="gray", highlightthickness=1, relief="flat")
    diametro_altura_do_peito.grid(row=0, column=1, padx=10, pady=5)

    Label(frame_manual, text="Altura (m):", bg="white").grid(row=1, column=0, sticky="w")
    altura_maxima = Entry(frame_manual, width=10, highlightbackground="gray", highlightthickness=1, relief="flat")
    altura_maxima.grid(row=1, column=1, padx=10, pady=5)

    Label(frame_manual, text="Fator de Forma:", bg="white").grid(row=2, column=0, sticky="w")
    fator_de_forma = Entry(frame_manual, width=10, highlightbackground="gray", highlightthickness=1, relief="flat")
    fator_de_forma.grid(row=2, column=1, padx=10, pady=5)

    Button(frame_manual, text="Calcular", command=calcular_volume).grid(row=3, column=0, columnspan=2, pady=10)

    # Resultado do cálculo manual
    resultado_label = Label(frame_manual, text="", font=("Arial", 12), bg="white")
    resultado_label.grid(row=4, column=0, columnspan=2)

    # Separador para volume da comunidade
    frame_comunidade = LabelFrame(root, text="Volume da Comunidade", font=("Arial", 12), bg="white", padx=10, pady=10)
    frame_comunidade.pack(fill="x", pady=10)

    Label(frame_comunidade, text=f"Volume total: {volume_comunidade:.2f} m³", font=("Arial", 12), bg="white").pack()

    # Iniciar o loop principal da interface
    root.mainloop()


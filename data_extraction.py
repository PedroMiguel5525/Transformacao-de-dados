from tabula import read_pdf
import pandas as pd
from zipfile import ZipFile, ZIP_DEFLATED
import os

current_directory = os.path.dirname(os.path.abspath(__file__))  # usei o diretório do arquivo para realizar os testes

pdf_path = "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"

# a tabula consegue ler todas as tabelas no pdf que são separadas em uma lista de dataframes

dfs = read_pdf(
    pdf_path,
    pages="3-181",
    pandas_options={"header":None},
    encoding="latin-1"
    )

processed_dfs = []

# com o pandas é possível tirar as linhas com o cabeçalho das tabelas e concatenar tudo em um dataframe só

for df in dfs:

    df = df.iloc[1:]
    processed_dfs.append(df)

header_df = ["Procedimento","RN (alteração)","Vigência","Seg. Odontológica","Seg. Ambulatorial","HCO","HSO","REF","PAC","DUT","SUBGRUPO","GRUPO","Capítulo"]

final_df = pd.concat(processed_dfs, ignore_index=True)
final_df.columns = header_df

# as mudanças solicitadas nas colunas

final_df['Seg. Odontológica'] = final_df['Seg. Odontológica'].map({'OD':'Seg. Odontológica'})
final_df['Seg. Ambulatorial'] = final_df['Seg. Ambulatorial'].map({'AMB':'Seg. Ambulatorial'})

# por fim o dataframe é salvo em csv e zipado

final_df.to_csv(
    "Anexo_1.csv",
    sep=';',
    na_rep='None',
    index=False,
    columns=header_df,
    encoding='latin-1'
    )

zip = ZipFile("Teste_Pedro.zip","w",compression=ZIP_DEFLATED)
zip.write(os.path.join(current_directory,"Anexo_1.csv"),"Anexo_1.csv")
os.remove('{}/{}'.format(current_directory, "Anexo_1.csv"))

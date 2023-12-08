#IMPORT DE BIBLIOTECAS
import streamlit as st 
import pandas as pd
import altair as alt
from PIL import Image
from IPython.display import display

st.set_page_config(layout='wide')

@st.cache_data
def gerar_df():
    
    #leitura do arquivo diretamente da base de dados da ANP,
    # removendo as linhas de introdução do documento
    serieHistMensal = pd.read_excel(io="https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/precos-revenda-e-de-distribuicao-combustiveis/shlp/mensal/mensal_estados-desde_jan2013.xlsx",engine='openpyxl',skiprows = range(0, 15))
    
    #Passando Primeira linha como coluna
    serieHistMensal.columns = serieHistMensal.loc[0]
    #excluindo a linha de cabeçalhos
    serieHistMensal.drop(0,axis=0,inplace=True)
    #Criando uma base de dados tratada
    #serieHistMensal.to_excel("data_base/serieHistMensal.xlsx",index=False)

    colunasUteis = ['MÊS','PRODUTO','REGIÃO','ESTADO','PREÇO MÉDIO REVENDA']
    serieHistMensal['MÊS'] = pd.to_datetime(serieHistMensal['MÊS'],format="%d-%m-%Y")
    serieHistMensal['MÊS'] = serieHistMensal['MÊS'].dt.strftime('%Y/%b')

    serieHistMensal = serieHistMensal[colunasUteis]
    return serieHistMensal

df = gerar_df()

with st.sidebar:
    st.subheader('Análise do Preço de Revenda de Combustíveis Líquidos\nno\nBrasil')
    logo_teste = Image.open('icone_combustivel.jpeg')
    st.image(logo_teste, use_column_width=True)
    st.subheader('SELEÇÃO DE FILTROS')
    fProduto = st.selectbox('Selecione o combustível:',options=df['PRODUTO'].unique())
    fEstado = st.selectbox('Selecione o Estado:',options=df['ESTADO'].unique())

    dadosUsuario = df.loc[(df['PRODUTO']== fProduto) & (df['ESTADO']==fEstado)]

st.header('PREÇOS DOS COMBUSTÍVEIS NO BRASIL: 2013 À 2023')
st.markdown('**Combustível selecionado: **'+fProduto)
st.markdown('**Estado: **'+fEstado)

graph_CombEstado = alt.Chart(dadosUsuario).mark_line(point=alt.OverlayMarkDef(color='red',size=20)).encode(x = 'MÊS:T',y='PREÇO MÉDIO REVENDA',strokeWidth = alt.value(3)).properties(height = 700,width=1350)

st.altair_chart(graph_CombEstado)
import streamlit as st
from fpdf import FPDF
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

load_dotenv()

def generate_pdf(content, name):
    file_path = f"{name}_dicas_financeiras.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.image('logo_qq.png', x=10, y=8, w=30)  # Assume que logo_qq.png está no diretório de trabalho
    pdf.set_xy(10, 40)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Dicas do Guru Financeiro da QueroQuitar para {name}", 0, 1, 'C')
    pdf.ln(20)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(file_path)
    return file_path

def generate_response(name, age, gender, location, state, job, income, stability, composition, assets, expenses, spending, short_term, medium_term, long_term, emergency, knowledge):
    template = (
        "Por favor, você é um expert em finanças e educação financeira e preciso que gere um relatório personalizado, em pdf, com dicas financeiras detalhadas baseadas nas respostas abaixo:\n"
        "Nome: {name}\n"
        "Idade: {age}\n"
        "Gênero: {gender}\n"
        "Localização: {location}\n"
        "Estado: {state}\n"
        "Trabalho: {job}\n"
        "Renda: {income}\n"
        "Estabilidade da renda: {stability}\n"
        "Composição da renda: {composition}\n"
        "Patrimônio: {assets}\n"
        "Gastos: {expenses}\n"
        "Onde estão os gastos: {spending}\n"
        "Objetivos financeiros de curto prazo: {short_term}\n"
        "Objetivos financeiros de médio prazo: {medium_term}\n"
        "Objetivos financeiros de longo prazo: {long_term}\n"
        "Fundo de emergência: {emergency}\n"
        "Conhecimento financeiro: {knowledge}\n"
        "Na primeira página do pdf, preciso que traga o resumo de todas as respostas que o cliente forneceu, na ordem acima."
        "Na segunda página, inicie com 'Prezado(a) {name}\n\n, Agradecemos por compatilhar suas informações conosco. Com base nas suas respostas, elaboramos algumas dicas financeiras personalizadas para ajudá-lo(a) a alcançar seus objetivos e melhoras sua situação financeira.\n\n A partir daqui comece a gerar as dicas personalizadas para o cliente."
        "Leve em consideração a IDADE, o ESTADO, o TRABALHO, a RENDA e demais itens na sua resposta. Gere dicas bem interessantes e amigáveis. Se puder, gere tabelas, no estilo excel, para ilustrar mais as dicas. Se puder, traga link de sites/portais etc para ajudar ainda mais o cliente nas ajudas. É possível termos respostas bem interessantes olhando esses aspectos mais locais, por exemplo."
        "Em cada item que gerar, cada bullet point, coloque em negrito o título do item e o resto sem negrito."
        "No final do arquivo PDF gerado colocar Atenciosamente\n, Guru Financeiro da QueroQuitar"
    )
    prompt = template.format(name=name, age=age, gender=gender, location=location, state=state,
                             job=job, income=income, stability=stability, composition=composition,
                             assets=assets, expenses=expenses, spending=spending,
                             short_term=short_term, medium_term=medium_term, long_term=long_term,
                             emergency=emergency, knowledge=knowledge)
    # Carrega a chave API do arquivo .env
    api_key = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(api_key=api_key, temperature=0, model="gpt-3.5-turbo-16k-0613")
    chain = LLMChain(llm=llm, prompt=PromptTemplate(input_variables=[], template=prompt))
    return chain.run({})

def main():
    st.set_page_config(page_title="Guru Financeiro QueroQuitar", page_icon=":currency:")
    st.markdown(
        """
        <style>
        .stApp {
            #background-color: #FF7F00;
            background-color: #6E3903;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.header("Guru Financeiro QueroQuitar")
    st.write("Olá, sou o Guru Financeiro da QueroQuitar e como uma inteligência artifical tenho a capacidade de gerar um relatório financeiro personalizado, exclusivamente para você de forma totalmente gratuita. Basta preencher o formulário abaixo, aceitar o termo e no final gerar o relatório. Vamos lá? * Perguntas de preenchimento obrigatório")

    with st.form("user_info"):
        name = st.text_input("Qual o seu nome? *")
        age = st.selectbox("Sua idade: *", ["Selecione", "Menor de 18 anos", "De 19 a 29 anos", "De 30 a 39 anos", "De 40 a 49 anos", "De 50 a 59 anos", "De 60 a 69 anos", "Maior ou igual a 70 anos"])
        gender = st.selectbox("Seu gênero: *", ["Selecione", "Masculino", "Feminino", "Outro", "Prefiro não responder"])
        location = st.selectbox("Onde mora? *", ["Selecione", "No Brasil", "Fora do Brasil"])
        state = st.selectbox("Em qual estado brasileiro? *", ["Selecione"] + ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])
        job = st.selectbox("Sobre o seu trabalho: *", ["Selecione", "Desempregado(a)", "Aposentado(a)", "Beneficiário(a) de algum programa do governo", "Funcionário Público", "Profissional CLT", "Profissional PJ", "Empreendedor(a)", "Em transição de carreira"])
        income = st.selectbox("Sobre sua faixa de renda mensal: *", ["Selecione", "Não possuo renda", "Até 1 salário mínimo", "Até 2 salários mínimos", "Até 3 salários mínimos", "4 a 8 salários mínimos", "9 a 12 salários mínimos", "13 a 20 salários mínimos", "Mais do que 20 salários mínimos"])
        stability = st.selectbox("Sobre a estabilidade da sua renda mensal: *", ["Selecione", "Não possuo renda","Minha renda é fixa", "Minha renda é variável", "Possuo tanto renda fixa quanto renda variável", "Minha renda é sazonal (temporária)"])
        composition = st.selectbox("Sobre a composição da sua renda mensal: *", ["Selecione", "Não possuo renda","Toda a minha renda vem do meu trabalho ou do governo", "Além da renda do trabalho, recebo renda de investimentos", "Além da renda do trabalho, recebo renda de aluguel de imóvel", "Além da renda do trabalho, recebo renda de outras fontes (não listadas nas opções anteriores)"])
        assets = st.multiselect("Sobre o seu patrimônio (selecione mais de uma opção se desejar): *", ["Não possuo nenhum bem, como casa, carro ou investimentos", "Possuo casa", "Possuo carro", "Possuo investimentos", "Possuo negócio próprio", "Possuo obras de arte ou bens de valor"])
        expenses = st.selectbox("Sobre os seus gastos mensais: *", ["Selecione", "Sempre gasto mais do que ganho", "Quase sempre gasto mais do que ganho", "Consigo, pelo menos, pagar todas as dívidas, mas não sobra nada ou quase nada", "Consigo economizar algum valor relevante"])
        spending = st.multiselect("Onde estão os seus gastos mensais (selecione mais de uma opção se desejar): *", ["Aluguel", "Farmácia", "Supermercado", "Transporte público", "Plano de celular", "Plano de internet em casa", "Serviços de entretenimento (netflix, disney+ etc)", "Viagens", "Cultura", "Educação", "Pagamento de dívidas em geral que não consegui pagar até o vencimento"])
        short_term = st.multiselect("Objetivos financeiros para o curto prazo - em até 6 meses (selecione mais de uma opção se desejar): *", ["Pretendo pagar minhas dívidas", "Pretendo quitar meu imóvel", "Pretendo quitar meu carro", "Pretendo quitar meus estudos", "Quero começar a investir", "Ampliar meus investimentos", "Outro"])
        medium_term = st.multiselect("Objetivos financeiros para o médio prazo - 6 meses a 1 ano (selecione mais de uma opção se desejar): *", ["Pretendo pagar minhas dívidas", "Pretendo quitar meu imóvel", "Pretendo quitar meu carro", "Pretendo quitar meus estudos", "Quero começar a investir", "Ampliar meus investimentos", "Outro"])
        long_term = st.multiselect("Objetivos financeiros para o longo prazo - mais do que 1 ano (selecione mais de uma opção se desejar): *", ["Pretendo pagar minhas dívidas", "Pretendo quitar meu imóvel", "Pretendo quitar meu carro", "Pretendo quitar meus estudos", "Quero começar a investir", "Ampliar meus investimentos", "Outro"])
        emergency = st.selectbox("Emergência Financeira: Você possui algum fundo de emergência/reserva ou capacidade para lidar com imprevistos financeiros? *", ["Selecione", "Sim", "Não"])
        knowledge = st.selectbox("Qual o seu nível de conhecimento com conceitos de educação financeira? *", ["Selecione", "Nenhum", "Pouco", "Intermediário", "Avançado"])

        acceptance = st.checkbox("Aceito fornecer meus dados em troca de dicas financeiras personalizadas.", key="acceptance")
        submitted = st.form_submit_button("Gerar relatório personalizado")

    if submitted and acceptance:
        response = generate_response(name, age, gender, location, state, job, income, stability, composition, assets, expenses, spending, short_term, medium_term, long_term, emergency, knowledge)
        file_path = generate_pdf(response, name)
        with open(file_path, "rb") as file:
            st.download_button("Baixar Relatório PDF", file, file_name=file_path)
        os.remove(file_path)  # Opcional: remover o arquivo após o download
    elif submitted and not acceptance:
        st.error("Você deve aceitar os termos para gerar o relatório.")

if __name__ == '__main__':
    main()    

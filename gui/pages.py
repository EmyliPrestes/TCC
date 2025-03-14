import streamlit as st
import cv2
from ml import modelo
import time
from tempfile import NamedTemporaryFile
from pathlib import Path
from db import db

from PIL import Image





def home():
    st.markdown(
        """
        <div style="background-color: #ac9c8f; padding: 20px; border-radius: 10px; box-shadow: 0 9px 50px rgba(0, 0, 0, 0.6);">
            <h2 style="color:white;">Sobre o Projeto</h2>
            <p style='color:white'>Bem-vindo ao site dedicado à detecção de Equipamentos de Proteção Individual (EPIs), desenvolvido como parte do Trabalho de Conclusão de Curso (TCC) da aluna <span style='color:red'>Emyli Beatriz Braga Prestes</span>. Este projeto é um componente essencial do curso de Tecnologia em Eletrônica Industrial, oferecido pelo <span style='color:green'>Instituto Federal do Amazonas Campus Manaus Distrito Industrial</span>. Sob a orientação do Professor Alexandre Lopes Martiniano, foi criado uma solução inovadora para a identificação automática de EPIs, utilizando tecnologias avançadas de visão computacional.</p>
            <p style='color:white'>O objetivo principal é aumentar a segurança no ambiente industrial, garantindo que todos os trabalhadores estejam devidamente equipados com os EPIs necessários para suas atividades. Este sistema automatizado de detecção pode ser integrado a câmeras de segurança existentes, proporcionando uma maneira eficiente e precisa de monitorar o uso de EPIs em tempo real.</p>
            <p style='color:white'>Esperamos que este projeto não só demonstre as habilidades técnicas desenvolvidas ao longo do curso, mas também contribua para a segurança e bem-estar dos profissionais na indústria. Agradecemos por visitar nosso site e por seu interesse em nosso trabalho.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def page1():
    st.markdown("<h1 style='color:white;'>Detecção com Câmera ao Vivo</h1>", unsafe_allow_html=True)

    run = st.checkbox('Ativar câmera')

    FRAME_WINDOW = st.image([])

    camera = None
    if run:
        camera = cv2.VideoCapture(0)
        
    while run:
        if camera:
            ret, frame = camera.read()
            if not ret:
                st.error("Falha ao capturar imagem da câmera.")
                break

            # Realizar a detecção usando o modelo treinado
            results= modelo.detect(frame)

            # Desenhar retângulos ou outras anotações na imagem, se necessário
            if results:
                for result in results:
                    for box in result.boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        assert len(box.cls) == 1
                        nome_equipamento_detectado = result.names[int(box.cls[0])]
                        color = (255, 0, 0)
                    
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                        (text_width, text_height), baseline = cv2.getTextSize(nome_equipamento_detectado, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)

                        cv2.rectangle(frame, (x1, y1 - text_height - baseline), (x1 + text_width, y1), color, -1)
                        cv2.putText(frame, nome_equipamento_detectado, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Converte o frame de BGR para RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Exibir a imagem com as detecções
            FRAME_WINDOW.image(frame)

            # Adicionar um pequeno atraso para permitir atualização da interface
            # time.sleep(0.1)

    if camera:
        camera.release()

def page2():
    st.markdown("<h1 style='color:white;'>Detecção de EPIs em FOTO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:white;'Tirar Foto</p>", unsafe_allow_html=True)

    

    '''uploaded_file = st.file_uploader("Escolha um arquivo", type=["jpg", "jpeg", "png"])'''

    botao = st.button('Tirar Foto')

    if botao:
        
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        
        if not ret:
            st.error("Falha ao capturar imagem da câmera.")
                
        else:
                
            with NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                cv2.imwrite(tmp_file.name, frame)
                    
            modelo.predict(tmp_file.name)
            
            Path(tmp_file.name).unlink()
           
            st.image('result.jpg', caption='Detecções', use_column_width=True)





     
    
def check_list_page():
    st.markdown("<h1 style='color:white;'>CheckList EPI</h1>", unsafe_allow_html=True)
    
    setores_equipamentos = db.listar_setores()
    setores = list(setores_equipamentos.keys())

    setor_selecionado = st.selectbox("Escolha um setor", setores)
    checkboxes_estado = {}

    # Mostrar a checklist de acordo com o setor selecionado
    if setor_selecionado:
        st.subheader(f"Equipamentos para o setor: {setor_selecionado}")
        equipamentos_obrigatorios = setores_equipamentos[setor_selecionado]
        
        if equipamentos_obrigatorios:
            for equipamento in equipamentos_obrigatorios:
                checkboxes_estado[equipamento] = st.empty()  # Cria um slot vazio para cada checkbox
                checkboxes_estado[equipamento].checkbox(equipamento, value=False, disabled=True)
        else:
            st.write("Nenhum equipamento encontrado para este setor.")

    st.markdown("<p style='color:white;'>Informações da Detecção</p>", unsafe_allow_html=True)
    run = st.checkbox('Ativar Detecção')
    texto_acesso = st.empty()
    frames_deteccao = st.empty()
    texto_acesso.text("")
    frames_deteccao.text("")

    camera = None
    if run and setor_selecionado:
        camera = cv2.VideoCapture(0)

        NUM_FRAMES_DETECCAO = 120
        todos_equipamentos_detectados = False
        contador_frames = 0
        equipamentos_detectados = []
        while not todos_equipamentos_detectados and contador_frames <= NUM_FRAMES_DETECCAO:
            if camera:
                ret, frame = camera.read()
                if not ret:
                    st.error("Falha ao capturar imagem da câmera.")
                    break

                # Realizar a detecção usando o modelo treinado
                results = modelo.detect(frame)
                
                # Desenhar retângulos ou outras anotações na imagem, se necessário
                if results:
                    for result in results:
                        for box in result.boxes:
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            assert len(box.cls) == 1
                            nome_equipamento_detectado = result.names[int(box.cls[0])]
                            
                            if nome_equipamento_detectado not in equipamentos_detectados and nome_equipamento_detectado in equipamentos_obrigatorios:
                                equipamentos_detectados.append(nome_equipamento_detectado)
                                checkboxes_estado[nome_equipamento_detectado].checkbox(nome_equipamento_detectado, value=True, disabled=True)
                            
                                color = (255, 0, 0)
                                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                                (text_width, text_height), baseline = cv2.getTextSize(nome_equipamento_detectado, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)

                                cv2.rectangle(frame, (x1, y1 - text_height - baseline), (x1 + text_width, y1), color, -1)
                                cv2.putText(frame, nome_equipamento_detectado, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                                # Converte o frame de BGR para RGB
                                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                FRAME_WINDOW = st.image([])
                                # Exibir a imagem com as detecções
                                FRAME_WINDOW.image(frame)

            if set(equipamentos_obrigatorios) == set(equipamentos_detectados):
                todos_equipamentos_detectados = True
                
            contador_frames += 1
            texto_acesso.text("Acesso em análise...")
            frames_deteccao.text(f"Frames analisados: {contador_frames}/{NUM_FRAMES_DETECCAO}")

        if todos_equipamentos_detectados:
            texto_acesso.text("Acesso Permitido!")
            frames_deteccao.text(f"Frames analisados: {contador_frames}/{NUM_FRAMES_DETECCAO}")
        else:
            texto_acesso.text("Acesso Negado!")
            frames_deteccao.text(f"Frames analisados: {contador_frames}/{NUM_FRAMES_DETECCAO}")

        if camera:
            camera.release()

    """
    criar uma janela de n frames para detectar os equipamentos listados durante x frames, caso detectado mostrar na tela acesso permitido, caso contrário acesso negado
    """

def sector_page():
    st.header("Gerenciamento de Setores e Equipamentos")

    # Seção para Inserir Equipamentos
    st.subheader("Inserir Equipamento")
    with st.form("equipamento_form"):
        nome_equipamento = st.text_input("Nome do Equipamento")
        submit_equipamento = st.form_submit_button("Inserir Equipamento")
        
        if submit_equipamento:
            if nome_equipamento:
                db.inserir_equipamento(nome_equipamento)
                st.success(f"Equipamento '{nome_equipamento}' inserido com sucesso!")
                st.experimental_rerun()
            else:
                st.error("Por favor, insira um nome para o equipamento.")

    # Seção para Visualizar e Deletar Equipamentos
    st.subheader("Equipamentos Existentes")
    equipamentos = db.listar_equipamentos()
    
    if equipamentos:
        for equipamento in equipamentos:
            with st.expander(f"{equipamento}"):
                if st.button(f"Deletar {equipamento}", key=f"del_eq_{equipamento}"):
                    db.excluir_equipamento(equipamento)
                    st.warning(f"Equipamento '{equipamento}' deletado com sucesso!")
                    st.experimental_rerun()
    else:
        st.write("Nenhum equipamento encontrado.")

    # Seção para Inserir Setores
    st.subheader("Inserir Setor")
    with st.form("setor_form"):
        nome_setor = st.text_input("Nome do Setor")
        equipamentos_disponiveis = db.listar_equipamentos()
        
        lista_de_equipamentos = st.multiselect("Selecione os Equipamentos", equipamentos_disponiveis)
        
        submit_setor = st.form_submit_button("Inserir Setor")
        
        if submit_setor:
            if nome_setor and lista_de_equipamentos:
                db.inserir_setor(nome_setor, lista_de_equipamentos)
                st.success(f"Setor '{nome_setor}' inserido com sucesso com os equipamentos selecionados!")
                st.experimental_rerun()
            else:
                st.error("Por favor, preencha todos os campos.")

    # Seção para Visualizar e Deletar Setores
    st.subheader("Setores Existentes")
    setores = db.listar_setores()
    
    if setores:
        for setor, equipamentos in setores.items():
            with st.expander(f"Setor: {setor}"):
                st.write("Equipamentos:")
                for equipamento in equipamentos:
                    st.write(f"- {equipamento}")
                if st.button(f"Deletar Setor {setor}", key=f"del_set_{setor}"):
                    db.excluir_setor(setor)
                    st.warning(f"Setor '{setor}' deletado com sucesso!")
                    st.experimental_rerun()
    else:
        st.write("Nenhum setor encontrado.")


def show_page(page_name):
    if page_name == "Sobre o Projeto":
        home()
    elif page_name == "Detecção com Câmera ao Vivo":
        page1()
    elif page_name == "Detecção de EPIs em Arquivo":
        page2()
    elif page_name== "TESTE":
        page3()
    elif page_name == "CheckList EPI":
        check_list_page()
    elif page_name == "Setores e Equipamentos":
        sector_page()

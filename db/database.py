import sqlite3
import json

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        
        # Cria tabela equipamentos caso não exista
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS equipamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
            )
        ''')
        # Cria tabela setores caso não exista
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS setores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                lista_de_equipamentos TEXT
            )
        ''')
        self.conn.commit()

    # CRUD para tabela equipamentos
    def inserir_equipamento(self, nome):
        
        try:
            self.cursor.execute('''
                INSERT INTO equipamentos (nome) 
                VALUES (?)
            ''', (nome,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f'Equipamento "{nome}" já existe.')

    def consultar_equipamento(self, id):
        
        self.cursor.execute('SELECT * FROM equipamentos WHERE id = ?', (id,))
        return self.cursor.fetchone()

    def listar_equipamentos(self):
        self.cursor.execute('SELECT * FROM equipamentos')
        return [equipamento[1] for equipamento in self.cursor.fetchall()]

    def excluir_equipamento(self, nome):
        self.cursor.execute('DELETE FROM equipamentos WHERE nome = ?', (nome,))
        self.conn.commit()

    # CRUD para tabela setores
    def inserir_setor(self, nome, lista_de_equipamentos_ids):
        equipamentos_json = json.dumps(lista_de_equipamentos_ids)
        self.cursor.execute('''
            INSERT INTO setores (nome, lista_de_equipamentos) 
            VALUES (?, ?)
        ''', (nome, equipamentos_json))
        self.conn.commit()

    def consultar_setor(self, id):
        
        self.cursor.execute('SELECT * FROM setores WHERE id = ?', (id,))
        setor = self.cursor.fetchone()
        
        if setor:
            id, nome, lista_de_equipamentos = setor
            lista_de_equipamentos_ids = json.loads(lista_de_equipamentos)
            return id, nome, lista_de_equipamentos_ids
        return None

    def obter_lista_equipamentos_setor(self, setor_id):
        # Consulta o setor pelo ID
        self.cursor.execute('''
            SELECT lista_de_equipamentos FROM setores WHERE id = ?
        ''', (setor_id,))
        
        # Recupera o resultado da consulta
        resultado = self.cursor.fetchone()
        
        if resultado:
            # Recupera a string JSON que representa a lista de equipamentos
            lista_de_equipamentos_json = resultado[0]
            
            # Converte a string JSON de volta para uma lista
            lista_de_equipamentos = json.loads(lista_de_equipamentos_json)
            
            return lista_de_equipamentos
        else:
            # Se o setor não for encontrado, retorna None ou uma lista vazia
            return None  # ou [] para uma lista vazia

    def atualizar_setor(self, id, nome=None, lista_de_equipamentos_ids=None):
        
        setor = self.consultar_setor(id)
        if not setor:
            print(f'Setor com ID {id} não encontrado.')
            return
        
        if nome is None:
            nome = setor[1]
        if lista_de_equipamentos_ids is None:
            lista_de_equipamentos_ids = setor[2]
        else:
            lista_de_equipamentos_ids = json.dumps(lista_de_equipamentos_ids)
        
        self.cursor.execute('''
            UPDATE setores
            SET nome = ?, lista_de_equipamentos = ?
            WHERE id = ?
        ''', (nome, lista_de_equipamentos_ids, id))
        self.conn.commit()

    def listar_setores(self):
        # Seleciona todos os setores com suas listas de equipamentos
        self.cursor.execute('''
            SELECT nome, lista_de_equipamentos FROM setores
        ''')
        
        # Recupera todos os resultados
        setores = self.cursor.fetchall()
        
        # Dicionário para armazenar os setores e suas listas de equipamentos
        dict_setores = {}
        
        for setor in setores:
            nome_setor, lista_de_equipamentos_json = setor
            
            # Converte a string JSON de volta para uma lista
            lista_de_equipamentos = json.loads(lista_de_equipamentos_json)
            
            # Extrai apenas os nomes dos equipamentos
            nomes_equipamentos = lista_de_equipamentos
            
            # Adiciona ao dicionário
            dict_setores[nome_setor] = nomes_equipamentos

        return dict_setores

    def excluir_setor(self, nome):
        try:
            self.cursor.execute('DELETE FROM setores WHERE nome = ?', (nome,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao excluir setor: {e}")
    

    def close(self):
        self.conn.close()

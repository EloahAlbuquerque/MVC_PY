#REFAZENDO O MÓDULO PARA ADEQUAÇÃO A INTERFACE DO THINKER
from database.db import Database
#from views.livro_view import LivroView
from models.livro import Livro
class LivroController:
    def __init__(self, db_config):
        #self.db = db_config
        self.db = Database(
            db_config["dbname"],
            db_config["user"],
            db_config["password"],
            db_config["host"],
            db_config["port"]
        )
        self.criar_tabela_se_nao_existir()
        #self.view = LivroView()
        
    def criar_tabela_se_nao_existir(self):
        conn = self.db.connect()
        if conn: 
            cur = conn.cursor()
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS livros(
                        ID SERIAL PRIMARY KEY,
                        titulo VARCHAR(50) NOT NULL,
                        autor VARCHAR(100) NOT NULL,
                        ano INTEGER,
                        ISBN VARCHAR(14)
                            );
            """)
            conn.commit()
            cur.close()
            conn.close()
    def adicionar_livro(self, id, titulo, autor, ano, isbn):
        conn = self.db.connect()
        if conn:
            cur = conn.cursor() #CUR É UM OBJETO CRIADO A PARIR DE UMA CONEXÃO COM O BANCO DE DADOS
            #EXECUTE(): MÉTODO DO CURSOR QUE EXECUTA UMA CONSULTA SQL PASSADA POR ARGUMENTO
            cur.execute(
                #%s É UM PLACEHOLDER QUE SERÁ SUBSTITUÍDO PELOS VALORES DA TUPLA A SEGUIR.
                #O PSYCOPG2 SUBSTITUI ESSE %s POR VALORES REAIS DE FORMA SEGURA, EVITANDO INJEÇÃO DE SQL
                "INSERT INTO livros(id, titulo, autor, ano, isbn) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING", (id, titulo, autor, ano, isbn))
            conn.commit() #CONFIRMA A TRANSAÇÃO, SALVANDO AS MUDANÇAS NO BANCO DE DADOS
            cur.close()
            conn.close()
            print("Livro adicionado com sucesso!")
        else:
            print("Erro ao conectar ao banco de dados.")
            
    def listar_livros(self):
        #self.view.mostrar_livros(livros)
        conn = self.db.connect()
        livros = []
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT id, titulo, autor, ano, isbn FROM livros ORDER BY id;")
            for linha in cur.fetchall():
                livros.append(Livro(*linha))
            cur.close()
            conn.close()
        return livros
                
        
      
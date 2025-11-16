from dao.db_config import get_db_connection

class AlunoDAO:

    sqlSelect = "SELECT id, nome, idade, cidade FROM aluno"

    def listar(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(self.sqlSelect)
        lista = cursor.fetchall()
        conn.close()
        return lista
    
    def salvar(self, id, nome, idade, cidade):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            if id:  # atualizar pois um valor para id foi informado
                cursor.execute('UPDATE aluno SET nome=%s, idade=%s, cidade=%s WHERE id=%s', (nome, idade, cidade, id))
            else:  # inserir novo registro
                cursor.execute('INSERT INTO aluno (nome, idade, cidade) VALUES (%s, %s, %s)', (nome, idade, cidade))
            conn.commit()
            return {"status": "ok"}
        except Exception as e:
            return {"status": "erro", "mensagem": f"Erro: {str(e)}"}
        finally:
            conn.close()

    def buscar_por_id(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, idade, cidade FROM aluno WHERE id = %s', (id,))
        registro = cursor.fetchone() # retorna o registro selecionado.
        conn.close()
        return registro

    def remover(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM aluno WHERE id=%s', (id,))
            conn.commit()
            return {"status": "ok"} 
        except Exception as e:
            return {"status": "erro", "mensagem": f"Erro: {str(e)}"}
        finally:
            conn.close()


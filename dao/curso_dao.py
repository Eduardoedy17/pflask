from dao.db_config import get_db_connection

class CursoDAO:

    sqlSelect = "SELECT id, nome_curso, duracao FROM curso"

    def listar(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(self.sqlSelect)
        lista = cursor.fetchall()
        conn.close()
        return lista
    
    def salvar(self, id, nome_curso, duracao):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO curso (nome_curso, duracao) VALUES (%s, %s)', (nome_curso, duracao))
            conn.commit()
            return {"status": "ok"}
        except Exception as e:
            return {"status": "erro", "mensagem": f"Erro: {str(e)}"}
        finally:
            conn.close()

    def atualizar(self, id, nome_curso, duracao):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE curso SET nome_curso = %s, duracao = %s WHERE id = %s', (nome_curso, duracao, id))
            conn.commit()
            return {"status": "ok"}
        except Exception as e:
            return {"status": "erro", "mensagem": f"Erro: {str(e)}"}
        finally:
            conn.close()

    def buscar_por_id(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome_curso, duracao FROM curso WHERE id = %s', (id,))
        curso = cursor.fetchone()
        conn.close()
        return curso

    def remover(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM curso WHERE id = %s', (id,))
            conn.commit()
            return {"status": "ok"}
        except Exception as e:
            return {"status": "erro", "mensagem": f"Erro: {str(e)}"}
        finally:
            conn.close()

    
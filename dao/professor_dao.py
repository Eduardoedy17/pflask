from dao.db_config import get_db_connection

class ProfessorDAO:

    sqlSelect = "SELECT id, nome, disciplina FROM professor"

    def listar(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(self.sqlSelect)
        lista = cursor.fetchall()
        conn.close()
        return lista
    
    def salvar(self, id, nome, disciplina):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            if id:  # atualizar pois um valor id foi informado
                cursor.execute('UPDATE professor SET nome=%s, disciplina=%s WHERE id=%s', (nome, disciplina, id))
            else:  # inserir novo registro  
                cursor.execute('INSERT INTO professor (nome, disciplina) VALUES (%s, %s)', (nome, disciplina))
            conn.commit()
            return {"status": "ok"}
        except Exception as e:
            return {"status": "erro", "mensagem": f"Erro: {str(e)}"}
        finally:
            conn.close()

    def buscar_por_id(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, disciplina FROM professor WHERE id = %s', (id,))
        registro = cursor.fetchone() # retorna o registro selecionado.
        conn.close()
        return registro

    def remover(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM professor WHERE id=%s', (id,))
            conn.commit()
            return {"status": "ok"}
        except Exception as e:
            return {"status": "erro", "mensagem": f"Erro: {str(e)}"}
        finally:
            conn.close()

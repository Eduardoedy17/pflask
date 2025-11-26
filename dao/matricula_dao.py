from dao.db_config import get_db_connection

class MatriculaDAO:
    def listar(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        # Traz o ID da matrícula, Nome do Aluno, Nome do Curso e Semestre da Turma
        sql = """
            SELECT m.id, a.nome, c.nome_curso, t.semestre
            FROM matricula m
            JOIN aluno a ON m.aluno_id = a.id
            JOIN curso c ON m.curso_id = c.id
            JOIN turma t ON m.turma_id = t.id
            ORDER BY m.id DESC
        """
        cursor.execute(sql)
        lista = cursor.fetchall()
        conn.close()
        return lista

    def salvar(self, id, aluno_id, curso_id, turma_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            if id: # Atualizar
                sql = "UPDATE matricula SET aluno_id=%s, curso_id=%s, turma_id=%s WHERE id=%s"
                cursor.execute(sql, (aluno_id, curso_id, turma_id, id))
            else: # Inserir Nova
                sql = "INSERT INTO matricula (aluno_id, curso_id, turma_id) VALUES (%s, %s, %s)"
                cursor.execute(sql, (aluno_id, curso_id, turma_id))
            conn.commit()
            return {"status": "ok"}
        except Exception as e:
            return {"status": "erro", "mensagem": str(e)}
        finally:
            conn.close()

    def buscar_por_id(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, aluno_id, curso_id, turma_id FROM matricula WHERE id = %s", (id,))
        item = cursor.fetchone()
        conn.close()
        return item

    def remover(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM matricula WHERE id = %s", (id,))
            conn.commit()
            return {"status": "ok"}
        except Exception as e:
            return {"status": "erro", "mensagem": str(e)}
        finally:
            conn.close()
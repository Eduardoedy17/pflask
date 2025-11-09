from dao.db_config import get_db_connection

class TurmaDAO:

    sqlSelect = """ SELECT t.id, semestre, nome_curso,  p.nome FROM turma t
                join curso c on c.id = t.curso_id
                join professor p on p.id  = t.professor_id """

    def listar(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(self.sqlSelect)
        lista = cursor.fetchall()
        conn.close()
        return lista
    
    def salvar(self, id, semestre, curso_id, professor_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO turma (semestre, curso_id, professor_id) VALUES (%s, %s, %s)', (semestre, curso_id, professor_id))
            conn.commit()
            return {"status": "ok"}
        except Exception as e:
            return {"status": "erro", "mensagem": f"Erro: {str(e)}"}
        finally:
            conn.close()
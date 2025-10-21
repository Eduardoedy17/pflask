from dao.db_config import get_db_connection

class TurmaDAO:

    sqlSelect = "SELECT id, semestre, curso_id, professor_id FROM turma"

    def listar(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(self.sqlSelect)
        lista = cursor.fetchall()
        conn.close()
        return lista
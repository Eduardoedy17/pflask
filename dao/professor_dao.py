from dao.db_config import get_db_connection

class ProfessorDAO:

    sqlSelect = "SELECT id, nome, disciplina FROM professor"

    def listar(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(self.sqlSelect)
        lista = cursor.fetchall()
        return lista

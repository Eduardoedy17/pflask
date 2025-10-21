from turma_dao import get_db_connection

class TurmaDAO:

    sqlSelect = "SELECT id, semestre, curso, professor FROM turma"

    def listar(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(self.sqlSelect)
        lista = cursor.fetchall()
        conn.close()
        return lista
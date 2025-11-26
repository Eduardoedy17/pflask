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
        """ Remove professor e suas dependências (Turmas e Matrículas dessas turmas) """
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # 1. Buscar IDs das turmas deste professor
            cursor.execute('SELECT id FROM turma WHERE professor_id = %s', (id,))
            turmas = cursor.fetchall()
            
            # 2. Para cada turma do professor, remover as matrículas (para não travar a exclusão da turma)
            for turma in turmas:
                turma_id = turma[0]
                cursor.execute('DELETE FROM matricula WHERE turma_id = %s', (turma_id,))
            
            # 3. Remover as turmas do professor
            cursor.execute('DELETE FROM turma WHERE professor_id = %s', (id,))

            # 4. Finalmente, remover o professor
            cursor.execute('DELETE FROM professor WHERE id=%s', (id,))
            
            conn.commit()
            return {"status": "ok"}
        except Exception as e:
            return {"status": "erro", "mensagem": f"Erro ao excluir professor: {str(e)}"}
        finally:
            conn.close()
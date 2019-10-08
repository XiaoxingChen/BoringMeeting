import sqlite3
import os

class SQLGlossary(object):
    def __init__(self, db_name='.glossary'):
        self.table_name = 'glossary'
        self.db_name = db_name
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS glossary
            (WORD TEXT PRIMARY KEY NOT NULL,
            DEFINITION  BLOB     NOT NULL,
            MEM_LEVEL   REAL     NOT NULL,
            PRONOUNCE   BLOB);''')
        conn.commit()
        conn.close()

    def ReplaceWord(self,word, definition, mem, audio=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        if audio is None:
            cursor.execute("REPLACE INTO glossary (WORD,DEFINITION,MEM_LEVEL) \
                VALUES (?, ?, ?)",  [word, definition, mem])
        else:
            cursor.execute("REPLACE INTO glossary (WORD,DEFINITION,MEM_LEVEL,PRONOUNCE) \
                VALUES (?, ?, ?, ?)",  [word, definition, mem, sqlite3.Binary(audio)])
        conn.commit()
        conn.close()

    def UpdateMemLevel(self, word, mem_level):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE glossary set MEM_LEVEL=? where WORD=? ",  [mem_level, word])
        conn.commit()
        conn.close()

    def Exists(self, words):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        results = []
        for word in words:
            cursor.execute('SELECT EXISTS(SELECT 1 FROM glossary WHERE WORD=?); ',  [word])
            results.append(cursor.fetchone()[0])
        conn.commit()
        conn.close()
        return results

    def FetchDefinitions(self, words):
        import yaml
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        definitions = []
        for word in words:
            cursor.execute('SELECT DEFINITION, MEM_LEVEL FROM glossary WHERE WORD=?;',  [word])
            def_in_yaml, mem_level = cursor.fetchone()
            definition = yaml.load(def_in_yaml)
            definition.mem_level = mem_level
            definitions.append(definition)
        conn.commit()
        conn.close()
        return definitions

    def FetchPronounce(self, word):
        import yaml
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT PRONOUNCE FROM glossary WHERE WORD=?;',  [word])
        pronounce = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return pronounce


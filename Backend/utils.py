import random 
import psycopg2



class uniqueID:
    def __init__(self, minNum, maxNum, db_info):
        self.minNum = minNum
        self.maxNum = maxNum
        self.db_info = db_info
        
    def genID(self):
        conn = psycopg2.connect(**self.db_info)
        cur = conn.cursor()

        newID=None
        while newID is None:
            newGenID = random.randint(self.minNum, self.maxNum)
            cur.execute("SELECT generated_id FROM unique_ids WHERE generated_id = %s", (newGenID,))
            result = cur.fetchone()
            if result is None:
                newID = newGenID
                cur.execute("INSERT INTO unique_ids (generated_id) VALUES (%s)", (newID,))
    
        
        conn.commit()
        cur.close()
        conn.close()
        return newID

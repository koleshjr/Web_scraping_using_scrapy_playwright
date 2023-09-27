import sqlite3
import copy
import json

class GroupedElementsPipeline:
    def __init__(self):
        self.elems = {}
    
    def process_item(self, item, spider):
        if item["chemical_group"] not in self.elems:
            self.elems[item["chemical_group"]] = {"element_count": 0, "elements": []}

        item_copy = copy.deepcopy(item)
        del item_copy["chemical_group"]
        self.elems[item["chemical_group"]]["elements"].append(dict(item_copy))
        self.elems[item["chemical_group"]]["element_count"] += 1
        return item
    
    def close_spider(self,spider):
        with open("grouped_elements.json", "w") as f:
            json.dump(self.elems, f, indent=2)

class ElemsPipeline:
    def __init__(self):
        self.conn = sqlite3.connect('elements.db')
        self.cursor= self.conn.cursor()

    def open_spider(self,spider):
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS elements(
                name TEXT,
                symbol TEXT PRIMARY KEY,
                atomic_number INTEGER,
                atomic_mass REAL,
                chemical_group TEXT
            )

            """
        )
        self.conn.commit()

    
    def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT OR IGNORE INTO elements VALUES(
                ?,?,?,?,?
            )
            """, (
                item['name'],
                item['symbol'],
                item['atomic_number'],
                item['atomic_mass'],
                item['chemical_group'])
        )
        self.conn.commit()
        return item
    
    def close_spider(self,spider):
        self.conn.close()


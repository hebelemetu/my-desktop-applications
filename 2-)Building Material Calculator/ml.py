import joblib
from dbase import Database
import numpy as np
db = Database('Database/building_db.db')

class ml_model:
    def __init__(self):
        self.db = Database('Database/building_db.db')

    def create_data_table(self):
        import pandas as pd
        import sqlite3
        self.db.drop_table_data()
        conn = sqlite3.connect('Database/building_db.db')
        dfs = pd.read_excel('Database/datafilled.xlsx', sheet_name=None,engine='openpyxl')
        for table, df in dfs.items():
            df.to_sql(table, conn)

    def predict(self,width,length,storey_height):
        width = round(width,2)
        length = round(length, 2)
        storey_height = round(storey_height, 2)
        if 0 < width <= 10.15:
            width = 1
        elif 10.15 < width <= 15.15:
            width = 2
        elif 15.15 < width <= 19.1:
            width = 3
        elif 19.1 < width < 51.7:
            width = 4
        else:
            width = 5

        if 0 < length <= 18.975:
            length = 1
        elif 18.975 < length <= 27.5:
            length = 2
        elif 27.5 < length <= 38.5:
            length = 3
        elif 38.5 < length < 78.5:
            length = 4
        else:
            length = 5

        if 0 < storey_height <= 3.85:
            storey_height = 1
        elif 3.85 < storey_height <= 5.2:
            storey_height = 2
        elif 5.2 < storey_height <= 7.425:
            storey_height = 3
        elif 7.425 < storey_height < 13.5:
            storey_height = 4
        else:
            storey_height = 5
        params = [width,length,storey_height]
        return params

    def predict_ml(self,width,length,storeyheight):
        width_model = 'Database/width_predict.joblib'
        length_model = 'Database/length.joblib'
        storey_model = 'Database/storey_height_predict.joblib'
        #width_model_load = joblib.load(width_model)
        #length_model_load = joblib.load(length_model)
        #storey_model_load = joblib.load(storey_model)
        #storey_model_load = joblib.load(storey_model)
        #width = width_model_load.predict(np.array([width]).reshape(1, 1))
        width = 1
        #length = length_model_load.predict(np.array([length]).reshape(1, 1))
        length = 1
        #storey_height = storey_model_load.predict(np.array([storeyheight]).reshape(1, 1))
        storey_height = 1
        #print("width: ",width[0])
        #print("length: ",length[0])
        #print("storeyheight: ",storey_height[0])
        params = [width,length,storey_height]
        return params

    def encode_parameters(self, structuraltype, foundationtype, foundation_beam,foundation_ground_wall, basement):
        structuraltype_dict = {"RC" : 0 , "STEEL": 1}
        foundationtype_dict = {"MAT": 0,"SINGLE_FOOTING": 1,"SINGLE_FOOTING(ONLY EDGE)": 2, "STRIP": 3}
        foundation_beam_dict = {"NO_BEAM": 0,"ONE_WAY": 1, "TWO_WAY": 3, "STRAP_BEAM": 2}
        foundation_ground_wall_dict = {"YES": 1, "NO": 0}
        basement_dict = {"YES": 1, "NO": 0}
        inputs = []

        for key,value in structuraltype_dict.items():
            if key == structuraltype:
                print("structural type: ",value)
                inputs.append(value)
        for key,value in foundationtype_dict.items():
            if key == foundationtype:
                print("foundation type: ",value)
                inputs.append(value)
        for key,value in foundation_beam_dict.items():
            if key == foundation_beam:
                print("foundation beam: ",value)
                inputs.append(value)
        for key,value in foundation_ground_wall_dict.items():
            if key == foundation_ground_wall:
                print("ground wall: ",value)
                inputs.append(value)
        for key,value in basement_dict.items():
            if key == basement:
                print("basement: ",value)
                inputs.append(value)
        return inputs

if __name__ == '__main__':
    ml = ml_model()
    print(ml.predict(15,1,1))


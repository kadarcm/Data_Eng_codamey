import pandas as pd
import sqlalchemy as sq
import json




class Clean:
    def __init__(self, settings_file: str) -> None:
        settings =json.load(open(settings_file)) 
        self.read_connection_str=settings["read_connection_str"]
        self.write_connection_str=settings["write_connection_str"]

    def load_data(self):
        engine = sq.create_engine(self.read_connection_str)
        self.table_lst = sq.inspect(engine).get_table_names()
        df_zip = zip(self.table_lst,[pd.read_sql_table(table, engine) for table in self.table_lst])
        self.df_dic = {table : df for (table , df) in df_zip}

    @staticmethod
    def contact(ct_info:dict):
        maddress = ct_info["mailing_address"].split(",")
        eaddress = ct_info["email"]
        return pd.Series([*maddress, eaddress], index=["street", "city", "state", "zip", "email"])
    
    def clean_student_table(self):
        mdf=self.df_dic["cademycode_students"]
        mdf["job_id"]=pd.to_numeric(mdf['job_id'].fillna(-1),downcast="integer")
        mdf["num_course_taken"]=pd.to_numeric(mdf["num_course_taken"].fillna(0),downcast="integer")
        mdf["current_career_path_id"]=pd.to_numeric(mdf["current_career_path_id"].fillna(0),downcast="integer")
        mdf["time_spent_hrs"]=pd.to_numeric(mdf["time_spent_hrs"].fillna(0))
        mdf["dob"]=pd.to_datetime(mdf["dob"])
        mdf["first_name"]=mdf["name"].str.split(" ",expand=True)[0]
        mdf["last_name"]=mdf["name"].str.split(" ",expand=True)[1]

        mdf=pd.concat([mdf,mdf["contact_info"].apply(self.contact)],axis=1)
        mdf.drop(columns=["contact_info", "name"], inplace=True)
        self.df_dic["cademycode_students"]=mdf
        

    def merge_tables(self):
        self.big_df= self.df_dic["cademycode_students"].merge(self.df_dic["cademycode_courses"], left_on="current_career_path_id", right_on="career_path_id")
        self.big_df= self.big_df.merge(self.df_dic["cademycode_student_jobs"].drop_duplicates(), left_on="job_id", right_on="job_id")
        self.big_df.drop(columns=["job_id", "career_path_id"], inplace=True)

    def output_dbs(self, path):
        engine =sq.create_engine(f"sqlite:///{path}/cademycode_anylitic.db")
        self.big_df.to_csv(f"./{path}/cademycode.csv")
        self.big_df.to_parquet(f"./{path}/cademycode.parquet.gzip", compression="gzip")
        self.big_df.to_sql('cademycode_scrubbed', engine, if_exists='replace', index=False)

    def add_unknown_rows(self):
        self.df_dic["cademycode_student_jobs"].loc[-1]=[-1, "none", 80000]
        self.df_dic["cademycode_courses"].loc[-1]=[0, "undecided", 20]
    
    def get_colums(self,table_name:str):
        return self.df_dic[table_name].columns
        # return ""


if __name__=="__main__":
    clean = Clean("./cademycode/cademyPy/setting.json")
    clean.load_data()
    for table in clean.table_lst:
        print(clean.get_colums(table))
    clean.clean_student_table()
    for table in clean.table_lst:
        print(clean.get_colums(table))
    clean.add_unknown_rows()
    clean.merge_tables()
    print(clean.big_df.columns)
 


from cleaner import Clean
import logging
import argparse


parser = argparse.ArgumentParser(description ='Search some files')
parser.add_argument("-f", dest = 'filename',
                    action="store", help="file name")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



if __name__ =="__main__":
    
    log_file_name=  parser.parse_args().filename or "log.txt"
    # log_file_name="log.txt"

    file_handeler = logging.FileHandler(filename=log_file_name,mode="a")
    formatter = logging.Formatter('%(asctime)s -  - %(levelname)s - %(message)s')
    file_handeler.setFormatter(formatter)
    logger.addHandler(file_handeler)
    
    logger.info("cademycode program started")
    clean= Clean("./cademycode/cademyPy/setting.json")
    clean.load_data()
    logger.info("Data Loaded")
    logger.info("tables %s found", str(clean.table_lst))
    for table in clean.table_lst:
        logger.info(f"{table} has {len(clean.df_dic[table])} many rows")
        logger.info(f"{table} has columns= {str(clean.get_colums(table))}")
    clean.clean_student_table()
    logger.info(f"Now student table has columns= {str(clean.get_colums('cademycode_students'))}" )
    clean.add_unknown_rows()
    logger.info("added rows to look-up tables for students with unknown jobs and career paths")
    clean.merge_tables()
    logger.info("merging tables to 1 ugly flat table")
    logger.info(f"flat table has columns= {clean.big_df.columns}")
    clean.output_dbs("cademycode/DBs")
    logger.info("outputing dbs, csv, and parquet")


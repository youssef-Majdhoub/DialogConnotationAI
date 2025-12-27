import pandas as pd
import numpy as np
from tqdm import tqdm
import csv
import os,ast

conversations_path="./raw_data/archive/movie_conversations.tsv"
lines_path="./raw_data/archive/movie_lines.tsv"
class DataCleaner:
    def __init__(self,paths,expected_columns):
        self.paths=paths
        self.expected_columns=expected_columns
        self.index=0
    def bad_line_function(self,bad_line):
        n=self.expected_columns[self.index]
        for i in range(n-1,len(bad_line)):
            bad_line[i]=bad_line[i].replace('*','')
            bad_line[i]=bad_line[i].strip()
        for i in range(bad_line.count('')):
            bad_line.remove('')
        bad_line=bad_line[:n-1]+[' '.join(bad_line[n-1:])]
        return bad_line
    def clean(self,path):
        cols=['a'+str(i) for i in range(self.expected_columns[self.index])]
        re=pd.read_table(path,engine="python",quoting=csv.QUOTE_NONE,names=cols,on_bad_lines=self.bad_line_function)
        return re.dropna()
    def integrity_check(self,discussions_frame,lines_frame):
        discussions_frame.columns=["per1","per2","movie_id","utterance_ids"]
        lines_frame.columns=["line_id","character_id","movie_id","character_name","text"]
        here_ids=set(lines_frame["line_id"])
        needed_ids=set()
        to_remove_diss=[]
        for i in range(len(discussions_frame)):
            lines=set(ast.literal_eval(discussions_frame.iloc[i]["utterance_ids"].replace(" ",",")))
            if lines.issubset(here_ids):
                needed_ids.update(lines)
            else:
                to_remove_diss.append(discussions_frame.index[i])
        discussions_frame.drop(index=to_remove_diss,inplace=True)
        lines_frame = lines_frame[lines_frame["line_id"].isin(needed_ids)]
        return discussions_frame,lines_frame
    def clean_path(self,path):
        abs=os.path.abspath(path)
        folder,name=os.path.split(abs)
        parts=os.path.splitext(name)
        return os.path.join(folder,parts[0]+'_cleaned'+parts[-1])
    def save_cleaned(self,repair_mode=False):
        clean_paths=[self.clean_path(path) for path in self.paths]
        re=[]
        for i in range(len(self.paths)):
            self.index=i
            if not(repair_mode) and os.path.exists(clean_paths[i]):continue
            re.append(self.clean(self.paths[i]))
        if(len(re)==2):
            diss,line=re
            diss,line=self.integrity_check(diss,line)
            diss.to_csv(clean_paths[0],sep='\t',index=False,header=None)
            line.to_csv(clean_paths[1],sep='\t',index=False,header=None)
        elif len(re)==1:
            print("integrity not checked please activate repair mode for safer data handling")
        return clean_paths
class DataProvider:
    def __init__(self):
        self.cleaner=DataCleaner([conversations_path,lines_path],[4,5])
        self.conversations_path,self.lines_path=self.cleaner.save_cleaned()
        stats_exists = os.path.exists("./data_set/data_stat.tsv")
        conv_dir_exists = os.path.exists("./data_set/conversations")
        stat_dir_exists = os.path.exists("./data_set/stats")
        if(stats_exists or conv_dir_exists or stat_dir_exists):
            self.repair_mode_from_raw_data() 
        else:
            self.create_data_set()
    def create_data_set(self):
        conversations=pd.read_csv(self.conversations_path,sep="\t",header=None,names=["per1","per2","movie_id","utterance_ids"])
        lines=pd.read_csv(self.lines_path,sep="\t",header=None,
                          names=["line_id","character_id","movie_id","character_name","text"],index_col="line_id")
        os.makedirs("./data_set/conversations",exist_ok=True)
        os.makedirs("./data_set/stats",exist_ok=True)
        stat_data={"id":[],"disscussion_length":[],"is_complete":[]}
        for i in tqdm(range(len(conversations)), desc="Creating conversations"):
            disscussion_df=self.create_conversation(conversations,lines,i)
            if(len(disscussion_df)==0):
                print("there is a problem")
            disscussion_df.to_csv(f"./data_set/conversations/conversation_{i+1}.tsv",sep="\t",index=False)
            disscussion_stat_df=self.create_disscussion_stat(i,len(disscussion_df))
            disscussion_stat_df.to_csv(f"./data_set/stats/stat_{i+1}.tsv",sep="\t",index=False)
            stat_data["id"].append(i+1)
            stat_data["disscussion_length"].append(len(disscussion_df))
            stat_data["is_complete"].append(0)
        self.data_stat=pd.DataFrame(stat_data)
        self.data_stat.to_csv("./data_set/data_stat.tsv",sep="\t",index=False)
    def create_conversation(self,conversations,lines,conversation_id):
        disscussion={"id":[],"lines_index":[],"character_id":[],"text":[]}
        lines_ids=conversations.iloc[conversation_id]["utterance_ids"]
        lines_ids=lines_ids.strip(" ")
        lines_ids=lines_ids.replace(" ",",")
        lines_ids=ast.literal_eval(lines_ids)
        conversation_lines=lines.loc[lines_ids]
        for i in range(len(conversation_lines)):
            disscussion["id"].append(conversation_id+1)
            disscussion["lines_index"].append(i)
            disscussion["character_id"].append(conversation_lines.iloc[i]["character_id"])
            disscussion["text"].append(conversation_lines.iloc[i]["text"])
        disscussion_df=pd.DataFrame(disscussion)
        return disscussion_df
    def create_disscussion_stat(self,conversation_id,number_of_lines):
        disscussion_stat={"id":[],"lines_index":[],"connotation":[]}
        for i in range(number_of_lines):
            disscussion_stat["id"].append(conversation_id+1)
            disscussion_stat["lines_index"].append(i)
            disscussion_stat["connotation"].append(np.nan)
        disscussion_stat_df=pd.DataFrame(disscussion_stat)
        return disscussion_stat_df
    def data_set_append(self):
        conversations=pd.read_csv(self.conversations_path,sep="\t",header=None,names=["per1","per2","movie_id","utterance_ids"])
        lines=pd.read_csv(self.lines_path,sep="\t",header=None,
                          names=["line_id","character_id","movie_id","character_name","text"],index_col="line_id")
        self.data_stat=pd.read_csv("./data_set/data_stat.tsv",sep="\t")
        starting_index=max(self.stat_data["id"])
        for i in tqdm(range(starting_index, len(conversations))):
            disscussion_df=self.create_conversation(conversations,lines,i)
            disscussion_df.to_csv(f"./data_set/conversations/conversation_{i+1}.tsv",sep="\t",index=False)
            disscussion_stat_df=self.create_disscussion_stat(i,len(disscussion_df))
            disscussion_stat_df.to_csv(f"./data_set/stats/stat_{i+1}.tsv",sep="\t",index=False)
            self.data_stat.loc[len(self.data_stat)]={"id":i+1,"disscussion_length":len(disscussion_df)}
        self.data_stat.to_csv("./data_set/data_stat.tsv",sep="\t",index=False)
    def repair_mode_from_raw_data(self):
        os.makedirs("./data_set/conversations",exist_ok=True)
        os.makedirs("./data_set/stats",exist_ok=True)
        self.conversations_path,self.lines_path=self.cleaner.save_cleaned()
        conversations=pd.read_csv(self.conversations_path,sep="\t",header=None,names=["per1","per2","movie_id","utterance_ids"])
        lines=pd.read_csv(self.lines_path,sep="\t",header=None,
                          names=["line_id","character_id","movie_id","character_name","text"],index_col="line_id")
        try:
            self.data_stat=pd.read_csv("./data_set/data_stat.tsv",sep="\t")
        except:
            self.data_stat=pd.DataFrame({"id":[],"disscussion_length":[],"is_complete":[]})
        new={"id":[],"disscussion_length":[],"is_complete":[]}
        ids=set(self.data_stat['id'].values)
        if len(self.data_stat)<len(conversations):
            print("there is missing conversations,please wait for a full report")
        for i in tqdm(range(len(conversations)), desc="Repairing dataset"):
            stat,log=1,1
            if not os.path.exists(f"./data_set/conversations/conversation_{i+1}.tsv"):
                disscussion_df=self.create_conversation(conversations,lines,i)
                disscussion_df.to_csv(f"./data_set/conversations/conversation_{i+1}.tsv",sep="\t",index=False)
                log=0
            if not os.path.exists(f"./data_set/stats/stat_{i+1}.tsv"):
                if log:
                    disscussion_df=pd.read_table(f"./data_set/conversations/conversation_{i+1}.tsv")
                stat_df=self.create_disscussion_stat(i,len(disscussion_df))
                stat_df.to_csv(f"./data_set/stats/stat_{i+1}.tsv",sep="\t",index=False)
                stat=0
            if not (i+1) in ids:
                if stat:
                    stat_df=pd.read_table(f"./data_set/stats/stat_{i+1}.tsv",header=None)
                new['id'].append(i+1)
                length=len(stat_df)
                new['disscussion_length'].append(length)
                new['is_complete'].append(length-stat_df['connotation'].isna().sum())
                ids.add(i+1)
        self.data_stat=pd.concat([self.data_stat,pd.DataFrame(new)])
        self.data_stat.to_csv("./data_set/data_stat.tsv",sep="\t",index=False)
    def get_conversation(self,conversation_id,include_stat=False):
        disscussion_df=pd.read_csv(f"./data_set/conversations/conversation_{conversation_id}.tsv",sep="\t",)
        if include_stat:
            disscussion_stat_df=pd.read_csv(f"./data_set/stats/stat_{conversation_id}.tsv",sep="\t",)
            disscussion_df=pd.merge(disscussion_df,disscussion_stat_df,left_on=["id","lines_index"],right_on=["id","lines_index"])
        return disscussion_df
    def get_disscusion_stats(self,conversation_id):
        disscussion_stat_df=pd.read_csv(f"./data_set/stats/stat_{conversation_id}.tsv",sep="\t")
        return disscussion_stat_df
    def update_connotation(self,conversation_id,line_index,connotation):
        disscussion_stat_df=pd.read_csv(f"./data_set/stats/stat_{conversation_id}.tsv",sep="\t")
        disscussion_stat_df.loc[disscussion_stat_df["lines_index"]==line_index,"connotation"]=connotation
        disscussion_stat_df.to_csv(f"./data_set/stats/stat_{conversation_id}.tsv",sep="\t",index=False)
        is_completed=len(disscussion_stat_df)-disscussion_stat_df['connotation'].isna().sum()
        self.data_stat.loc[self.data_stat['id']==conversation_id,'is_complete']=is_completed
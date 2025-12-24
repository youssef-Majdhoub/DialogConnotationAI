import pandas as pd
import os,ast

conversations_path="./raw_data/archive/movie_conversations.tsv"
lines_path="./raw_data/archive/movie_lines.tsv"
class data_provider():
    def __init__(self):
        if(os.path.exists("./data_set/data_stat.tsv")):
           self.data_stat=pd.read_csv("./data_set/data_stat.tsv",sep="\t")
        else:
            self.create_data_set()
    def create_data_set(self):
        conversations=pd.read_csv(conversations_path,sep="\t",header=None,names=["per1","per2","movie_id","utterance_ids"])
        lines=pd.read_csv(lines_path,sep="\t",header=None,names=["line_id","character_id","movie_id","character_name","text"])
        os.makedirs("./data_set/conversations",exist_ok=True)
        stat_data={"id":[],"disscussion_length":[]}
        for i in range(len(conversations)):
            disscussion_df=self.create_conversation(conversations,lines,i)
            disscussion_df.to_csv(f"./data_set/conversations/conversation_{i+1}.tsv",sep="\t",index=False)
            disscussion_stat_df=self.create_disscussion_stat(i,len(disscussion_df))
            disscussion_stat_df.to_csv(f"./data_set/stats/stat_{i+1}.tsv",sep="\t",index=False)
            stat_data["id"].append(i+1)
            stat_data["disscussion_length"].append(len(disscussion_df))
        self.data_stat=pd.DataFrame(stat_data)
        self.data_stat.to_csv("./data_set/data_stat.tsv",sep="\t",index=False)
    def create_conversation(self,conversations,lines,conversation_id):
        disscussion={"id":[],"lines_index":[],"character_id":[],"text":[]}
        lines_ids=conversations.iloc[conversation_id]["utterance_ids"]
        lines_ids=lines_ids.strip(" ")
        lines_ids=lines_ids.replace(" ",",")
        lines_ids=ast.literal_eval(lines_ids)
        conversation_lines=lines[lines["line_id"].isin(lines_ids)]
        for i in range(len(conversation_lines)):
            disscussion["id"].append(conversation_id+1)
            disscussion["lines_index"].append(i)
            disscussion["character_id"].append(conversation_lines.iloc[i]["character_id"])
            disscussion["text"].append(conversation_lines.iloc[i]["text"])
        disscussion_df=pd.DataFrame(disscussion)
        print(disscussion_df.head())
        return disscussion_df
    def create_disscussion_stat(self,conversation_id,number_of_lines):
        disscussion_stat={"id":[],"line_index":[],"connotation":[]}
        for i in range(number_of_lines):
            disscussion_stat["id"].append(conversation_id)
            disscussion_stat["line_index"].append(i)
            disscussion_stat["connotation"].append("None")
        disscussion_stat_df=pd.DataFrame(disscussion_stat)
        print(disscussion_stat_df.head())
        return disscussion_stat_df
    def data_set_append(self):
        conversations=pd.read_csv(conversations_path,sep="\t",header=None,names=["per1","per2","movie_id","utterance_ids"])
        lines=pd.read_csv(lines_path,sep="\t",header=None,names=["line_id","character_id","movie_id","character_name","text"])
        stat_data=pd.read_csv("./data_set/data_stat.tsv",sep="\t")
        starting_index=max(stat_data["id"])
        for i in range(starting_index,len(conversations)):
            disscussion_df=self.create_conversation(conversations,lines,i)
            disscussion_df.to_csv(f"./data_set/conversations/conversation_{i+1}.tsv",sep="\t",index=False)
            disscussion_stat_df=self.create_disscussion_stat(i,len(disscussion_df))
            disscussion_stat_df.to_csv(f"./data_set/stats/stat_{i+1}.tsv",sep="\t",index=False)
            stat_data["id"].append(i+1)
            stat_data["disscussion_length"].append(len(disscussion_df))
        self.data_stat=pd.DataFrame(stat_data)
        self.data_stat.to_csv("./data_set/data_stat.tsv",sep="\t",index=False)
    def repair_mode_from_raw_data(self):
        conversations=pd.read_csv(conversations_path,sep="\t",header=None,names=["per1","per2","movie_id","utterance_ids"])
        lines=pd.read_csv(lines_path,sep="\t",header=None,names=["line_id","character_id","movie_id","character_name","text"])
        stat_data=pd.read_csv("./data_set/data_stat.tsv",sep="\t")
        if len(stat_data)<len(conversations):
            print("there is missing conversations,please wait for a full report")
        for i in range(len(conversations)):
            if not os.path.exists(f"./data_set/conversations/conversation_{i+1}.tsv"):
                print(f"conversation {i+1} is missing, recreating it")
                disscussion_df=self.create_conversation(conversations,lines,i)
                disscussion_df.to_csv(f"./data_set/conversations/conversation_{i+1}.tsv",sep="\t",index=False)
            if not os.path.exists(f"./data_set/stats/stat_{i+1}.tsv"):
                print(f"stat for conversation {i+1} is missing, recreating it")
                disscussion_stat_df=self.create_disscussion_stat(i,len(disscussion_df))
                disscussion_stat_df.to_csv(f"./data_set/stats/stat_{i+1}.tsv",sep="\t",index=False)
            if not (i+1) in stat_data["id"].values:
                print(f"stat entry for conversation {i+1} is missing, adding it")
                stat_data=stat_data.append({"id":i+1,"disscussion_length":len(disscussion_df)},ignore_index=True)
        self.data_stat=pd.DataFrame(stat_data)
        self.data_stat.to_csv("./data_set/data_stat.tsv",sep="\t",index=False)
    def get_conversation(self,conversation_id,include_stat=False):
        disscussion_df=pd.read_csv(f"./data_set/conversations/conversation_{conversation_id}.tsv",sep="\t")
        if include_stat:
            disscussion_stat_df=pd.read_csv(f"./data_set/stats/stat_{conversation_id}.tsv",sep="\t")
            disscussion_df=pd.merge(disscussion_df,disscussion_stat_df,left_on=["id","lines_index"],right_on=["id","line_index"])
        return disscussion_df
    def get_disscusion_stats(self,conversation_id):
        disscussion_stat_df=pd.read_csv(f"./data_set/stats/stat_{conversation_id}.tsv",sep="\t")
        return disscussion_stat_df
    def update_connotation(self,conversation_id,line_index,connotation):
        disscussion_stat_df=pd.read_csv(f"./data_set/stats/stat_{conversation_id}.tsv",sep="\t")
        disscussion_stat_df.loc[disscussion_stat_df["line_index"]==line_index,"connotation"]=connotation
        disscussion_stat_df.to_csv(f"./data_set/stats/stat_{conversation_id}.tsv",sep="\t",index=False)
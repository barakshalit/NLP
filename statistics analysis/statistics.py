import json
import glob
import pandas as pd
from stylometry.extract import *
import stylometry



def st(file_paths):
    VERB_st = ADV_st= ADJ_st= NOUN_st= DET_st= ADP_st= PRON_st= AUX_st= PUNCT_st= SCONJ_st=INTJ_st= NUM_st=PROPN_st=CCONJ_st= X_st = word_len_st = song_len_st = male_st = female_st = 0
    for file_path in file_paths:
        with open(file_path, 'r',encoding='utf-8') as file:
            data = json.load(file)
            VERB_num, ADV_num, ADJ_num, NOUN_num, DET_num, ADP_num, PRON_num, AUX_num, PUNCT_num, SCONJ_num,INTJ_num, NUM_num, PROPN_num, CCONJ_num, X_num = pos_num(data)
            word_len_num = word_len(data)
            song_len_num = song_mean_len(data)
            male_num,female_num = gender_num(data)
            

            VERB_st += VERB_num
            ADV_st += ADV_num
            ADJ_st += ADJ_num
            NOUN_st += NOUN_num
            DET_st += DET_num
            ADP_st += ADP_num
            PRON_st += PRON_num
            AUX_st += AUX_num
            PUNCT_st += PUNCT_num
            SCONJ_st += SCONJ_num
            INTJ_st += INTJ_num
            NUM_st += NUM_num
            PROPN_st += PROPN_num
            CCONJ_st += CCONJ_num
            X_st += X_num
            
            word_len_st += word_len_num
            song_len_st += song_len_num
            male_st += male_num
            female_st += female_num

    VERB_st/=len(file_paths)
    ADV_st/=len(file_paths)
    ADJ_st/=len(file_paths)
    NOUN_st/=len(file_paths)
    DET_st/=len(file_paths)
    ADP_st/=len(file_paths)
    PRON_st/=len(file_paths)
    AUX_st/=len(file_paths)
    PUNCT_st/=len(file_paths)
    SCONJ_st/=len(file_paths)
    INTJ_st/=len(file_paths)
    NUM_st/=len(file_paths)
    PROPN_st/=len(file_paths)
    CCONJ_st/=len(file_paths)
    X_st/=len(file_paths)

    word_len_st/=len(file_paths)
    song_len_st/=len(file_paths)
    male_st/=len(file_paths)
    female_st/=len(file_paths)

    
    
    return VERB_st, ADV_st, ADJ_st, NOUN_st, DET_st, ADP_st, PRON_st, AUX_st, PUNCT_st, SCONJ_st, INTJ_st, NUM_st, PROPN_st, CCONJ_st, X_st,word_len_st, song_len_st,male_st,female_st

def pos_num(data):
    tokens_len = len(data['tokens'])
    VERB_num = ADV_num = ADJ_num = NOUN_num = DET_num = ADP_num = PRON_num = AUX_num = PUNCT_num = SCONJ_num = INTJ_num = NUM_num = PROPN_num = CCONJ_num =  X_num =0

    for i in range (tokens_len):
        if (data['tokens'][i]['morph']['pos'] == 'VERB'):
            VERB_num += 1
        if (data['tokens'][i]['morph']['pos'] == 'ADV'):
            ADV_num += 1
        if (data['tokens'][i]['morph']['pos'] == 'ADJ'):
            ADJ_num += 1
        if (data['tokens'][i]['morph']['pos'] == 'NOUN'):
            NOUN_num += 1
        if (data['tokens'][i]['morph']['pos'] == 'DET'):
            DET_num += 1
        if (data['tokens'][i]['morph']['pos'] == 'ADP'):
            ADP_num += 1
        if (data['tokens'][i]['morph']['pos'] == 'PRON'):
            PRON_num += 1
        if (data['tokens'][i]['morph']['pos'] == 'AUX'):
            AUX_num += 1
        if (data['tokens'][i]['morph']['pos'] == 'PUNCT'):
            PUNCT_num += 1
        if (data['tokens'][i]['morph']['pos'] == 'SCONJ'):
            SCONJ_num += 1
        if (data['tokens'][i]['morph']['pos'] == 'INTJ'):
            INTJ_num += 1
        if (data['tokens'][i]['morph']['pos'] == 'NUM'):
            NUM_num += 1
        if (data['tokens'][i]['morph']['pos'] == 'PROPN'):
            PROPN_num += 1
        if (data['tokens'][i]['morph']['pos'] == 'CCONJ'):
            CCONJ_num += 1
        if (data['tokens'][i]['morph']['pos'] == 'X'):
            X_num += 1

    return VERB_num/tokens_len, ADV_num/tokens_len, ADJ_num/tokens_len, NOUN_num/tokens_len, DET_num/tokens_len, ADP_num/tokens_len, PRON_num/tokens_len, AUX_num/tokens_len, PUNCT_num/tokens_len, SCONJ_num/tokens_len, INTJ_num/tokens_len, NUM_num/tokens_len,PROPN_num/tokens_len,CCONJ_num/tokens_len, X_num/tokens_len

def word_len(data):
    tokens_len = len(data['tokens'])
    word_len = 0
    for i in range (tokens_len):
       word_len +=  data['tokens'][i]['offsets']['end'] - data['tokens'][i]['offsets']['start']
    return word_len/tokens_len

def mean_sentence_len(file_paths):
    sentence_len = 0
    for file_path in file_paths:
        document= StyloDocument(file_path)
        mean_sentence_len = document.mean_sentence_len()
        sentence_len += mean_sentence_len

    return sentence_len/len(file_paths)

def song_mean_len(data):
    tokens_len = len(data['tokens'])
    song_len =  data['tokens'][tokens_len-1]['offsets']['end'] - data['tokens'][0]['offsets']['start']
    return song_len

def gender_num(data):
    tokens_len = len(data['tokens'])
    male_num = female_num= 0
    for i in range (tokens_len):
        x = data['tokens'][i]['morph']['feats'].get('Gender')
        if (x == 'Masc'):
            male_num += 1
        if (x == 'Fem'):
            female_num += 1   
    return male_num/tokens_len,female_num/tokens_len

def main():
    # Specify the file paths
    file_paths_old = glob.glob('stylometry-data/Dor Ha-Medina BERT output/*.json')
    file_paths_new = glob.glob('stylometry-data/Present BERT output/*.json')
    file_paths_old_sen = glob.glob('stylometry-data/old/*')
    file_paths_new_sen = glob.glob('stylometry-data/new/*')
    
    
    # old songs statistics
    print("Old songs statistics:\n")
    VERB_st_old, ADV_st_old, ADJ_st_old, NOUN_st_old, DET_st_old, ADP_st_old, PRON_st_old, AUX_st_old, PUNCT_st_old, SCONJ_st_old, INTJ_st_old, NUM_st_old, PROPN_st_old, CCONJ_st_old, X_st_old,word_len_old,song_len_old,male_old,female_old = st(file_paths_old)
    # syntax
    print(" VERB_st_old =",VERB_st_old,"\n", "ADV_st_old =",ADV_st_old,"\n", "ADJ_st_old =",ADJ_st_old,"\n", "NOUN_st_old =",NOUN_st_old,"\n", "DET_st_old =",DET_st_old,"\n", "ADP_st_old =",ADP_st_old,"\n", "PRON_st_old =",PRON_st_old,"\n", "AUX_st_old =",AUX_st_old,"\n", "PUNCT_st_old =",PUNCT_st_old,"\n", "SCONJ_st_old =",SCONJ_st_old,"\n", "INTJ_st_old =",INTJ_st_old,"\n", "NUM_st_old =",NUM_st_old,"\n", "PROPN_st_old =",PROPN_st_old,"\n", "CCONJ_st_old =",CCONJ_st_old,"\n", "X_st_old =",X_st_old,"\n")
    print("Total syntaxes = ",VERB_st_old+ ADV_st_old+ ADJ_st_old+ NOUN_st_old+ DET_st_old+ ADP_st_old+ PRON_st_old+ AUX_st_old+ PUNCT_st_old+ SCONJ_st_old + INTJ_st_old + NUM_st_old + PROPN_st_old+ CCONJ_st_old+ X_st_old,"\n")
    # Word mean length
    print("Old Word mean length: ",word_len_old,"\n")
    # sentence mean length
    print("Old Mean sentence length:", mean_sentence_len(file_paths_old_sen),"\n")
    # song mean length
    print("Old mean song length: ",song_len_old,"\n")
    # gender statistics
    print("Old male percentage: ", male_old, ",", "Old female percentage: ",female_old,"\n")
    print("====================================================================================================\n")

    # new songs statistics
    print("New songs statistics:\n")
    VERB_st_new, ADV_st_new, ADJ_st_new, NOUN_st_new, DET_st_new, ADP_st_new, PRON_st_new, AUX_st_new, PUNCT_st_new, SCONJ_st_new, INTJ_st_new, NUM_st_new, PROPN_st_new, CCONJ_st_new, X_st_new,word_len_new,song_len_new,male_new,female_new = st(file_paths_new)
    # syntax
    print(" VERB_st_new =",VERB_st_new,"\n", "ADV_st_new =",ADV_st_new,"\n", "ADJ_st_new =",ADJ_st_new,"\n", "NOUN_st_new =",NOUN_st_new,"\n", "DET_st_new =",DET_st_new,"\n", "ADP_st_new =",ADP_st_new,"\n", "PRON_st_new =",PRON_st_new,"\n", "AUX_st_new =",AUX_st_new,"\n", "PUNCT_st_new =",PUNCT_st_new,"\n", "SCONJ_st_new =",SCONJ_st_new,"\n", "INTJ_st_new =",INTJ_st_new,"\n", "NUM_st_new =",NUM_st_new,"\n", "PROPN_st_new =",PROPN_st_new,"\n", "CCONJ_st_new =",CCONJ_st_new,"\n", "X_st_new =",X_st_new,"\n")
    print("Total syntaxes = ",VERB_st_new+ ADV_st_new+ ADJ_st_new+ NOUN_st_new+ DET_st_new+ ADP_st_new+ PRON_st_new+ AUX_st_new+ PUNCT_st_new+ SCONJ_st_new + INTJ_st_new + NUM_st_new + PROPN_st_new+ CCONJ_st_new+ X_st_new,"\n")
    # Word mean length
    print("New word mean length: ",word_len_new,"\n")
    # sentence mean length
    print("New mean sentence length:", mean_sentence_len(file_paths_new_sen),"\n")
    # song mean length
    print("New mean song length: ",song_len_new,"\n")
    # gender statistics
    print("New male percentage: ", male_new, ",", "New female percentage: ",female_new,"\n")
    print("====================================================================================================\n")

    # comparison
    print("Comparison:\n")
    print("Old songs statistics VS New songs statistics:")
    # syntax
    print(" VERB_st_old/VERB_st_new =",VERB_st_old/VERB_st_new,"\n","ADV_st_old/ADV_st_new=",ADV_st_old/ADV_st_new,"\n","ADJ_st_old/ADJ_st_new=",ADJ_st_old/ADJ_st_new,"\n","NOUN_st_old/NOUN_st_new=",NOUN_st_old/NOUN_st_new,"\n","DET_st_old/DET_st_new=",DET_st_old/DET_st_new,"\n","ADP_st_old/ADP_st_new=",ADP_st_old/ADP_st_new,"\n","PRON_st_old/PRON_st_new=",PRON_st_old/PRON_st_new,"\n","AUX_st_old/AUX_st_new=",AUX_st_old/AUX_st_new,"\n","PUNCT_st_old/PUNCT_st_new=",PUNCT_st_old/PUNCT_st_new,"\n","SCONJ_st_old/SCONJ_st_new=",SCONJ_st_old/SCONJ_st_new,"\n","INTJ_st_old/INTJ_st_new=",INTJ_st_old/INTJ_st_new,"\n","NUM_st_old/NUM_st_new=",NUM_st_old/NUM_st_new,"\n","PROPN_st_old/PROPN_st_new=",PROPN_st_old/PROPN_st_new,"\n","CCONJ_st_old/CCONJ_st_new=",CCONJ_st_old/CCONJ_st_new,"\n","X_st_old/X_st_new=",X_st_old/X_st_new,"\n")
    # Word mean length
    print("New word mean / Old word mean: =",word_len_old/word_len_new,"\n")
    # sentence mean length
    print("Old mean sentence length / New mean sentence length:", mean_sentence_len(file_paths_old_sen)/mean_sentence_len(file_paths_new_sen),"\n")
    # song mean length
    print("Old mean song length / New mean song length: ",song_len_old/song_len_new,"\n")
    # gender statistics
    print("Old male / New male: " ,male_old/male_new,"\n")
    print("Old female / New female: " ,female_old/female_new)
    print("====================================================================================================\n")



if __name__ == "__main__":
    main()



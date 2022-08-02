
import os
import pandas as pd
import sys


TM_folder = os.environ['TM_folder']
subject_level_text_loc = os.environ['subject_level_text_loc'] # output location
transcript_level_text_loc = os.environ['transcript_level_text_loc'] # inputs 


'''
Subject-level transcript. 
Use csv in transcript_level_text folder. 
'''
def subject_level_transcript(study):
	# switch to specific patient folder - transcript CSVs

	try:
		os.chdir(os.getcwd() + transcript_level_text_loc)
	except Exception as e:
		print(e, flush=True) # should never reach this error if calling via bash module
		return

	print("Generating subject-level transcript text for " + study, flush=True)

	metadata = pd.DataFrame()
	save_path = f'{TM_folder}/{subject_level_text_loc}/{study}_subject_level_text.csv'

	for filename in os.listdir():
		if filename.endswith(".csv"): 
			cur_daily_text = pd.read_csv(filename)
			cur_full_text = "".join(cur_daily_text['text'])
			subject_id = filename.split('_')[2]
			cur_full_text_df = pd.DataFrame({'doc_id': [subject_id], 'text': [cur_full_text]})
			metadata = metadata.append(cur_full_text_df, ignore_index = True)
	
	metadata.to_csv(save_path, index=False)
			

if __name__ == '__main__':
	subject_level_transcript(sys.argv[1])
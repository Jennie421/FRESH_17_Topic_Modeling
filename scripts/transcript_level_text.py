import os
import pandas as pd
import sys
import string


TM_folder = os.environ['TM_folder']
transcript_level_text_loc = os.environ['transcript_level_text_loc'] # output loc 

study_loc = os.environ['study_loc']
transcripts_loc = os.environ['transcripts_loc']
audio_qc_loc = os.environ['audio_qc_loc']



"""
Summarize pre-processed transcript text for a subject by concatination. 
Caution: must delete daily_text.csv for a subject to avoid repetition. 
"""
def daily_transcripts(study, OLID):
	# switch to specific patient folder - transcript CSVs
	try:
		os.chdir(study_loc + study + "/" + OLID + transcripts_loc + "csv")
	except:
		print("No csv", flush=True) # should never reach this error if calling via bash module
		return

	print("Summarizing daily transcript text for " + OLID, flush=True)
	
	try:
		# if there already exist metadataWithWeek.csv, from wordcloud pipeline
		metadata = pd.read_csv(f'{study_loc}{study}/{OLID}{audio_qc_loc}{study}_{OLID}_metadataWithWeek.csv')
	except:
		# if not, create the file here
		metadata = add_week(study, OLID)

	for r in range(metadata.shape[0]):  # Iterate through rows 
		transcript_path = metadata['transcript_name'].iloc[r]
		try:
			cur_trans = pd.read_csv(transcript_path)
		except:
			print("Problem loading " + transcript_path, flush=True)
			continue

		# week = metadata['week'].iloc[r]
		# period = metadata['period'].iloc[r] 
		acad_cal_day = int(float(metadata['acad_cal_day'].iloc[r])) # Cast day to int
		# word_count = int(float(metadata['num_words'].iloc[r]))

		daily_text_outpath = f'{TM_folder}/{transcript_level_text_loc}/{study}_{OLID}_daily_text.csv'
		# title = f'{OLID}: Week {week}, {period}, Acad Day {acad_cal_day} (Word Count = {word_count})'

		try:
			text_process(cur_trans, time_point=acad_cal_day, text_path=daily_text_outpath, verbose=True)

		except Exception as e:
			print("Function crashed on " + transcript_path)
			print(e)
			continue


"""
Helper function that processes the transcripts of a subject, outputs csv in formate required by TM analysis
"""
def text_process(transcript_df, text_path, time_point=None, include_punctuation=["'",'[',']',"-"], split_char=" ", pt_only=True, verbose=True): 

	exclude = set(string.punctuation)
	for punc in include_punctuation:
		exclude.remove(punc) # punctuation that will be left in with the wordcloud

	# filter to include only patient words when applicable
	if pt_only:
		subjects = transcript_df["subject"].tolist()
		pt_id = max(set(subjects), key = subjects.count)
		transcript_df = transcript_df[transcript_df["subject"]==pt_id]

	# use transcript to generate necessary inputs to wordcloud function
	sentences = transcript_df["text"].tolist()
	text_full = ""

	for s in sentences:
		word_list = s.split(" ")
		new_break = ""
		for w in word_list:
			try:
				# remove any white space or related characters from string before also removing puncutation (besides exception list)
				w_filt = ''.join(ch for ch in w.strip() if ch not in exclude).lower()
			except:
				if verbose:
					print("problem with word: " + w) # sometimes weird characters cause incorrect splitting here
				continue
		
			# don't want single dashes to count as punctuation, but do remove double dashes at ends of words, as TranscribeMe tends to use them a lot to indicate pauses/stuttering
			if w_filt.endswith("--"):
				w_filt = w_filt[:-2]
			if w_filt.endswith("'s"):
				w_filt = w_filt[:-2] # also remove 's before checking sentiment, as want contractions to be fine but possessive s causes problems
			while len(w_filt) > 1 and w_filt[1] == "-": # remove single letter stuttering at beginning of word as well
				w_filt = w_filt[2:]
			if len(w_filt) <= 1:
				# single letter stutters can be skipped entirely
				continue
			
			new_break = new_break + w_filt + split_char
		text_full = text_full + new_break # compiling full list of filtered text to be used in wordcloud gen

	# Export daily or weekly full text for topic modeling in R
	cur_text_df = pd.DataFrame({'doc_id': [time_point], 'text': [text_full]}) # week or day as doc id

	try:
		full_text_df = pd.read_csv(f'{text_path}')
		full_text_df = pd.concat([full_text_df, cur_text_df])
	except:
		full_text_df = cur_text_df

	full_text_df.to_csv(f'{text_path}', index=False)



"""
Helper function that pads academic calendar days to a full range. 
Adds week number inforrmation to a given metadata data frame. 
"""
def acad_cal_days_and_weeks(metadata):
	# generating a full academic days and weeks df
	acad_cal_days = []
	week = [1]*5
	# Declare a list that is to be converted into a column
	for i in range (1, 280): 
		acad_cal_days.append(i)

	for j in range (2, 42):
		temp = [j] * 7
		week += temp

	week_info = metadata['subject']
	df1 = pd.DataFrame({"acad_cal_day": acad_cal_days})
	df2 = pd.DataFrame({"week": week})
	week_info = pd.concat([week_info, df1, df2], axis=1)

	return week_info


"""
Returns a file of metadata with week. 
Only invoked when metadtaWithWeek.csv does not exist. 
"""
def add_week(study, OLID):
	# Get the all_features file 
	all_features_path = study_loc + study + "/" + OLID + audio_qc_loc + study + "_" + OLID + "_phoneAudioDiary_allFeatures.csv"
	metadata = pd.read_csv(all_features_path)

	week_info = acad_cal_days_and_weeks(metadata)  # generating a full academic days and weeks df
	metadata = pd.merge(week_info, metadata, on=['subject', 'acad_cal_day'], how='left')

	metadata.dropna(inplace=True)	# remove days with missing data
	metadata = metadata[metadata.unavailable_diary == 0]	 # drop unavailable diaries  

	return metadata



if __name__ == '__main__':
	## Map command line arguments to function arguments.
	daily_transcripts(sys.argv[1], sys.argv[2])

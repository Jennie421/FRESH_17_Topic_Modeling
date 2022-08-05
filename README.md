# FRESH_17_Topic_Modeling

Below are documentations of codes used for FRESH_17 audio diary transcript analysis regarding topic modeling. 

## Set up
Run the shell scripts on the cluster to preprocess the transcripts into files that can be converted to corpus in TM analysis. 
Run the R codes on your local computer for TM analysis (have not resolve how to run R on the cluster). 


## Flow of execution 
1. `$ bash topic_modeling_transcript_level.sh STUDYNAME SUBJECT`
  * calls `phone_transcript_allFeatures.py` if allFeatures doesn't exist
    + outputs allFeatures containing audio qc, transcript qc,  and NLP summary. 
  * calls `transcript_level_text.py`
    + outputs processed daily transcript texts for the subject (Have the potential to be modified to output weekly-level texts). 
2. `$ bash topic_modeling_subject_level.sh STUDYNAME`
  * removes previously generated output file if it exists. 
  * calls `subject_level_text.py`
    + loops through and summarizes all avaliable daily transcript texts of different subjects
 

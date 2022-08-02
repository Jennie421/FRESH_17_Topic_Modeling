#!/bin/bash

# this script generates topic modeling corpus files for FRESH_17

# start by getting the absolute path to the directory this script is in, which will be the top level of the repo
# this way script will work even if the repo is downloaded to a new location, rather than relying on hard coded paths to where I put the repo. 
full_path=$(realpath $0)
repo_root=$(dirname $full_path)
# export the path to the repo for scripts called by this script to also use - will unset at end
export repo_root

func_root="$repo_root"/scripts

# gather user settings, first asking which study the code should run on - this is only setting currently for the viz side
# NOTE: take command line argument as subject name variable 
study=$1
export study

p=$2
export p

# modify data location 
TM_folder="$repo_root"
export TM_folder 

transcript_level_text_loc=/FRESH_17_text/transcript_level_text # output loc
export transcript_level_text_loc


study_loc=/n/home_fasse/jennieli/
export study_loc 

transcripts_loc=/phone/processed/audio/transcripts/transcript_data/
export transcripts_loc

# Below are variables needed for metadata generation 
audio_qc_loc=/phone/processed/audio/
export audio_qc_loc

NLP_loc=/phone/processed/audio/transcripts/NLP_features/
export NLP_loc

transcript_qc_loc=/phone/processed/audio/transcripts/
export transcript_qc_loc

all_features_file=$study_loc/$study/$p/$audio_qc_loc/$study"_"$p"_phoneAudioDiary_allFeatures.csv"


# let user know script is starting
echo ""
echo "Beginning script - transcript-level text summary for:"
echo "$study - $p"
echo ""

# add current time for runtime tracking purposes
now=$(date +"%T")
echo "Current time: ${now}"
echo ""


# Build subject-level metadata if not already exist 
if [[ ! -f $all_features_file ]]; then
	echo "******************* Generating subject-level metadata *******************"
	python "$func_root"/phone_transcript_metadata.py "$study" "$p"
	echo ""
fi


# running the main computations
echo "******************* transcript-level text summary *******************"

if [[ ! -d $TM_folder/$transcript_level_text_loc ]]; then
	mkdir -p $TM_folder/$transcript_level_text_loc # create output folder if there isn't already
fi

cd $TM_folder/$transcript_level_text_loc

python "$func_root"/transcript_level_text.py "$study" "$p"

echo "Completed analysis for $p"

echo ""


echo "=============Script Terminated============="
echo "  "
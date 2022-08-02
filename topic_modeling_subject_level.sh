#!/bin/bash

# this script generates topic modeling corpus files for FRESH_17
# this script does not depend on any outputs from the viz pipeline

# start by getting the absolute path to the directory this script is in, which will be the top level of the repo
# this way script will work even if the repo is downloaded to a new location, rather than relying on hard coded paths to where I put the repo. 
full_path=$(realpath $0)
repo_root=$(dirname $full_path)
# export the path to the repo for scripts called by this script to also use - will unset at end
export repo_root

# gather user settings, first asking which study the code should run on - this is only setting currently for the viz side
# NOTE: take command line argument as subject name variable 
study=$1
export study


# modify data location 
TM_folder="$repo_root"
export TM_folder 

transcript_level_text_loc=/FRESH_17_text/transcript_level_text
export transcript_level_text_loc

subject_level_text_loc=/FRESH_17_text/subject_level_text
export subject_level_text_loc

# let user know script is starting
echo ""
echo "Beginning script - subject-level transcript text summary for:"
echo "$study"
echo ""

# add current time for runtime tracking purposes
now=$(date +"%T")
echo "Current time: ${now}"
echo ""

echo "******************* subject-level transcript text summary *******************"

func_root="$repo_root"/scripts

# running the main computations
if [[ ! -d $TM_folder/$subject_level_text_loc ]]; then
	mkdir -p $TM_folder/$subject_level_text_loc # create output folder if there isn't already
fi

# Remove old metadata file if exists. Avoid concatonation error. 
if [[ -f $TM_folder/$subject_level_text_loc/FRESH_17_subject_level_text.csv ]]; then
	echo "Removing old subject-level text summary"
	rm $TM_folder/$subject_level_text_loc/FRESH_17_subject_level_text.csv
fi

python "$func_root"/subject_level_text.py $study

echo ""

echo "=============Script Terminated============="
echo "  "
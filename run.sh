#$ tr -d '\r' <q.sh >q-new.sh
#$ mv q-new.sh q.sh
#sed -i 's/\r//' run.sh
#!/bin/sh
while getopts "n:t:s:l:e:" opt
do
   case "$opt" in
      n) parameterA="$OPTARG" ;;
      t) parameterB="$OPTARG" ;;
      s) parameterC="$OPTARG" ;;
	  e) parameterD="$OPTARG" ;;
	  l) parameterE="$OPTARG" ;;
   esac
done
# Print helpFunction in case parameters are empty
if [ -z "$parameterA" ] || [ -z "$parameterB" ] && [ -z "$parameterC" ]
then
   echo "Insufficient arguments to run the script";
fi
if [ -z "$parameterD" ]
then
	parameterD="NLTK";
fi

if [ -z "$parameterE" ]
then
    parameterE="en";
fi
if [ -z "$parameterC" ]
then
	parameterC="NA";
fi
if [ -z "$parameterA" ]
then
	parameterA=1;
fi
if [ $parameterE == "ja" ]
 then
	case $parameterB in
		(SEN)    python scripts/preprocessing_scripts/sentence_Japanese.py $parameterA
		;;
		(TOK)    python scripts/preprocessing_scripts/token_Japanese.py $parameterA
        ;;
		(POS)    python scripts/preprocessing_scripts/pos_Japanese.py $parameterA
        ;;    
	esac	
else	
python scripts/main.py $parameterA $parameterB $parameterC $parameterD $parameterE
fi

	

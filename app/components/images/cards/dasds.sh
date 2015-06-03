for FILE in *.png;
do mv "$FILE" $(echo "$FILE" | sed 's/ace/A/');
done
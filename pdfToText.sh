#!/bin/bash

	if [ ! -d "TEXT" ] 
		then
			$(mkdir TEXT/)
	fi
	for fich in $(ls TEXT)
	do
		rm TEXT/$fich
	done
	for fich in $(find -name "*.pdf")
	do
		$(pdftotext -raw -enc ASCII7 $fich)
	done
	for fich in $(find $1 -name "*.txt" | grep -oP '(?<=/)[^ ]*')
	do 
		mv $1/$fich TEXT	
	done

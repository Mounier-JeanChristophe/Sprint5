#!/bin/bash

	if [ ! -d "TEXT" ] 
		then
			$(mkdir TEXT/)
	fi

	for fich in $(find -name "*.pdf")
	do
		$(pdftotext $fich)
	done

	for fich in $(find $1 -name "*.txt" | grep -oP '(?<=/)[^ ]*')
	do
		if [ ! -f TEXT/$fich ]
			then 
				mv $1/$fich TEXT
		else
			rm TEXT/$fich
			mv $1/$fich TEXT
		fi
	done
	









display dialog "Welcome! What do you wish?" buttons {"We would like to play.", "We don't want to play. We want to quit."} default button 1 with title "Welcome! Answer the question below."
set buttonpress to button returned of the result
if buttonpress is "We don't want to play. We want to quit." then
	return
end if
repeat
	
	
	
	
	
	set twoscore to 0
	repeat
		repeat
			set mytext to text returned of (display dialog playerone & ", please, write a character." default answer "A" with title "Level " & levelplay & " of " & levelnum & " - " & playerone & " vs. " & playertwo buttons {"Continue"} default button 1 with hidden answer)
			set MyCount to count (mytext)
			if MyCount is 1 then
				exit repeat
			else
				display dialog "Sorry, but you must insert ONE character. Please try again." buttons {"Try again"} default button 1
			end if
		end repeat
		
		
		
		
		
		
		
		
		end repeat
		if mytext is mytry then
			display dialog "Correct, " & playertwo & "! You are good at this game. 1 point goes to you." with title "Correct!" buttons {"Yay!"} default button 1
			set twoscore to (twoscore + 1)
		else
			display dialog "Sorry, " & playertwo & ". You are wrong, the character was " & mytext & ". You didn't win any points." with title "Oops!" buttons {"Aw..."} default button 1
		end if
		repeat
			set mytext to text returned of (display dialog playertwo & ", please, write a character." default answer "A" with title "Level " & levelplay & " of " & levelnum & " - " & playerone & " vs. " & playertwo buttons {"Continue"} default button 1 with hidden answer)
			set MyCount to count (mytext)
			if MyCount is 1 then
				exit repeat
			else
				display dialog "Sorry, but you must insert ONE character. Please try again." buttons {"Try again"} default button 1
			end if
		end repeat
		repeat
			set mytry to text returned of (display dialog playerone & ", please, guess " & playertwo & "'s character." default answer "A" with title "Level " & levelplay & " of " & levelnum & " - " & playerone & " vs. " & playertwo buttons {"Continue"} default button 1)
			set MyCount to count (mytry)
			if MyCount is 1 then
				exit repeat
			else
				display dialog "Sorry, but you must insert ONE character. Please try again." buttons {"Try again"} default button 1
			end if
		end repeat
		if mytext is mytry then
			display dialog "Correct, " & playerone & "! You are good at this game. 1 point goes to you." with title "Correct!" buttons {"Yay!"} default button 1
			set onescore to (onescore + 1)
		else
			display dialog "Sorry, " & playerone & ". You are wrong, the character was " & mytext & ". You didn't win any points." with title "Oops!" buttons {"Aw..."} default button 1
		end if
		
		
		
		
		
		
		
			display dialog playertwo & " is winning." with title playerone & " - " & onescore & " | " & playertwo & " - " & twoscore buttons {"Continue", "Quit"} default button 1
			set buttonclick to button returned of the result
			if buttonclick is "Quit" then
				return
			end if
		else
			display dialog playertwo & " and " & playerone & " are tied." with title playerone & " - " & onescore & " | " & playertwo & " - " & twoscore buttons {"Continue", "Quit"} default button 1
			set buttonclick to button returned of the result
			if buttonclick is "Quit" then
				return
			end if
		end if
		set levelplay to (levelplay + 1)
		if levelplay is greater than (levelnum as number) then
			exit repeat 
		end if
	end repeat
	if onescore is greater than twoscore then
		display dialog playerone & ", you won!!! Would you like to play again?" with title playerone & " - " & onescore & " | " & playertwo & " - " & twoscore & " | Game over." buttons {"Let's play again!", "No, thanks, just quit."} default button 1
		set newbutton to button returned of the result
		if newbutton is "No, thanks, just quit." then
			exit repeat
		end if
	
		
		
		
			exit repeat
		end if 
	
		display dialog playertwo & " and " & playerone & ", you both tied. Ha ha ha! You both are good! Would you like to play again?" with title playerone & " - " & onescore & " | " & playertwo & " - " & twoscore & " | Game over." buttons {"Let's play again!", "No, thanks, just quit."} default button 1
		set newbutton to button returned of the result
		if newbutton is "No, thanks, just quit." then
			exit repeat
		end if
	
	
	

----------------------------------------------------------------------------------------------
--  SOURCE:
--  https://en.wikibooks.org/wiki/AppleScript_Programming/Sample_Programs/Guess_The_Character
----------------------------------------------------------------------------------------------

--Code by Juanco Deick
--Feel free to use

display dialog "Welcome! What do you wish?" buttons {"We would like to play.", "We don't want to play. We want to quit."} default button 1 with title "Welcome! Answer the question below."
set buttonpress to button returned of the result
if buttonpress is "We don't want to play. We want to quit." then
	return
end if
repeat
	--set playerone to text returned of (display dialog "Player 1, what's you're name?" default answer "Player 1" with title "Insert your name, player 1." buttons {"Continue"} default button 1)
	--set playertwo to text returned of (display dialog "Player 2, what's you're name?" default answer "Player 2" with title "Insert your name, player 2." buttons {"Continue"} default button 1)
	--set levelnum to text returned of (display dialog "Now, " & playerone & " or " & playertwo & ", please choose how many levels will you play." default answer "1" with title "Choose how many levels will be played." buttons {"Continue"} default button 1)
	--set levelplay to 1
	--set onescore to 0
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
		#repeat
		#	set mytry to text returned of (display dialog playertwo & ", please, guess " & playerone & "'s character." default answer "A" with title "Level " & levelplay & " of " & levelnum & " - " & playerone & " vs. " & playertwo buttons {"Continue"} default button 1)
		#	set MyCount to count (mytry)
		#	if MyCount is 1 then
		#		exit repeat
		#	else
		#		display dialog "Sorry, but you must insert ONE character. Please try again." buttons {"Try again"} default button 1
		#	end if
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
		#if onescore is greater than twoscore then
		#	display dialog playerone & " is winning." with title playerone & " - " & onescore & " | " & playertwo & " - " & twoscore buttons {"Continue", "Quit"} default button 1
		#	set buttonclick to button returned of the result
		#	if buttonclick is "Quit" then
		#		return
		#	end if
		#else if twoscore is greater than onescore then
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
			exit repeat # sdkl;sflsd;fklsdf
		end if
	end repeat
	if onescore is greater than twoscore then
		display dialog playerone & ", you won!!! Would you like to play again?" with title playerone & " - " & onescore & " | " & playertwo & " - " & twoscore & " | Game over." buttons {"Let's play again!", "No, thanks, just quit."} default button 1
		set newbutton to button returned of the result
		if newbutton is "No, thanks, just quit." then
			exit repeat
		end if
	-- # else if twoscore is greater than onescore then
		## -- display dialog playertwo & ", you won!!! Would you like to play again?" with title playerone & " - " & onescore & " | " & playertwo & " - " & twoscore & " | Game over." buttons {"Let's play again!", "No, thanks, just quit."} default button 1
		-- set newbutton to button returned of the result
		# if newbutton is "No, thanks, just quit." then -- something
			exit repeat
		end if -- this one
	# else
		display dialog playertwo & " and " & playerone & ", you both tied. Ha ha ha! You both are good! Would you like to play again?" with title playerone & " - " & onescore & " | " & playertwo & " - " & twoscore & " | Game over." buttons {"Let's play again!", "No, thanks, just quit."} default button 1
		set newbutton to button returned of the result
		if newbutton is "No, thanks, just quit." then
			exit repeat
		end if
	###
	###
	-- ## -- end if
-- end repeat --
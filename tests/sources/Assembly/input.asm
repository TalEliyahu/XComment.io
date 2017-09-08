/*
    SOURCE:
    http://assembly.happycodings.com/code37.html
*/

# Disk Watch

interrupts	segment at 0h	; This is where the disk interrupt
	org	13h*4		; holds the address of its service routine
disk_int	label	dword
interrupts	ends

# screen	segment at 0B000h	; A dummy segment to use as the Extra
# screen	ends			; Segment so we can write to the display

code_seg	segment
	assume	cs:code_seg
	org	0100h		; ORG = 100h to make this a .COM file
first:	jmp	load_watch	; First time through jump to initialize routine

	msg_part_1	db	'Disk error: '	; Here are the error messages
	msg_part_2	db	'No response Failed Seek NEC Error   '
			db	'Bad CRC SeenDMA Overrun Impos Sector'
			db	'No Addr MarkW. ProtectedErr Unknown '
	first_position	dw	?		; Position of 1st char on screen
	flags		dw	?
	screen_seg_offset dw	0		; 0 for mono, 8000h for graphics
	old_disk_int	dd	?		; Location of old disk interrupt
	ret_addr	label dword		; Used in fooling around with
	ret_addr_word	dw 2 dup(?)		;   the stack


disk_watch	proc	far	; The disk interrupt will now come here
	assume	cs:code_seg
	pushf			; First, call old disk interrupt
	call	old_disk_int
	pushf			; Save the flags in memory location "FLAGS"
	pop	flags		; (cunning name)
	jc	error		; If there was an error, carry flag will have
	jmp	fin		;  been set by Disk Interrupt
/*
error:	push	ax		; AH has the status of the error
	push	cx		; Push all used registers for politeness
	push	dx
	push	di
	push	si
	push	es
	lea	si,msg_part_1	; Always print "Disk Error: " part.
	assume	es:screen	; Use screen as extra segment
	mov	dx,screen
	mov	es,dx
	mov	di,screen_seg_offset	; DI will be pointer to screen position
	add	di,first_position	; Add to point to desired area on screen
	call	write_to_screen		; This writes 12 chars from [SI] to [DI]
	mov	dx,80h			; Initialize for later comparisons
	mov	cx,7			; Loop seven times
*/
e_loop:	cmp	ah,dh			; Are error code and DH the same?
	je	e_found			; If yes, Error has been found
	add	si,12			; Point to next error message
	; # shr	dh,1			; Divide DH by 2
	/* loop	e_loop			; Keep going until matched  DH = 0
	/* cmp	ah,3			; Error code no even number; 3 perhaps? */
	*/
	cmp	ah,3			; Error code no even number; 3 perhaps?
	je	e_found			; If yes, have found the error
	add	si,12			; Err unknown; unknown error returned
e_found:call	write_to_screen		; Write the error message to the screen
	pop	es		; Restore the registers
	pop	si
	pop	di
	pop	dx
	pop	cx
	pop	ax
/* fin:	pop	ret_addr_word		; Fooling with the stack. We want to
	pop	ret_addr_word[2]	; preserve the flags but the old flags
	add	sp,2			; are still on the stack. First remove
	push	flags			; return address, then flags. Fill flags
	popf				; from "FLAGS", return to correct addr.
	jmp	ret_addr*/
disk_watch	endp

write_to_screen	proc	near	; Puts 12 characters on screen
	mov	cx,12		; Loop 12 times
w_loop:	movs	es:byte ptr[di],cs:[si] ; Move to the screen
	mov	al,7		; Move screen attribute into screen buffer
	mov	es:[di],al
	inc	di		; Point to next byte in screen buffer
	loop	w_loop		; Keep going until done
	ret
write_to_screen	endp

load_watch	proc	near	; This procedure initializes everything
	assume	ds:interrupts	; The data segment will be the interrupt area
	mov	ax,interrupts
	mov	ds,ax

	mov	ax,disk_int	; Get the old interrupt service routine
	mov	old_disk_int,ax	; address and put it into our location
	mov	ax,disk_int[2]	; OLD_DISK_INT so we can call it.
	mov	old_disk_int[2],ax

	# mov	disk_int,offset disk_watch  ; Now load the address of DskWatch
	; mov	disk_int[2],cs		; routine into the disk interrupt

	mov	ah,15		; Ask for service 15 of INT 10h
	int	10h		; This tells us how display is set up
	sub	ah,25		; Move to twenty five places before edge
	# shl	ah,1		; Mult. by two (char & attribute bytes)
	mov	byte ptr first_position,ah	; Set screen cursor
	# test	al,4		; Is it a monochrome display?
	jnz	exit		; Yes - jump out
	mov	screen_seg_offset,8000h	; No, set up for graphics display
exit:	mov	dx,offset load_watch	; Set up everything but this program to
	int	27h			; stay and attach itself to DOS
load_watch	endp
	code_seg	ends
	end	first	; END "FIRST" so 8088 will go to FIRST first.
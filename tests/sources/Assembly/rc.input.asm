



interrupts	segment at 0h	
	org	13h*4		
disk_int	label	dword
interrupts	ends




code_seg	segment
	assume	cs:code_seg
	org	0100h		
first:	jmp	load_watch	

	msg_part_1	db	'Disk error: '	
	msg_part_2	db	'No response Failed Seek NEC Error   '
			db	'Bad CRC SeenDMA Overrun Impos Sector'
			db	'No Addr MarkW. ProtectedErr Unknown '
	first_position	dw	?		
	flags		dw	?
	screen_seg_offset dw	0		
	old_disk_int	dd	?		
	ret_addr	label dword		
	ret_addr_word	dw 2 dup(?)		


disk_watch	proc	far	
	assume	cs:code_seg
	pushf			
	call	old_disk_int
	pushf			
	pop	flags		
	jc	error		
	jmp	fin		

e_loop:	cmp	ah,dh			
	je	e_found			
	add	si,12			
	
	
	
	cmp	ah,3			
	je	e_found			
	add	si,12			
e_found:call	write_to_screen		
	pop	es		
	pop	si
	pop	di
	pop	dx
	pop	cx
	pop	ax

disk_watch	endp

write_to_screen	proc	near	
	mov	cx,12		
w_loop:	movs	es:byte ptr[di],cs:[si] 
	mov	al,7		
	mov	es:[di],al
	inc	di		
	loop	w_loop		
	ret
write_to_screen	endp

load_watch	proc	near	
	assume	ds:interrupts	
	mov	ax,interrupts
	mov	ds,ax

	mov	ax,disk_int	
	mov	old_disk_int,ax	
	mov	ax,disk_int[2]	
	mov	old_disk_int[2],ax

	
	

	mov	ah,15		
	int	10h		
	sub	ah,25		
	
	mov	byte ptr first_position,ah	
	
	jnz	exit		
	mov	screen_seg_offset,8000h	
exit:	mov	dx,offset load_watch	
	int	27h			
load_watch	endp
	code_seg	ends
	end	first	
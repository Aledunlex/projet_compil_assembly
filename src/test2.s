.text
.globl main
main:
movq $2, %rbx
movq %rbx, %rdx
movq $7, %rcx
movq %rcx, %r8
movq %rdx, %r9
movq %r8, %r10
imulq %r10, %r9
movq $1, %r11
movq %r9, %rdi
movq %r11, %rax
subq %rax, %rdi
call print_int
ret
print_int:
	movq %rdi, %rsi
	movq $message, %rdi
	movq $0, %rax
	call printf
	ret
.data
message:
	.string "%d"

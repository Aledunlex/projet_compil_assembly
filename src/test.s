.text
.globl main
main:
movq $2, %rbx
movq $3, %rdx
movq %rbx, %rcx
movq %rdx, %r8
imulq %r8, %rcx
movq $1, %r9
movq %rcx, %rdi
movq %r9, %rax
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
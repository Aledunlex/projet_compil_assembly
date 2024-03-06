.text
.globl main
main:
    movq $2, %rax
    movq $3, %rbx
    imulq %rbx, %rax
    movq $1, %rcx
    subq %rcx, %rax
    movq %rax, %rdi
    call print_int
    ret
print_int: # rdi est utilisé comme paramètre
    movq %rdi, %rsi
    movq $message, %rdi # format pour printf
    movq $0, %rax
    call printf
    ret
.data
message:
.string "%d\n"
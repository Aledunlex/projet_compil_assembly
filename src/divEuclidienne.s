.data
    result_string:
    .string "Result: %d\n"

.text
.globl main
main:
    movq $6, %rdi # move a to rdi
    movq $3, %rsi # move b to rsi
    call euclidean_div
    ret

.globl euclidean_div
euclidean_div:
    movq %rdi, %rax # move a to rax
    movq %rsi, %rbx # move b to rbx
    cqto # sign-extend rax into rdx
    idivq %rbx # signed integer division, result in rax, remainder in rdx
    movq %rax, %rdi # move quotient to rdi
    movq $result_string, %rsi # format string for printf
    movq $0, %rax # set return value to 0
    call printf
    ret

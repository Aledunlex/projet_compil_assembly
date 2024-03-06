import sys

from C_gen3adresses import Generator
from utils import parse_program


class Alloc:

    def alloc_reg(self, gen3addresses, index):
        code_assembler = ".text\n.globl main\nmain:\n"

        reg_list = ["%rbx", "%rdx", "%rcx", "%r8", "%r9", "%r10", "%r11", "%r12", "%r13", "%r14", "%r15"]

        for i in range(index - 2):
            gen3addresses = gen3addresses.replace(f"temp_{i}", reg_list[i])

        gen3addresses = gen3addresses.replace(f"temp_{index - 2}", "%rdi")
        gen3addresses = gen3addresses.replace(f"temp_{index - 1}", "%rax")

        code_assembler += gen3addresses

        code_assembler += "call print_int \nret\n"
        code_assembler += "print_int:\n\tmovq %rdi, %rsi\n\tmovq $message, %rdi\n\tmovq $0, %rax\n\t" \
                          "call printf\n\tret\n.data\n"
        code_assembler += "message:\n\t.string \"%d\""

        return code_assembler


if __name__ == "__main__":
    ast = parse_program(sys.argv[1])
    generator = Generator()
    generator.gen(ast)
    alloc = Alloc()
    print(alloc.alloc_reg(generator.expression, generator.index))

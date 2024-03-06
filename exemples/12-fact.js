function factorial(n) {
    if (n < 2) {
        return 1;  // 0! = 1! = 1
    }
    return n * factorial(n - 1);
} ;

print_int(factorial(21)); // 6

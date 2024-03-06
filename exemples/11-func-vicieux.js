var x = 10;

function blob(n) {
    x = x + n;
    return x;
} ;

print_int(blob(1));
print_string(blob("a"));

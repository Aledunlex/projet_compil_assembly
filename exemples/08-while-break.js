var x = 0;
var y = 8;

while (x < 10) {
    if (x == y) {
        break;
    }
    x += 1 ;
    if (x < 2) {
        continue;
    }
    print_int(x);
}

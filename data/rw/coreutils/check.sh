cd coreutils
cp ../p.c src/
gcc -I. -I./lib  -Ilib -I./lib -Isrc -I./src -Werror -Wall -Warith-conversion -Wbad-function-cast -Wcast-align=strict -Wdate-time -Wdisabled-optimization -Wdouble-promotion -Wduplicated-branches -Wduplicated-cond -Wextra -Wformat-signedness -Winit-self -Winvalid-pch -Wlogical-op -Wmissing-declarations -Wmissing-include-dirs -Wmissing-prototypes -Wnull-dereference -Wold-style-definition -Wopenmp-simd -Woverlength-strings -Wpacked -Wpointer-arith -Wshadow -Wstrict-overflow -Wstrict-prototypes -Wsuggest-attribute=cold -Wsuggest-attribute=const -Wsuggest-attribute=format -Wsuggest-attribute=malloc -Wsuggest-attribute=noreturn -Wsuggest-attribute=pure -Wsuggest-final-methods -Wsuggest-final-types -Wsync-nand -Wtrampolines -Wuninitialized -Wunknown-pragmas -Wno-unused-macros -Wvariadic-macros -Wvla -Wwrite-strings -Warray-bounds=2 -Wattribute-alias=2 -Wformat=2 -Wimplicit-fallthrough=5 -Wshift-overflow=2 -Wno-unused-const-variable -Wno-unused-function -Wvla-larger-than=4031 -Wno-sign-compare -Wno-unused-parameter -Wno-format-nonliteral -fdiagnostics-show-option -funit-at-a-time -Wno-return-local-addr -Wno-stringop-overflow -Wno-unused-macros -g -O2 -Wl,--as-needed  -o src/p src/p.c src/libver.a lib/libcoreutils.a   lib/libcoreutils.a -ldl

if [ $? -ne 0 ]; then
    echo "compilation error"
    exit 2
fi

./src/p
if [ $? -ne 0 ]; then
    echo "assertion error"
    exit 1
fi
cd ..
exit 0

from main import main, get_parser

size = []
rust = []
numpy = []

for magnitude in range(5):
    for factor in [1, 3]:
        s = factor*(10**magnitude)
        size.append(s)
        for engine in ['rust', 'numpy']:
            config = f"--seed 55 --no-display --engine {engine} -n {s} -p {s}"          
            args = get_parser().parse_args(config.split())
            locals()[engine].append(main(args))
print("size   \t rust   \t numpy")
for s, rst, np in zip(size, rust, numpy):
    print(f"{s} \t {rst:.4f} \t {np:.4f}")
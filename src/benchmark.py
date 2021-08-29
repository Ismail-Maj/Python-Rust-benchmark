from main import main, get_parser

size = []
rust_multicore = []
rust = []
numpy = []
python = []

for magnitude in range(6):
    for factor in [1, 3]:
        s = factor*(10**magnitude)
        size.append(s)
        for engine in ['rust-multicore', 'rust', 'numpy', 'python']:
            if s > 10000 and engine == "python":
                python.append(0)
                continue
            if s > 30000 and engine == "numpy":
                numpy.append(0)
                continue
            config = f"--seed 55 --no-display --engine {engine} -n {s} -p {s}"          
            args = get_parser().parse_args(config.split())
            locals()[engine.replace('-','_')].append(main(args))

print("size   \t python   \t numpy   \t rust    \t rust-multicore")
for s, py, np, rst, rstM in zip(size, python, numpy, rust, rust_multicore):
    print(f"{s} \t {py:.4f} \t {np:.4f} \t {rst:.4f} \t {rstM:.4f}")
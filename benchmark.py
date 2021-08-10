from main import main, get_parser

#size = [1, 5, 10, 20, 50, 100, 200, 500, 1000, 5000, 10000, 20000, 30000]
size = [1, 5, 10, 20, 50, 100, 200, 500, 1000]
python = []
numpy = []
rust = []

for s in size:
    for engine in ['python', 'rust', 'numpy']:
        if engine == "python" and s > 10000: # lists aren't memory efficient
            python.append(0)
            continue
        config = f"--seed 55 --display False --engine {engine} -n {s} -p {s}"            
        args = get_parser().parse_args(config.split())
        locals()[engine].append(main(args))

print("size   \t python   \t rust   \t numpy")
for s, py, rst, np in zip(size, python, rust, numpy):
    print(f"{s} \t {py:.4f} \t {rst:.4f} \t {np:.4f}")


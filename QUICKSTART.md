# Quick Reference

## 🚀 Quick Start

```bash
# 1. Install dependencies
sudo apt install libsfml-dev libtbb-dev cmake build-essential

# 2. Build
cmake -S . -B build/release -DCMAKE_BUILD_TYPE=Release
cmake --build build/release

# 3. Run
./build/release/mandelbrot

# 4. View output
ls -lh mandelbrot.png grain_time.txt
```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | Main project documentation, overview, and getting started |
| [docs/USAGE.md](docs/USAGE.md) | Detailed usage instructions and parameter modifications |
| [docs/PERFORMANCE.md](docs/PERFORMANCE.md) | Performance analysis and optimization guide |
| [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) | Project organization and file structure |

## 📁 Project Structure

```
IMAPP25-mandelbrot/
├── src/                   # Source code
├── docs/                  # Documentation
├── output/                # Generated images
├── results/               # Performance data
└── CMakeLists.txt         # Build configuration
```

## 🎯 Common Tasks

### Build in Debug mode (with sanitizers)
```bash
cmake -S . -B build/debug -DCMAKE_BUILD_TYPE=Debug
cmake --build build/debug
./build/debug/mandelbrot
```

### Modify visualization parameters
Edit `src/main.cpp` to change:
- Resolution (default: 800×800)
- Complex plane region
- Maximum iterations (default: 256)
- Color scheme
- Grain sizes to test

### Analyze performance results
```bash
cat grain_time.txt
# Import into spreadsheet or plotting tool
```

## 🔍 Understanding Output

**mandelbrot.png**: 800×800 pixel visualization of the Mandelbrot set
- Black = inside the set
- Red gradient = outside the set (colored by escape time)

**grain_time.txt**: Performance data for different grain sizes
- Format: `grain_size seconds`
- Used to find optimal parallelization strategy

## ⚡ Performance Tips

- Use **Release mode** for accurate performance measurements
- Optimal grain size is typically **16-128** pixels
- Close background applications during benchmarking
- See [docs/PERFORMANCE.md](docs/PERFORMANCE.md) for detailed analysis

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Build errors | Check dependencies are installed |
| Slow execution | Use Release mode, not Debug |
| Missing output | Check write permissions |
| Different results | Performance varies by hardware |

For detailed troubleshooting, see [docs/USAGE.md](docs/USAGE.md#troubleshooting)

## 📖 Learn More

- **What is Mandelbrot Set?** → [README.md](README.md#what-is-the-mandelbrot-set)
- **How does parallelization work?** → [docs/PERFORMANCE.md](docs/PERFORMANCE.md#parallelization-strategy)
- **How to modify the code?** → [docs/USAGE.md](docs/USAGE.md#modifying-parameters)
- **What do the files do?** → [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)

## 🎓 Course Context

This project is part of the IMAPP25 course and demonstrates:
- Parallel computing with TBB
- Performance optimization techniques
- Fractal generation algorithms
- Benchmarking and analysis methods

# Mandelbrot Set Visualization and Performance Analysis

A parallel implementation of the Mandelbrot set generator using Intel's oneAPI Threading Building Blocks (TBB). This project demonstrates high-performance computing techniques for generating fractal images and analyzing the performance impact of different parallelization grain sizes.

## Table of Contents

- [Overview](#overview)
- [What is the Mandelbrot Set?](#what-is-the-mandelbrot-set)
- [Project Structure](#project-structure)
- [Features](#features)
- [Dependencies](#dependencies)
- [Building the Project](#building-the-project)
- [Running the Program](#running-the-program)
- [Understanding the Output](#understanding-the-output)
- [Performance Analysis](#performance-analysis)
- [Technical Details](#technical-details)

## Overview

This project is part of the IMAPP25 course and serves as a starting point for exploring parallel computing concepts through the visualization of the Mandelbrot set. The program generates a high-resolution PNG image of the famous Mandelbrot fractal while measuring the performance impact of different parallelization strategies.

## What is the Mandelbrot Set?

The Mandelbrot set is a famous mathematical fractal discovered by Benoit Mandelbrot in 1980. It is defined as the set of complex numbers `c` for which the iterative function:

```
z(n+1) = z(n)² + c
```

remains bounded when starting from `z(0) = 0`. In simpler terms, the Mandelbrot set consists of all complex numbers that don't "escape to infinity" under this iteration.

The visualization colors each pixel based on how many iterations it takes for the point to escape (exceed a magnitude of 2), creating the characteristic intricate patterns and self-similar structures that make the Mandelbrot set one of the most recognizable fractals in mathematics.

## Project Structure

```
IMAPP25-mandelbrot/
├── src/                    # Source code files
│   └── main.cpp           # Main program implementation
├── docs/                   # Documentation files
├── output/                 # Generated images (gitignored)
│   └── mandelbrot.png     # Generated fractal visualization
├── results/                # Performance measurement results (gitignored)
│   └── grain_time.txt     # Grain size performance data
├── CMakeLists.txt         # CMake build configuration
├── README.md              # This file
└── .gitignore             # Git ignore rules
```

## Features

- **Parallel Processing**: Utilizes Intel TBB for efficient multi-threaded computation
- **Performance Benchmarking**: Tests multiple grain sizes to find optimal parallelization strategy
- **High-Resolution Output**: Generates 800×800 pixel PNG images
- **Configurable Parameters**: Easy to modify visualization parameters (resolution, complex plane bounds, iteration limits)
- **Performance Data Export**: Automatically generates timing data for analysis

## Dependencies

The program requires the following libraries:

- **SFML (Simple and Fast Multimedia Library)**: Used for image creation and PNG file export
- **oneTBB (Threading Building Blocks)**: Provides parallel processing capabilities
- **C++20 compatible compiler**: GCC 10+ or Clang 10+ recommended
- **CMake 3.16+**: For building the project

### Installation on Ubuntu/Debian

Install all required dependencies with:

```shell
sudo apt update
sudo apt install libsfml-dev libtbb-dev cmake build-essential
```

### Installation on macOS

```shell
brew install sfml tbb cmake
```

### Installation on Windows

Use vcpkg or download the libraries manually from their respective websites.

## Building the Project

### Debug Build

Debug builds include address sanitizer and additional debugging symbols:

```shell
cmake -S . -B build/debug -DCMAKE_BUILD_TYPE=Debug
cmake --build build/debug
```

### Release Build

Release builds are optimized for performance:

```shell
cmake -S . -B build/release -DCMAKE_BUILD_TYPE=Release
cmake --build build/release
```

## Running the Program

After building, run the executable:

```shell
# For debug build
./build/debug/mandelbrot

# For release build
./build/release/mandelbrot
```

The program will:
1. Test different grain sizes (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048)
2. Generate performance timing data
3. Create a PNG image of the Mandelbrot set

### Execution Time

Execution time varies depending on your hardware:
- Typical desktop (4-8 cores): 1-5 seconds total
- High-end workstation (16+ cores): < 1 second total
- Each grain size test takes a fraction of a second

## Understanding the Output

### Generated Image: `mandelbrot.png`

The output is an 800×800 pixel image showing:
- **Black regions**: Points inside the Mandelbrot set (never escape)
- **Red gradient**: Points outside the set, colored by escape iteration count
- **Complex boundary**: The intricate fractal boundary between the two regions

The visualization covers the complex plane region:
- Real axis: -2.2 to 0.8
- Imaginary axis: -1.5 to 1.5

This region captures the most visually interesting part of the Mandelbrot set, including the main cardioid, circular bulb, and the intricate self-similar structures extending from them.

### Performance Data: `grain_time.txt`

This file contains timing results for each grain size tested. Format:
```
grain_size seconds
1 0.141317
2 0.112635
...
```

**Grain size** refers to the size of work units distributed to threads. Smaller grain sizes provide better load balancing but higher scheduling overhead, while larger grain sizes reduce overhead but may lead to load imbalance.

## Performance Analysis

The program tests various grain sizes to help you understand the trade-offs in parallel programming:

- **Small grain sizes (1-8)**: Better load balancing, higher overhead
- **Medium grain sizes (16-128)**: Often optimal performance
- **Large grain sizes (256-2048)**: Lower overhead, potential load imbalance

Optimal grain size depends on:
- Number of CPU cores available
- Cache characteristics
- Problem complexity

For more detailed performance analysis, see [PERFORMANCE.md](docs/PERFORMANCE.md) (if available).

## Technical Details

### Algorithm

1. **Mandelbrot Iteration**: For each pixel, compute the corresponding complex number `c`
2. **Escape Test**: Iterate `z = z² + c` up to 256 times
3. **Coloring**: Color based on the iteration count when |z| > 2
4. **Parallelization**: Use TBB's `parallel_for` with 2D blocked ranges

### Key Parameters

- **Image Resolution**: 800×800 pixels
- **Maximum Iterations**: 256
- **Escape Threshold**: |z| < 2 (or norm(z) < 4)
- **Complex Plane Bounds**: [-2.2 + 1.5i, 0.8 - 1.5i]

### Code Organization

The main components are:

- `mandelbrot()`: Computes escape time for a complex number
- `to_color()`: Converts iteration count to RGB color
- `main()`: Orchestrates the parallel computation and benchmarking

## Further Reading

- [Mandelbrot Set on Wikipedia](https://en.wikipedia.org/wiki/Mandelbrot_set)
- [Intel oneTBB Documentation](https://www.intel.com/content/www/us/en/docs/onetbb/developer-guide-api-reference/current/overview.html)
- [SFML Graphics Module](https://www.sfml-dev.org/documentation/2.5.1/group__graphics.php)

## License

This project is part of the IMAPP25 course materials.

## Contributing

This is an educational project. Students should follow course guidelines for modifications and submissions.

![Mandelbrot Set Visualization](output/mandelbrot.png)

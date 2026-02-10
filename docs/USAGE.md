# Usage Guide

## Quick Start

```shell
# Build the project
cmake -S . -B build/release -DCMAKE_BUILD_TYPE=Release
cmake --build build/release

# Run the program
./build/release/mandelbrot

# View the output
ls -lh mandelbrot.png grain_time.txt
```

## Build Options

### Debug Mode
Debug mode includes address sanitizer for detecting memory errors:
```shell
cmake -S . -B build/debug -DCMAKE_BUILD_TYPE=Debug
cmake --build build/debug
./build/debug/mandelbrot
```

Use debug mode when:
- Developing or modifying the code
- Debugging memory issues
- Testing for undefined behavior

### Release Mode
Release mode enables all optimizations for maximum performance:
```shell
cmake -S . -B build/release -DCMAKE_BUILD_TYPE=Release
cmake --build build/release
./build/release/mandelbrot
```

Use release mode when:
- Running performance benchmarks
- Generating final results
- Measuring actual execution times

## Output Files

The program generates two files in the current directory:

### 1. mandelbrot.png
- High-resolution image (800×800 pixels)
- PNG format, can be viewed with any image viewer
- Contains the visualization of the Mandelbrot set
- File size: approximately 50-200 KB depending on the complexity

### 2. grain_time.txt
- Plain text file with performance measurements
- Two columns: grain_size and execution time in seconds
- Can be imported into spreadsheet software for analysis
- Used for comparing different parallelization strategies

## Modifying Parameters

To change the visualization parameters, edit `src/main.cpp`:

### Resolution
```cpp
int const display_width{800};   // Change to desired width
int const display_height{800};  // Change to desired height
```

### Visualization Region
```cpp
Complex const top_left{-2.2, 1.5};      // Top-left corner in complex plane
Complex const lower_right{0.8, -1.5};   // Bottom-right corner
```

Common interesting regions:
- Full view: `{-2.2, 1.5}` to `{0.8, -1.5}`
- Zoom on "tail": `{-0.8, 0.2}` to `{-0.7, 0.1}`
- Zoom on spiral: `{-0.75, 0.15}` to `{-0.73, 0.13}`

### Maximum Iterations
```cpp
for (; i != 256 && std::norm(z) < 4.; ++i) {
    // Change 256 to increase detail (slower)
    // Higher values reveal more detail at boundaries
}
```

### Grain Sizes to Test
```cpp
std::vector<int> grain_sizes = {1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048};
// Add or remove values to test different grain sizes
```

### Color Scheme
```cpp
auto to_color(int k)
{
  // Modify this function to change colors
  return k < 256 ? sf::Color{static_cast<sf::Uint8>(10 * k), 0, 0}
                 : sf::Color::Black;
}
```

Example alternative color schemes:
- Blue gradient: `{0, 0, static_cast<sf::Uint8>(10 * k)}`
- Green gradient: `{0, static_cast<sf::Uint8>(10 * k), 0}`
- Grayscale: `{static_cast<sf::Uint8>(k), static_cast<sf::Uint8>(k), static_cast<sf::Uint8>(k)}`

## Performance Tips

### For Faster Execution
1. Use Release build mode
2. Close other applications to free CPU cores
3. Use optimal grain size (typically 16-128)
4. Reduce image resolution for testing

### For Better Quality
1. Increase maximum iterations (e.g., 512 or 1024)
2. Increase image resolution (e.g., 1600×1600)
3. Zoom into specific regions for detailed views

### For Performance Analysis
1. Always use Release mode
2. Run multiple times and average results
3. Test a wide range of grain sizes
4. Monitor CPU usage during execution

## Troubleshooting

### Build Errors

**Error: "SFML not found"**
```shell
sudo apt install libsfml-dev  # Ubuntu/Debian
brew install sfml             # macOS
```

**Error: "TBB not found"**
```shell
sudo apt install libtbb-dev   # Ubuntu/Debian
brew install tbb              # macOS
```

**Error: "CMake version too old"**
```shell
sudo apt install cmake        # Install latest version
# Or download from cmake.org
```

### Runtime Errors

**Error: "Segmentation fault"**
- Try Debug build to identify the issue
- Address sanitizer will provide detailed error information

**Error: "Failed to save image"**
- Check disk space
- Verify write permissions in current directory
- Ensure SFML is properly installed

### Performance Issues

**Program runs very slowly**
- Ensure you're using Release build, not Debug
- Check if other applications are using CPU
- Verify TBB is properly linked (check with `ldd ./build/release/mandelbrot`)

**All grain sizes have similar performance**
- System may have limited cores (check with `nproc` or `lscpu`)
- Background processes may be consuming CPU
- Try larger image resolutions to see more pronounced differences

## Advanced Usage

### Running with Custom Output Location
```shell
cd /desired/output/directory
/path/to/build/release/mandelbrot
```

### Analyzing Results with Python
```python
import pandas as pd
import matplotlib.pyplot as plt

# Read timing data
data = pd.read_csv('grain_time.txt', sep=' ')

# Plot performance vs grain size
plt.figure(figsize=(10, 6))
plt.plot(data['grain_size'], data['seconds'], marker='o')
plt.xlabel('Grain Size')
plt.ylabel('Execution Time (seconds)')
plt.title('Performance vs Grain Size')
plt.xscale('log', base=2)
plt.grid(True)
plt.savefig('performance_analysis.png')
plt.show()
```

### Batch Processing Different Parameters
Create a shell script to test different configurations:
```bash
#!/bin/bash
for resolution in 400 800 1600; do
    # Modify main.cpp with desired resolution
    # Rebuild and run
    # Save results with unique names
done
```

## Getting Help

For questions or issues:
1. Check the main [README.md](../README.md)
2. Review the [PERFORMANCE.md](PERFORMANCE.md) for optimization tips
3. Consult course materials and documentation
4. Examine the source code comments in `src/main.cpp`

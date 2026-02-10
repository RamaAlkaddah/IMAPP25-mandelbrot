# Performance Analysis Guide

## Understanding Parallel Performance

This document explains the performance characteristics of the Mandelbrot set generator and how different parameters affect execution time.

## Table of Contents

- [Parallelization Strategy](#parallelization-strategy)
- [Grain Size Impact](#grain-size-impact)
- [Performance Metrics](#performance-metrics)
- [Optimization Techniques](#optimization-techniques)
- [Hardware Considerations](#hardware-considerations)
- [Interpreting Results](#interpreting-results)

## Parallelization Strategy

### Threading Model

The program uses Intel's oneAPI Threading Building Blocks (TBB) for parallel execution:

- **Work Distribution**: The image is divided into 2D rectangular tiles
- **Thread Pool**: TBB manages a pool of worker threads (typically one per CPU core)
- **Load Balancing**: TBB automatically distributes tiles to available threads
- **Simple Partitioner**: Ensures predictable, non-adaptive work distribution

### Parallel For Loop

```cpp
oneapi::tbb::parallel_for(
  oneapi::tbb::blocked_range2d<int>(
    0, display_height, grain_size,  // Rows dimension
    0, display_width,  grain_size   // Columns dimension
  ),
  [&](const oneapi::tbb::blocked_range2d<int>& r) {
    // Process tile
  },
  oneapi::tbb::simple_partitioner{}
);
```

Each tile is a `grain_size × grain_size` block of pixels processed independently.

## Grain Size Impact

### What is Grain Size?

**Grain size** determines the size of work units (tiles) that are distributed to threads:
- Smaller grain size = more tiles = better load balancing but higher overhead
- Larger grain size = fewer tiles = less overhead but potential load imbalance

### Performance Trade-offs

#### Small Grain Sizes (1-8 pixels)

**Advantages:**
- Excellent load balancing
- Threads rarely sit idle
- Good for non-uniform workloads

**Disadvantages:**
- High scheduling overhead
- More context switching
- Cache inefficiency due to small working sets

**Typical Performance:** Slower due to overhead

#### Medium Grain Sizes (16-128 pixels)

**Advantages:**
- Good balance between overhead and load balancing
- Better cache utilization
- Moderate number of tiles

**Disadvantages:**
- May not perfectly distribute work
- Some threads may finish earlier

**Typical Performance:** Usually optimal

#### Large Grain Sizes (256-2048 pixels)

**Advantages:**
- Low scheduling overhead
- Excellent cache utilization
- Minimal context switching

**Disadvantages:**
- Poor load balancing
- Some threads may be underutilized
- Less flexibility in work distribution

**Typical Performance:** Slower due to load imbalance

### Optimal Grain Size

The optimal grain size depends on:

1. **Number of CPU cores**: More cores need smaller grain sizes
2. **Cache size**: Larger caches benefit from larger grain sizes
3. **Image resolution**: Higher resolutions allow larger grain sizes
4. **Workload uniformity**: Mandelbrot computation varies by region

**Rule of Thumb:**
- For 4-8 cores: grain size of 32-64 often optimal
- For 16+ cores: grain size of 16-32 often optimal
- Total tiles should be 4-8× the number of cores

## Performance Metrics

### Execution Time

The primary metric is wall-clock time in seconds for completing the entire image.

**Expected Performance (800×800 resolution, Release build):**
- 4-core CPU: 0.1-0.3 seconds per grain size test
- 8-core CPU: 0.05-0.15 seconds per grain size test
- 16-core CPU: 0.03-0.08 seconds per grain size test

### Speedup

Speedup = (Sequential Time) / (Parallel Time)

**Theoretical Maximum:** Number of CPU cores (Amdahl's Law applies)

**Actual Speedup Factors:**
- 4 cores: 3-3.5× faster than sequential
- 8 cores: 5-7× faster than sequential
- 16 cores: 10-14× faster than sequential

### Efficiency

Efficiency = Speedup / Number of Cores

**Good Efficiency:** 70-90%
**Excellent Efficiency:** 90%+

### Scalability

How performance improves with more cores:
- **Strong Scaling**: Fixed problem size, increasing cores
- **Weak Scaling**: Problem size increases with cores

This implementation focuses on strong scaling.

## Optimization Techniques

### Already Implemented

1. **Parallel Processing**: TBB parallel_for for multi-threading
2. **Simple Partitioner**: Deterministic work distribution
3. **Cache-Friendly**: 2D blocked iteration pattern
4. **Compiler Optimizations**: Release mode enables -O3, vectorization

### Potential Improvements

1. **Adaptive Grain Size**: Use `auto_partitioner` instead of `simple_partitioner`
2. **SIMD Vectorization**: Process multiple pixels simultaneously
3. **Early Termination**: Skip obviously inside/outside regions
4. **Color Computation**: Pre-compute color table instead of calculating each time
5. **Memory Layout**: Optimize data structure for cache efficiency
6. **Algorithmic**: Use periodicity checking to reduce iterations

### Code-Level Optimizations

```cpp
// Current implementation
auto k = mandelbrot(top_left + Complex{delta_x * column, delta_y * row});

// Potential optimization: cache complex numbers
Complex c = top_left + Complex{delta_x * column, delta_y * row};
auto k = mandelbrot(c);
```

```cpp
// Current color computation (per pixel)
auto to_color(int k) { ... }

// Optimized: pre-computed lookup table
std::array<sf::Color, 257> color_table;
// Initialize once, lookup many times
```

## Hardware Considerations

### CPU Architecture

**Factors Affecting Performance:**

1. **Core Count**: More cores allow better parallelization
2. **Cache Hierarchy**: L1/L2/L3 cache sizes affect grain size optimization
3. **Memory Bandwidth**: Can bottleneck with many cores
4. **Hyperthreading**: May provide 10-30% additional performance

### CPU Cache

**Cache Levels:**
- **L1 Cache**: 32-64 KB per core, fastest access
- **L2 Cache**: 256-512 KB per core, medium access
- **L3 Cache**: 8-32 MB shared, slower access

**Grain Size and Cache:**
- Each tile should fit in L2 cache when possible
- 64×64 tile = 4,096 pixels ≈ 16 KB of data (fits in L2)
- 128×128 tile = 16,384 pixels ≈ 64 KB of data (may exceed L2)

### NUMA Considerations

On multi-socket systems:
- Each socket has its own memory controllers
- Memory access time varies by location (local vs. remote)
- TBB is NUMA-aware but may require tuning

## Interpreting Results

### Analyzing grain_time.txt

Example output:
```
grain_size seconds
1 0.141317
2 0.112635
4 0.098572
8 0.0906322
16 0.0880396
32 0.0879084
64 0.0870741
128 0.0873336
256 0.087815
512 0.0887895
1024 0.15876
2048 0.158713
```

**Analysis:**

1. **Very small grain sizes (1-8)**: High overhead visible
2. **Optimal range (16-128)**: Performance plateau at ~0.087 seconds
3. **Large grain sizes (512-2048)**: Performance degrades due to load imbalance

**Optimal grain size**: 64 (0.0870741 seconds)

### Performance Curve

Typical performance curve:
```
        ^
  Time  |     *
        |    *
        |  *
        | *
        |*
        +*-------------*-*-*-*-------*---*--> Grain Size
         1 2 4 8 16 32 64 128 256 512 1024
         
         |<-Overhead->|<-Sweet Spot->|<-Imbalance->|
```

### Common Patterns

**Pattern 1: Clear Optimum**
- Smooth decrease, flat middle, smooth increase
- Indicates good parallelization
- Clear optimal grain size

**Pattern 2: Minimal Variation**
- All grain sizes similar performance
- May indicate limited cores or sequential bottleneck
- Check system resources

**Pattern 3: Monotonic Decrease**
- Larger grain sizes always faster
- May indicate overhead dominates
- Consider increasing problem size

## Benchmarking Best Practices

### Consistent Environment

1. **Close Background Applications**: Minimize CPU competition
2. **Disable CPU Frequency Scaling**: Use performance governor
3. **Cool System**: Avoid thermal throttling
4. **Consistent Power Mode**: Plug in laptop, disable power saving

### Multiple Runs

```shell
for i in {1..5}; do
    ./build/release/mandelbrot
    mv grain_time.txt grain_time_$i.txt
done
```

Then average the results for more reliable data.

### System Information

Record system specs for context:
```shell
lscpu                    # CPU information
free -h                  # Memory information
cat /proc/cpuinfo        # Detailed CPU info
```

## Performance Analysis Tools

### Command-Line Tools

```shell
# Monitor CPU usage during execution
htop

# Measure execution time
time ./build/release/mandelbrot

# Profile with perf (Linux)
perf stat -d ./build/release/mandelbrot

# Check thread usage
ps -eLf | grep mandelbrot
```

### Profiling Tools

- **Valgrind/Callgrind**: Function-level profiling
- **Intel VTune**: Advanced performance analysis
- **perf**: Linux performance counter tool
- **gprof**: GNU profiler

### Visualization

Use Python/matplotlib or Excel to create graphs:
- Execution time vs grain size (line plot)
- Speedup vs number of cores (if testing)
- Efficiency vs grain size (derived metric)

## Expected Results

### Typical Performance Range

**800×800 image, Release build, modern CPU:**

| Grain Size | Expected Time | Performance |
|------------|---------------|-------------|
| 1-8        | 0.10-0.15s   | Slow (overhead) |
| 16-64      | 0.08-0.09s   | Optimal |
| 128-256    | 0.08-0.10s   | Good |
| 512-2048   | 0.10-0.20s   | Slow (imbalance) |

### Performance Goals

- **Good**: Optimal grain size 2× faster than worst
- **Excellent**: Optimal grain size 3× faster than worst
- **Outstanding**: Near-linear speedup with core count

## Further Exploration

### Experiments to Try

1. **Vary Image Resolution**: Test 400×400, 800×800, 1600×1600
2. **Different Regions**: Some areas compute faster than others
3. **Iteration Limits**: Test 128, 256, 512, 1024 max iterations
4. **Different Partitioners**: Try `auto_partitioner`, `affinity_partitioner`
5. **Thread Count**: Manually limit threads with `task_scheduler_init`

### Research Questions

- How does cache size affect optimal grain size?
- What's the relationship between grain size and core count?
- How does the Mandelbrot computation pattern affect load balancing?
- Can we predict optimal grain size from system parameters?

## Conclusion

Performance optimization is a balance between:
- **Parallelization Overhead**: Cost of managing threads and tasks
- **Load Balancing**: Ensuring all threads have equal work
- **Cache Efficiency**: Keeping data in fast memory

The optimal grain size strikes this balance, and understanding these trade-offs is key to writing high-performance parallel code.

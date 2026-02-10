# Project Structure

This document explains the organization of files and directories in this project.

## Directory Structure

```
IMAPP25-mandelbrot/
│
├── src/                        # Source code directory
│   └── main.cpp               # Main program implementation
│
├── docs/                       # Documentation directory
│   ├── USAGE.md               # Detailed usage instructions
│   ├── PERFORMANCE.md         # Performance analysis guide
│   └── PROJECT_STRUCTURE.md   # This file
│
├── output/                     # Generated images (gitignored)
│   └── mandelbrot.png         # Generated fractal visualization
│
├── results/                    # Performance data (gitignored)
│   └── grain_time.txt         # Grain size timing measurements
│
├── build/                      # Build directory (gitignored)
│   ├── debug/                 # Debug build artifacts
│   └── release/               # Release build artifacts
│
├── CMakeLists.txt             # CMake build configuration
├── README.md                  # Main project documentation
└── .gitignore                 # Git ignore rules
```

## File Descriptions

### Root Directory Files

#### `CMakeLists.txt`
**Purpose:** CMake build configuration file

**Contents:**
- Project name and version
- C++ standard requirements (C++20)
- Compiler flags for warnings and sanitizers
- Dependency declarations (TBB, SFML)
- Executable target definition

**When to Modify:**
- Adding new source files
- Changing C++ standard version
- Adding new dependencies
- Modifying compiler flags

#### `README.md`
**Purpose:** Main project documentation and entry point

**Contents:**
- Project overview and purpose
- Quick start guide
- Feature list
- Dependency installation instructions
- Build and run instructions
- Technical details
- Links to additional documentation

**Audience:** All users (developers, students, reviewers)

#### `.gitignore`
**Purpose:** Specifies files and directories Git should ignore

**Contents:**
- Build artifacts (`.o`, `.a`, `.so`, executables)
- Build directory
- Output files (images, timing data)
- IDE/editor temporary files

**When to Modify:**
- Adding new types of generated files
- Excluding new temporary file patterns

## Source Directory (`src/`)

### `src/main.cpp`
**Purpose:** Main program implementation

**Components:**
1. **Mandelbrot Function**: Computes escape time for a complex number
2. **Color Mapping**: Converts iteration count to RGB color
3. **Main Function**: Orchestrates computation and benchmarking

**Key Sections:**
- Header includes (SFML, TBB, standard library)
- Type definitions (`Complex`)
- Core algorithm implementation
- Parallelization with TBB
- Performance measurement loop
- Image generation and file I/O

**Size:** ~90 lines of code
**Language:** C++20

## Documentation Directory (`docs/`)

### `docs/USAGE.md`
**Purpose:** Comprehensive usage guide

**Contents:**
- Build instructions (Debug/Release)
- Running the program
- Understanding output files
- Modifying parameters
- Performance tips
- Troubleshooting guide
- Advanced usage examples

**Audience:** Users who want to run or modify the program

### `docs/PERFORMANCE.md`
**Purpose:** In-depth performance analysis

**Contents:**
- Parallelization strategy explanation
- Grain size impact analysis
- Performance metrics definitions
- Optimization techniques
- Hardware considerations
- Result interpretation guide
- Benchmarking best practices

**Audience:** Users interested in performance optimization and parallel computing concepts

### `docs/PROJECT_STRUCTURE.md`
**Purpose:** Explains project organization (this file)

**Contents:**
- Directory structure overview
- File descriptions and purposes
- Design decisions
- Maintenance guidelines

**Audience:** Developers and contributors

## Output Directory (`output/`)

**Purpose:** Contains generated visualization images

**Files:**
- `mandelbrot.png`: Main output image (800×800 pixels)

**Characteristics:**
- Automatically generated when program runs
- Not tracked in Git (in `.gitignore`)
- Can be safely deleted (will be regenerated)

**Note:** This directory may not exist in a fresh clone. It will be created automatically when the program runs or can be created manually.

## Results Directory (`results/`)

**Purpose:** Contains performance measurement data

**Files:**
- `grain_time.txt`: Timing data for different grain sizes

**Format:**
```
grain_size seconds
1 0.141317
2 0.112635
...
```

**Characteristics:**
- Plain text, space-separated values
- Automatically generated when program runs
- Not tracked in Git (in `.gitignore`)
- Can be imported into spreadsheet software for analysis

**Note:** This directory may not exist in a fresh clone. It will be created automatically when the program runs or can be created manually.

## Build Directory (`build/`)

**Purpose:** Contains compiled binaries and build artifacts

**Subdirectories:**
- `build/debug/`: Debug build with sanitizers
- `build/release/`: Optimized release build

**Contents:**
- Compiled object files (`.o`)
- Executable binary (`mandelbrot`)
- CMake cache and configuration files
- Dependency information

**Characteristics:**
- Completely generated by CMake
- Not tracked in Git (in `.gitignore`)
- Can be safely deleted and rebuilt
- Typically 10-50 MB in size

## Design Decisions

### Why This Structure?

#### Separation of Source Code (`src/`)
- **Scalability**: Easy to add more source files
- **Organization**: Clear separation from documentation and output
- **Standard Practice**: Follows common C++ project conventions

#### Dedicated Documentation Directory (`docs/`)
- **Discoverability**: All documentation in one place
- **Separation**: Keeps root directory clean
- **Extensibility**: Easy to add more documentation files

#### Separate Output Directories
- **Clarity**: Clear distinction between input and output
- **Gitignore**: Easy to exclude generated files
- **Organization**: Prevents clutter in root directory

#### Root-Level Configuration Files
- **Convention**: Standard practice for build configuration
- **Visibility**: Easy to find and modify
- **Tool Expectations**: Build tools expect configuration at root

### Alternative Structures Considered

#### Flat Structure (All Files in Root)
**Rejected Because:**
- Cluttered root directory
- Difficult to distinguish source from output
- Poor scalability for larger projects

#### Include Directory (`include/`)
**Not Used Because:**
- Single source file doesn't warrant separate headers
- No library component to expose
- Keeps structure simple for educational project

#### Test Directory (`test/`)
**Not Used Because:**
- Primary focus is on learning parallel computing
- Manual verification sufficient for this project
- Can be added later if needed

## Maintenance Guidelines

### Adding New Source Files

1. Place in `src/` directory
2. Update `CMakeLists.txt`:
   ```cmake
   add_executable(mandelbrot src/main.cpp src/new_file.cpp)
   ```

### Adding New Documentation

1. Place in `docs/` directory
2. Use Markdown format (`.md`)
3. Link from main `README.md` if appropriate

### Modifying Build Configuration

1. Edit `CMakeLists.txt`
2. Reconfigure CMake:
   ```shell
   cmake -S . -B build/release
   ```
3. Rebuild project

### Managing Generated Files

- **Never commit** files listed in `.gitignore`
- Output and results directories can be safely deleted
- Regenerate by running the program

## File Naming Conventions

### Source Files
- Format: `lowercase_with_underscores.cpp`
- Example: `main.cpp`, `mandelbrot_utils.cpp`

### Documentation Files
- Format: `UPPERCASE_WITH_UNDERSCORES.md`
- Example: `README.md`, `USAGE.md`, `PERFORMANCE.md`

### Output Files
- Format: `lowercase_with_underscores.ext`
- Example: `mandelbrot.png`, `grain_time.txt`

## Version Control

### Tracked Files
- All source code (`src/`)
- All documentation (`docs/`, `README.md`)
- Build configuration (`CMakeLists.txt`)
- Git configuration (`.gitignore`)

### Ignored Files (Not Tracked)
- Build artifacts (`build/`)
- Generated images (`output/`, `*.png`)
- Performance data (`results/`, `grain_time.txt`)
- IDE/editor files (`.vscode/`, `.idea/`, `*.swp`)

### Rationale
- **Track source**: Essential for rebuilding project
- **Ignore generated**: Can be recreated from source
- **Ignore personal**: IDE settings vary by developer

## Future Expansion

### Potential Additions

#### `include/` Directory
For separating interface (`.h`) from implementation (`.cpp`) if project grows.

#### `test/` Directory
For unit tests and integration tests:
```
test/
├── unit/
│   └── mandelbrot_test.cpp
└── integration/
    └── full_program_test.cpp
```

#### `examples/` Directory
For example configurations or scripts:
```
examples/
├── high_resolution.sh
├── zoom_regions.sh
└── color_schemes.cpp
```

#### `scripts/` Directory
For utility scripts:
```
scripts/
├── benchmark.sh
├── analyze_results.py
└── generate_animation.sh
```

#### `data/` Directory
For input data or configuration files:
```
data/
├── interesting_regions.txt
├── color_palettes.json
└── test_parameters.yml
```

## Best Practices

### For Developers

1. **Keep Source Organized**: All code in `src/`
2. **Document Changes**: Update relevant `.md` files
3. **Test Builds**: Test both Debug and Release modes
4. **Clean Commits**: Don't commit generated files

### For Users

1. **Read Documentation**: Start with `README.md`
2. **Check USAGE.md**: For detailed instructions
3. **Explore Examples**: Try modifying parameters
4. **Clean Builds**: Delete `build/` if issues arise

### For Contributors

1. **Follow Structure**: Maintain existing organization
2. **Update Documentation**: Keep docs in sync with code
3. **Respect .gitignore**: Don't commit ignored files
4. **Consistent Naming**: Follow existing conventions

## Conclusion

This project structure balances simplicity with organization:
- **Simple enough** for a single-file program
- **Organized enough** for clear separation of concerns
- **Extensible enough** for future growth
- **Standard enough** to be familiar to C++ developers

The structure makes it easy to:
- Find relevant files quickly
- Understand the project layout
- Add new components
- Maintain and modify the code
- Collaborate with others

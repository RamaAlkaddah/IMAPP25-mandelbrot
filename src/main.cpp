#include <SFML/Graphics.hpp>
#include <complex>

#include <oneapi/tbb/parallel_for.h>
#include <oneapi/tbb/blocked_range2d.h>
#include <oneapi/tbb/partitioner.h>

#include <chrono>
#include <fstream>
#include <vector>


using Complex = std::complex<double>;

int mandelbrot(Complex const& c)
{
  int i = 0;
  auto z = c;
  for (; i != 256 && std::norm(z) < 4.; ++i) {
    z = z * z + c;
  }
  return i;
}

auto to_color(int k)
{
  return k < 256 ? sf::Color{static_cast<sf::Uint8>(10 * k), 0, 0}
                 : sf::Color::Black;
}

int main()
{
  int const display_width{800};
  int const display_height{800};

  Complex const top_left{-2.2, 1.5};
  Complex const lower_right{0.8, -1.5};
  auto const diff = lower_right - top_left;

  auto const delta_x = diff.real() / display_width;
  auto const delta_y = diff.imag() / display_height;

  sf::Image image;

  // list of grain sizes to test
  std::vector<int> grain_sizes = {1, 2, 4, 8, 16, 32, 64,128,256,512,1024,2048};

  std::ofstream timing_file("grain_time.txt");
  timing_file << "grain_size seconds\n"; // column titles

  for (int grain_size : grain_sizes) {
    image.create(display_width, display_height);


    auto t0 = std::chrono::high_resolution_clock::now();
//parallel_for(range, lambda_function, partitioner);
    oneapi::tbb::parallel_for(
      oneapi::tbb::blocked_range2d<int>(
        0, display_height, grain_size,
        0, display_width,  grain_size
      ),
      [&](const oneapi::tbb::blocked_range2d<int>& r) {


        for (int row = r.rows().begin(); row != r.rows().end(); ++row) {
          for (int column = r.cols().begin(); column != r.cols().end(); ++column) {

            auto k = mandelbrot(
              top_left + Complex{delta_x * column, delta_y * row}
            );

            image.setPixel(column, row, to_color(k));
          }
        }
      },
      oneapi::tbb::simple_partitioner{}
    );

    auto t1 = std::chrono::high_resolution_clock::now();
    double seconds = std::chrono::duration<double>(t1 - t0).count();

    timing_file << grain_size << " " << seconds << "\n";
  }

  // Save the image from the last run (last grain_size)
  image.saveToFile("mandelbrot.png");

  return 0;
}

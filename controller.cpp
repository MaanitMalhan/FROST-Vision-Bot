#include <iostream>
#include <fstream>
#include <string>
#include <unistd.h> // For sleep

int main() {
    const char* pipe_name = "/tmp/vision_pipe"; // Same pipe name as in the Python script

    while (true) {
        // Open the pipe for reading
        std::ifstream pipe(pipe_name);

        if (!pipe.is_open()) {
            std::cerr << "Error: Could not open pipe." << std::endl;
            return 1;
        }

        std::string line;
        while (std::getline(pipe, line)) {
            // Read data from the pipe (each line corresponds to one set of coordinates)
            std::cout << "Received: " << line << std::endl;

            // Optional: Parse the coordinates from the received string
            int x, y;
            if (sscanf(line.c_str(), "%d,%d", &x, &y) == 2) {
                std::cout << "Parsed x: " << x << " y: " << y << std::endl;
            } else {
                std::cout << "Failed to parse coordinates." << std::endl;
            }
        }

        // If the pipe closes (e.g., Python script ends), reopen the pipe
        std::cout << "Writer closed the pipe. Waiting for a new connection..." << std::endl;
        pipe.close();

        // Optional: Add a delay before reopening the pipe to avoid busy-waiting
        sleep(1);
    }

    return 0;
}

#include <iostream>
#include <experimental/filesystem>
#include <fstream>
#include <vector>
#include <string>
#include <cstring>
#include <algorithm>
#include <zip.h>

namespace fs = std::experimental::filesystem;

void list_zip_files(std::vector<std::string> &zip_files) {
    // List all ZIP files in the current directory
    for (const auto &entry : fs::directory_iterator(fs::current_path())) {
        if (entry.path().extension() == ".zip") {
            zip_files.push_back(entry.path().string());
        }
    }
}

void extract_zip_file(const std::string &zip_file, const std::string &extract_to) {
    // Extract a ZIP file to a specific location using libzip
    int err = 0;
    zip *z = zip_open(zip_file.c_str(), 0, &err);
    if (z == nullptr) {
        std::cerr << "Failed to open zip file: " << zip_file << "\n";
        return;
    }

    fs::create_directories(extract_to);
    zip_uint64_t total_entries = static_cast<zip_uint64_t>(zip_get_num_entries(z, 0));
    for (zip_uint64_t i = 0; i < total_entries; i++) {
        const char *name = zip_get_name(z, i, 0);
        if (name == nullptr) {
            continue;
        }
        std::string full_path = extract_to + "/" + name;
        if (name[strlen(name) - 1] == '/') {
            fs::create_directories(full_path);
        } else {
            auto zf = zip_fopen_index(z, i, 0);
            if (zf) {
                std::ofstream output(full_path, std::ios::binary);
                char buffer[8192];
                zip_int64_t bytes_read;
                while ((bytes_read = zip_fread(zf, buffer, sizeof(buffer))) > 0) {
                    output.write(buffer, bytes_read);
                }
                zip_fclose(zf);
            }
        }
        // Print progress
        std::cout << "Extracting " << (i + 1) << "/" << total_entries << ": " << name << "\n";
    }
    zip_close(z);
}

bool is_image_file(const std::string &filename) {
    std::string lower_filename = filename;
    std::transform(lower_filename.begin(), lower_filename.end(), lower_filename.begin(), ::tolower);
    return (lower_filename.find(".jpg", lower_filename.size() - 4) != std::string::npos || lower_filename.find(".jpeg", lower_filename.size() - 5) != std::string::npos ||
            lower_filename.find(".png", lower_filename.size() - 4) != std::string::npos || lower_filename.find(".bmp", lower_filename.size() - 4) != std::string::npos ||
            lower_filename.find(".gif", lower_filename.size() - 4) != std::string::npos || lower_filename.find(".tiff", lower_filename.size() - 5) != std::string::npos);
}

void move_files_to_data_folder(const fs::path &root_dir, const std::string &target_dir = "data") {
    size_t file_count = 0;
    for (const auto &entry : fs::recursive_directory_iterator(root_dir)) {
        if (!fs::is_directory(entry) && is_image_file(entry.path().string())) {
            file_count++;
        }
    }

    size_t processed_files = 0;
    for (const auto &entry : fs::recursive_directory_iterator(root_dir)) {
        if (fs::is_directory(entry)) {
            continue;
        }

        if (is_image_file(entry.path().string())) {
            std::string category_name = entry.path().parent_path().filename().string();
            fs::path target_category_path = fs::path(target_dir) / category_name;
            fs::create_directories(target_category_path);
            fs::path target_path = target_category_path / entry.path().filename();
            fs::rename(entry, target_path);
            processed_files++;
            // Print progress
            std::cout << "Moving file " << processed_files << "/" << file_count << ": " << entry.path().filename().string() << "\n";
        }
    }
}

int main() {
    // Step 1: List ZIP files
    std::vector<std::string> zip_files;
    list_zip_files(zip_files);

    // Step 2: Extract ZIP files
    std::string extract_root = "extracted_files";
    for (const auto &zip_file : zip_files) {
        extract_zip_file(zip_file, extract_root);
    }

    // Step 3: Move files as per the given logic
    move_files_to_data_folder(extract_root);

    // Optionally, clean up the extracted_files folder
    fs::remove_all(extract_root);

    return 0;
}

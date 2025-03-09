<p align="center">
  <img src="docs/images/icon.png" alt="Image Optimizer Logo" width="200"/>
</p>

# Bulk Image Optimizer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/) [![Pillow](https://img.shields.io/badge/Pillow-9.0+-blue.svg)](https://python-pillow.github.io)

A powerful, user-friendly desktop application for bulk image optimization.

## Features

- **Batch Processing**: Optimize multiple images at once by selecting individual files or entire folders
- **Format Support**: Works with JPEG, PNG, GIF, BMP, TIFF, and WebP files
- **Quality Control**: Adjust JPEG quality and PNG compression levels
- **Image Resizing**: Resize images while maintaining aspect ratio
- **Format Conversion**: Convert images between formats
- **User-Friendly Interface**: Clean, intuitive design for efficient workflow

## Screenshot

<p align="center">
  <img src="docs/images/screenshot.jpg" alt="Image Optimizer Screenshot" width="400"/>
</p>

## Installation for Users

### Windows

1. Download the latest release from the [Releases page](https://github.com/barandev/bulk-image-optimizer/releases)
2. Run the app (`BulkImageOptimizer.exe`)
3. Launch the application's executable file

### macOS

`! WIP !`

### Linux

`! WIP !`

## Installation for Developers

### Prerequisites

- Python 3.6 or higher
- Pillow (PIL Fork)

### Installation Steps

1. Clone this repository:

   ```bash
   git clone https://github.com/barandev/bulk-image-optimizer.git
   cd bulk-image-optimizer
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

### Creating an Executable (for Developers)

You can create a standalone executable using PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py

# Optional parameters:
# pyinstaller --onefile --windowed --icon="docs\images\icon.ico" --noconsole --add-binary="docs\images\icon.png;docs\images" --clean main.py
```

The executable will be created in the `dist` directory.

## Usage

1. **Select Images**: Click "Select Images" to choose individual files or "Select Folder" to scan an entire directory
2. **Configure Settings**:
   - Adjust JPEG quality (10-100) **(85 by default)**
   - Set PNG compression level (0-9) **(6 by default)**
   - Enable/disable resizing and set maximum dimensions **(disabled by default)**
   - Choose output format **(original by default)**
   - Set output directory **(creates new folder with the name `optimized` on the source folder by default)**
   - Toggle original filename preservation **(enabled by default)**
3. **Start Optimization**: Click the "START OPTIMIZATION" button
4. **Monitor Progress**: The progress bar and status text will keep you informed

## Customization

The application is designed to be easily customized. At the top of the `main.py` file, you'll find several configuration sections:

- **APP_TITLE and dimensions**: Modify the window title and size
- **COLORS**: Change the color palette
- **FONTS**: Update font families, sizes, and styles
- **PADDING**: Adjust spacing throughout the interface
- **TEXTS**: Modify all text labels and messages (useful for localization)
- **DEFAULTS**: Change default optimization settings
- **FORMATS**: Update supported file formats and extensions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Pillow (PIL Fork)](https://python-pillow.org/) for image processing capabilities
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework

## Roadmap

- [ ] Add advanced optimization algorithms
- [ ] Implement metadata preservation options
- [ ] Add file size preview functionality
- [ ] Add localization support
- [ ] Implement batch rename features

import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
from typing import List
import time

# -----------------------------------------------------------------------------
# CUSTOMIZATION VARIABLES
# -----------------------------------------------------------------------------

# Application title and dimensions
APP_TITLE = "Bulk Image Optimizer"  # The title displayed in the application window
APP_WIDTH = 800  # Initial width of the application window in pixels
APP_HEIGHT = 900  # Initial height of the application window in pixels
APP_MIN_WIDTH = 800  # Minimum allowed width of the application window
APP_MIN_HEIGHT = 600  # Minimum allowed height of the application window

# Pastel Color Palette
COLORS = {
    "bg_primary": "#FFFFFF",  # White background for main UI elements
    "bg_secondary": "#A8BFAC",  # Light sage for secondary elements and accents
    "accent": "#96CCD9",  # Light blue/teal for highlights and important elements
    "accent_hover": "#758C74",  # Darker sage for hover states
    "accent_pressed": "#758C74",  # Same darker sage for pressed states
    "button_bg": "#96CCD9",  # Light blue/teal for regular buttons
    "button_primary": "#D9674E",  # Vibrant terracotta for primary action button
    "text_primary": "#333333",  # Dark gray for primary text
    "text_secondary": "#758C74",  # Darker sage for secondary text
    "border": "#A8BFAC",  # Light sage for borders
    "success": "#A8BFAC",  # Light sage for success indicators
    "warning": "#BF7D56",  # Muted terracotta for warnings
    "error": "#D9674E",  # Vibrant terracotta for errors
    "disabled": "#CCCCCC",  # Light gray for disabled elements
    "progress_track": "#EEEEEE",  # Very light gray for progress bar track
    "list_select": "#96CCD9",  # Light blue/teal for selection background
}

# Font configurations
FONTS = {
    "regular": ("Helvetica", 9),  # Regular font for most UI elements
    "bold": ("Helvetica", 9, "bold"),  # Bold version for emphasis
    "heading": ("Helvetica", 10, "bold"),  # Font for headings and titles
    "button": ("Helvetica", 10, "bold"),  # Font for buttons
    "small": ("Helvetica", 8),  # Smaller font for less important information
}

# UI Padding and spacing
PADDING = {
    "frame": 10,  # Padding for frames
    "widget": 5,  # Standard padding between widgets
    "button_x": 10,  # Horizontal internal padding for buttons
    "button_y": 5,  # Vertical internal padding for buttons
    "list_item": 2,  # Padding for list items
}

# Text labels and messages
TEXTS = {
    # Window and section titles
    "title": "Bulk Image Optimizer",
    "image_selection": "Image Selection",
    "optimization_settings": "Optimization Settings",
    # Buttons
    "select_images": "Select Images",
    "select_folder": "Select Folder",
    "clear_selection": "Clear Selection",
    "browse": "Browse...",
    "start_optimization": "START OPTIMIZATION",
    "cancel": "Cancel",
    # Labels
    "no_files": "No files selected",
    "files_selected": "{} files selected",
    "jpg_quality": "JPEG Quality:",
    "png_compression": "PNG Compression:",
    "resize_images": "Resize Images",
    "max_width": "Max Width:",
    "max_height": "Max Height:",
    "convert_to": "Convert to:",
    "output_dir": "Output Directory:",
    "preserve_names": "Preserve original filenames",
    "ready": "Ready",
    "starting": "Starting optimization...",
    "processing": "Processing {}...",
    "progress": "Processed {}/{} images. Success: {}, Failed: {}",
    "canceling": "Canceling...",
    # Dialog messages
    "no_files_warn": "No Files Selected",
    "no_files_msg": "Please select at least one image to optimize.",
    "dir_error_title": "Error",
    "dir_error_msg": "Could not create output directory: {}",
    "complete_title": "Optimization Complete",
    "complete_msg": "Successfully optimized {} images.\nFailed: {}\n\nImages saved to: {}",
    "failed_title": "Optimization Failed",
    "failed_msg": "Failed to optimize any of the {} images.\nCheck the console for error details.",
    "no_images_title": "No Images Found",
    "no_images_msg": "No image files were found in the selected folder.",
}

# Default values for settings
DEFAULTS = {
    "jpg_quality": 85,  # Default JPEG quality (0-100)
    "png_compression": 6,  # Default PNG compression level (0-9)
    "resize_enabled": False,  # Whether image resizing is enabled by default
    "max_width": "1920",  # Default maximum width for resizing
    "max_height": "1080",  # Default maximum height for resizing
    "convert_format": "original",  # Default conversion format
    "preserve_names": True,  # Whether to preserve original filenames by default
    "output_subfolder": "optimized",  # Default subfolder name for output when not specified
}

# Format options and file types
FORMATS = {
    "convert_options": [
        "original",
        "jpg",
        "png",
        "webp",
    ],  # Supported conversion formats
    "file_extensions": (
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".tiff",
        ".webp",
    ),  # Supported file extensions
    "filetypes": [
        ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.webp"),
        ("JPEG", "*.jpg *.jpeg"),
        ("PNG", "*.png"),
        ("All files", "*.*"),
    ],
}


class ImageOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.minsize(APP_MIN_WIDTH, APP_MIN_HEIGHT)

        # Application state
        self.selected_files = []
        self.output_directory = ""
        self.processing = False
        self.optimization_thread = None

        # Create the main UI
        self.create_ui()

        # Apply the theme
        self.set_theme()

    def set_theme(self):
        """Apply the pastel theme to all UI elements"""
        style = ttk.Style()

        # Configure the base styles for different widget types
        style.configure("TFrame", background=COLORS["bg_primary"])
        style.configure("TButton", foreground=COLORS["text_primary"])
        style.map(
            "TButton",
            background=[
                ("active", COLORS["accent_hover"]),
                ("!disabled", COLORS["button_bg"]),
            ],
            foreground=[("disabled", COLORS["disabled"])],
        )

        # Configure action button style
        style.configure(
            "Action.TButton",
            background=COLORS["button_primary"],
            foreground=COLORS["bg_primary"],
        )
        style.map(
            "Action.TButton",
            background=[
                ("active", COLORS["accent_hover"]),
                ("!disabled", COLORS["button_primary"]),
            ],
            foreground=[("pressed", COLORS["bg_primary"])],
        )

        # Configure text-based widgets
        style.configure(
            "TLabel",
            background=COLORS["bg_primary"],
            foreground=COLORS["text_primary"],
            font=FONTS["regular"],
        )

        style.configure(
            "TCheckbutton",
            background=COLORS["bg_primary"],
            foreground=COLORS["text_primary"],
            font=FONTS["regular"],
        )

        # Configure progress bar
        style.configure(
            "Horizontal.TProgressbar",
            background=COLORS["accent"],
            troughcolor=COLORS["progress_track"],
        )

        # Configure frames and labels
        style.configure(
            "TLabelframe",
            background=COLORS["bg_primary"],
            foreground=COLORS["text_primary"],
        )

        style.configure(
            "TLabelframe.Label",
            foreground=COLORS["text_primary"],
            background=COLORS["bg_primary"],
            font=FONTS["heading"],
        )

        # Configure dropdown combobox
        style.configure(
            "TCombobox",
            foreground=COLORS["text_primary"],
            fieldbackground=COLORS["bg_primary"],
        )

        # Set the root background color
        self.root.configure(bg=COLORS["bg_primary"])

        # Update Optimize button if it exists
        if hasattr(self, "optimize_btn"):
            self.optimize_btn.configure(
                bg=COLORS["button_primary"],
                fg=COLORS["bg_primary"],
                activebackground=COLORS["accent_hover"],
                activeforeground=COLORS["bg_primary"],
            )

        # Update Listbox colors if it exists
        if hasattr(self, "files_list"):
            self.files_list.configure(
                bg=COLORS["bg_primary"],
                fg=COLORS["text_primary"],
                selectbackground=COLORS["list_select"],
                selectforeground=COLORS["bg_primary"],
                highlightbackground=COLORS["border"],
                highlightcolor=COLORS["accent"],
            )

    def create_ui(self):
        """Create the user interface elements"""
        # Configure custom styles first
        style = ttk.Style()
        style.configure(
            "Action.TButton",
            font=FONTS["button"],
        )

        main_frame = ttk.Frame(self.root, padding=PADDING["frame"])
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header with logo or title (optional)
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, PADDING["widget"]))

        header_label = ttk.Label(
            header_frame,
            text=TEXTS["title"],
            font=("Helvetica", 16, "bold"),
            foreground=COLORS["button_primary"],
        )
        header_label.pack(side=tk.LEFT, padx=PADDING["widget"])

        # File selection area
        file_frame = ttk.LabelFrame(
            main_frame, text=TEXTS["image_selection"], padding=PADDING["frame"]
        )
        file_frame.pack(
            fill=tk.BOTH, expand=True, padx=PADDING["widget"], pady=PADDING["widget"]
        )

        button_frame = ttk.Frame(file_frame)
        button_frame.pack(fill=tk.X, padx=PADDING["widget"], pady=PADDING["widget"])

        select_files_btn = ttk.Button(
            button_frame, text=TEXTS["select_images"], command=self.select_files
        )
        select_files_btn.pack(
            side=tk.LEFT, padx=PADDING["widget"], pady=PADDING["widget"]
        )

        select_folder_btn = ttk.Button(
            button_frame, text=TEXTS["select_folder"], command=self.select_folder
        )
        select_folder_btn.pack(
            side=tk.LEFT, padx=PADDING["widget"], pady=PADDING["widget"]
        )

        clear_btn = ttk.Button(
            button_frame, text=TEXTS["clear_selection"], command=self.clear_selection
        )
        clear_btn.pack(side=tk.LEFT, padx=PADDING["widget"], pady=PADDING["widget"])

        # Files list
        list_frame = ttk.Frame(file_frame)
        list_frame.pack(
            fill=tk.BOTH, expand=True, padx=PADDING["widget"], pady=PADDING["widget"]
        )

        self.files_list = tk.Listbox(
            list_frame,
            selectmode=tk.EXTENDED,
            height=10,
            font=FONTS["regular"],
            highlightthickness=1,
            relief=tk.SOLID,
            borderwidth=1,
        )
        scrollbar = ttk.Scrollbar(
            list_frame, orient="vertical", command=self.files_list.yview
        )
        self.files_list.configure(yscrollcommand=scrollbar.set)

        self.files_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # File count label
        self.file_count_var = tk.StringVar(value=TEXTS["no_files"])
        file_count_label = ttk.Label(file_frame, textvariable=self.file_count_var)
        file_count_label.pack(
            anchor=tk.W, padx=PADDING["widget"], pady=PADDING["widget"]
        )

        # Settings frame
        settings_frame = ttk.LabelFrame(
            main_frame, text=TEXTS["optimization_settings"], padding=PADDING["frame"]
        )
        settings_frame.pack(
            fill=tk.BOTH, padx=PADDING["widget"], pady=PADDING["widget"]
        )

        # Quality settings
        quality_frame = ttk.Frame(settings_frame)
        quality_frame.pack(fill=tk.X, padx=PADDING["widget"], pady=PADDING["widget"])

        ttk.Label(quality_frame, text=TEXTS["jpg_quality"]).pack(
            side=tk.LEFT, padx=PADDING["widget"]
        )
        self.jpg_quality_var = tk.IntVar(value=DEFAULTS["jpg_quality"])
        jpg_quality_scale = ttk.Scale(
            quality_frame,
            from_=10,
            to=100,
            variable=self.jpg_quality_var,
            orient=tk.HORIZONTAL,
            length=200,
            command=lambda val: self.jpg_quality_var.set(int(float(val))),
        )
        jpg_quality_scale.pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=PADDING["widget"]
        )
        ttk.Label(quality_frame, textvariable=self.jpg_quality_var).pack(
            side=tk.LEFT, padx=PADDING["widget"]
        )

        # PNG compression
        png_frame = ttk.Frame(settings_frame)
        png_frame.pack(fill=tk.X, padx=PADDING["widget"], pady=PADDING["widget"])

        ttk.Label(png_frame, text=TEXTS["png_compression"]).pack(
            side=tk.LEFT, padx=PADDING["widget"]
        )
        self.png_compression_var = tk.IntVar(value=DEFAULTS["png_compression"])
        png_compression_scale = ttk.Scale(
            png_frame,
            from_=0,
            to=9,
            variable=self.png_compression_var,
            orient=tk.HORIZONTAL,
            length=200,
            command=lambda val: self.png_compression_var.set(int(float(val))),
        )
        png_compression_scale.pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=PADDING["widget"]
        )
        ttk.Label(png_frame, textvariable=self.png_compression_var).pack(
            side=tk.LEFT, padx=PADDING["widget"]
        )

        # Resize options
        resize_frame = ttk.Frame(settings_frame)
        resize_frame.pack(fill=tk.X, padx=PADDING["widget"], pady=PADDING["widget"])

        self.resize_enabled = tk.BooleanVar(value=DEFAULTS["resize_enabled"])
        resize_check = ttk.Checkbutton(
            resize_frame, text=TEXTS["resize_images"], variable=self.resize_enabled
        )
        resize_check.pack(side=tk.LEFT, padx=PADDING["widget"])

        ttk.Label(resize_frame, text=TEXTS["max_width"]).pack(
            side=tk.LEFT, padx=PADDING["widget"]
        )
        self.max_width_var = tk.StringVar(value=DEFAULTS["max_width"])
        max_width_entry = ttk.Entry(
            resize_frame, textvariable=self.max_width_var, width=6
        )
        max_width_entry.pack(side=tk.LEFT, padx=PADDING["widget"])

        ttk.Label(resize_frame, text=TEXTS["max_height"]).pack(
            side=tk.LEFT, padx=PADDING["widget"]
        )
        self.max_height_var = tk.StringVar(value=DEFAULTS["max_height"])
        max_height_entry = ttk.Entry(
            resize_frame, textvariable=self.max_height_var, width=6
        )
        max_height_entry.pack(side=tk.LEFT, padx=PADDING["widget"])

        # File format options
        format_frame = ttk.Frame(settings_frame)
        format_frame.pack(fill=tk.X, padx=PADDING["widget"], pady=PADDING["widget"])

        ttk.Label(format_frame, text=TEXTS["convert_to"]).pack(
            side=tk.LEFT, padx=PADDING["widget"]
        )
        self.convert_format_var = tk.StringVar(value=DEFAULTS["convert_format"])
        format_dropdown = ttk.Combobox(
            format_frame,
            textvariable=self.convert_format_var,
            values=FORMATS["convert_options"],
            width=10,
            state="readonly",
        )
        format_dropdown.pack(side=tk.LEFT, padx=PADDING["widget"])

        # Output directory
        output_frame = ttk.Frame(settings_frame)
        output_frame.pack(fill=tk.X, padx=PADDING["widget"], pady=PADDING["widget"])

        ttk.Label(output_frame, text=TEXTS["output_dir"]).pack(
            side=tk.LEFT, padx=PADDING["widget"]
        )
        self.output_dir_var = tk.StringVar(value="")
        output_dir_entry = ttk.Entry(
            output_frame, textvariable=self.output_dir_var, width=40
        )
        output_dir_entry.pack(
            side=tk.LEFT, padx=PADDING["widget"], fill=tk.X, expand=True
        )

        output_dir_btn = ttk.Button(
            output_frame, text=TEXTS["browse"], command=self.select_output_dir
        )
        output_dir_btn.pack(side=tk.LEFT, padx=PADDING["widget"])

        # Preserve original filenames option
        preserve_frame = ttk.Frame(settings_frame)
        preserve_frame.pack(fill=tk.X, padx=PADDING["widget"], pady=PADDING["widget"])

        self.preserve_names_var = tk.BooleanVar(value=DEFAULTS["preserve_names"])
        preserve_check = ttk.Checkbutton(
            preserve_frame,
            text=TEXTS["preserve_names"],
            variable=self.preserve_names_var,
        )
        preserve_check.pack(side=tk.LEFT, padx=PADDING["widget"])

        # Progress section
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, padx=PADDING["widget"], pady=PADDING["widget"])

        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            orient=tk.HORIZONTAL,
            length=100,
            mode="determinate",
            variable=self.progress_var,
        )
        self.progress_bar.pack(
            fill=tk.X, padx=PADDING["widget"], pady=PADDING["widget"]
        )

        self.status_var = tk.StringVar(value=TEXTS["ready"])
        status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        status_label.pack(fill=tk.X, padx=PADDING["widget"])

        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=PADDING["widget"], pady=10)

        # Create main action button with custom styling
        self.optimize_btn = tk.Button(
            button_frame,
            text=TEXTS["start_optimization"],
            command=self.start_optimization,
            font=FONTS["button"],
            padx=PADDING["button_x"],
            pady=PADDING["button_y"],
            relief=tk.RAISED,
            borderwidth=2,
        )
        self.optimize_btn.pack(
            side=tk.RIGHT,
            padx=PADDING["widget"],
            pady=PADDING["widget"],
        )

        self.cancel_btn = ttk.Button(
            button_frame,
            text=TEXTS["cancel"],
            command=self.cancel_optimization,
            state=tk.DISABLED,
        )
        self.cancel_btn.pack(side=tk.RIGHT, padx=PADDING["widget"])

    def select_files(self):
        """Open file dialog to select multiple image files"""
        files = filedialog.askopenfilenames(
            title=TEXTS["select_images"], filetypes=FORMATS["filetypes"]
        )

        if files:
            self.selected_files = list(files)
            self.update_files_list()

    def select_folder(self):
        """Open folder dialog to select a directory of images"""
        folder = filedialog.askdirectory(title=TEXTS["select_folder"])

        if folder:
            new_files = []

            for root, _, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(FORMATS["file_extensions"]):
                        full_path = os.path.join(root, file)
                        new_files.append(full_path)

            if new_files:
                self.selected_files.extend(new_files)
                self.update_files_list()
            else:
                messagebox.showinfo(TEXTS["no_images_title"], TEXTS["no_images_msg"])

    def update_files_list(self):
        """Update the listbox with selected files"""
        self.files_list.delete(0, tk.END)

        for file in self.selected_files:
            self.files_list.insert(tk.END, os.path.basename(file))

        self.file_count_var.set(
            TEXTS["files_selected"].format(len(self.selected_files))
        )

    def clear_selection(self):
        """Clear the selected files list"""
        self.selected_files = []
        self.files_list.delete(0, tk.END)
        self.file_count_var.set(TEXTS["no_files"])

    def select_output_dir(self):
        """Select directory to save optimized images"""
        directory = filedialog.askdirectory(title=TEXTS["output_dir"])

        if directory:
            self.output_directory = directory
            self.output_dir_var.set(directory)

    def start_optimization(self):
        """Begin the optimization process"""
        if not self.selected_files:
            messagebox.showwarning(TEXTS["no_files_warn"], TEXTS["no_files_msg"])
            return

        # Get output directory
        output_dir = self.output_dir_var.get()
        if not output_dir:
            # If no output directory is specified, create an "optimized" subfolder in the same location as the first image
            first_image_dir = os.path.dirname(self.selected_files[0])
            output_dir = os.path.join(first_image_dir, DEFAULTS["output_subfolder"])
            self.output_dir_var.set(output_dir)

        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError as e:
                messagebox.showerror(
                    TEXTS["dir_error_title"], TEXTS["dir_error_msg"].format(e)
                )
                return

        # Get optimization settings
        settings = {
            "jpg_quality": self.jpg_quality_var.get(),
            "png_compression": self.png_compression_var.get(),
            "resize": self.resize_enabled.get(),
            "max_width": (
                int(self.max_width_var.get())
                if self.max_width_var.get().isdigit()
                else int(DEFAULTS["max_width"])
            ),
            "max_height": (
                int(self.max_height_var.get())
                if self.max_height_var.get().isdigit()
                else int(DEFAULTS["max_height"])
            ),
            "convert_format": self.convert_format_var.get(),
            "preserve_names": self.preserve_names_var.get(),
            "output_dir": output_dir,
        }

        # Update UI for processing state
        self.processing = True
        self.optimize_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)
        self.status_var.set(TEXTS["starting"])

        # Start optimization in a separate thread
        self.optimization_thread = threading.Thread(
            target=self.process_images,
            args=(self.selected_files, settings),
            daemon=True,
        )
        self.optimization_thread.start()

    def process_images(self, files: List[str], settings: dict):
        """Process all selected images with the given settings"""
        total_files = len(files)
        processed = 0
        successful = 0
        failed = 0

        for i, file_path in enumerate(files):
            if not self.processing:  # Check if canceled
                break

            try:
                self.status_var.set(
                    TEXTS["processing"].format(os.path.basename(file_path))
                )

                # Process the image
                success = self.optimize_image(file_path, settings)

                if success:
                    successful += 1
                else:
                    failed += 1

            except Exception as e:
                failed += 1
                print(f"Error processing {file_path}: {e}")

            processed += 1
            progress = (processed / total_files) * 100
            self.progress_var.set(progress)

            # Update the status every few images or at the end
            if i % 5 == 0 or i == total_files - 1:
                self.status_var.set(
                    TEXTS["progress"].format(processed, total_files, successful, failed)
                )

        # Reset UI after completion
        self.root.after(0, self.finish_optimization, successful, failed)

    def optimize_image(self, file_path: str, settings: dict) -> bool:
        """Optimize a single image according to settings"""
        try:
            # Open image
            img = Image.open(file_path)

            # Handle resize if enabled
            if settings["resize"]:
                original_width, original_height = img.size
                max_width = settings["max_width"]
                max_height = settings["max_height"]

                # Only resize if the image is larger than the max dimensions
                if original_width > max_width or original_height > max_height:
                    # Calculate new dimensions while maintaining aspect ratio
                    width_ratio = max_width / original_width
                    height_ratio = max_height / original_height
                    ratio = min(width_ratio, height_ratio)

                    new_width = int(original_width * ratio)
                    new_height = int(original_height * ratio)

                    img = img.resize((new_width, new_height), Image.LANCZOS)

            # Determine output format
            original_format = img.format
            output_format = original_format

            if settings["convert_format"] != "original":
                output_format = settings["convert_format"].upper()
            elif output_format is None:
                # If format cannot be determined, default to PNG
                output_format = "PNG"

            # Determine output filename
            if settings["preserve_names"]:
                base_name = os.path.basename(file_path)
                file_name, original_ext = os.path.splitext(base_name)

                # Adjust extension if format is changing
                if settings["convert_format"] != "original":
                    new_ext = f".{settings['convert_format'].lower()}"
                else:
                    new_ext = original_ext

                output_filename = f"{file_name}{new_ext}"
            else:
                # Generate a new name with timestamp
                timestamp = int(time.time())
                file_name = os.path.basename(file_path)
                name_without_ext, _ = os.path.splitext(file_name)

                if settings["convert_format"] != "original":
                    ext = f".{settings['convert_format'].lower()}"
                else:
                    _, ext = os.path.splitext(file_path)

                output_filename = f"{name_without_ext}_optimized_{timestamp}{ext}"

            output_path = os.path.join(settings["output_dir"], output_filename)

            # Save with appropriate settings
            if output_format == "JPEG" or output_format == "JPG":
                # Convert to RGB if saving as JPEG (no alpha channel support)
                if img.mode in ("RGBA", "LA", "P"):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(
                        img, mask=img.split()[3] if img.mode == "RGBA" else None
                    )
                    img = background

                img.save(
                    output_path,
                    format="JPEG",
                    quality=settings["jpg_quality"],
                    optimize=True,
                )

            elif output_format == "PNG":
                img.save(
                    output_path,
                    format="PNG",
                    optimize=True,
                    compress_level=settings["png_compression"],
                )

            elif output_format == "WEBP":
                # WebP quality goes from 0-100 like JPEG
                img.save(
                    output_path,
                    format="WEBP",
                    quality=settings["jpg_quality"],
                    method=6,
                )

            else:
                # For other formats, just save with default settings
                img.save(output_path, format=output_format)

            return True

        except Exception as e:
            print(f"Error optimizing {file_path}: {e}")
            return False

    def finish_optimization(self, successful: int, failed: int):
        """Reset UI state after optimization completes"""
        self.processing = False
        self.optimize_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)

        if successful > 0:
            messagebox.showinfo(
                TEXTS["complete_title"],
                TEXTS["complete_msg"].format(
                    successful, failed, self.output_dir_var.get()
                ),
            )
        else:
            messagebox.showerror(
                TEXTS["failed_title"], TEXTS["failed_msg"].format(successful + failed)
            )

    def cancel_optimization(self):
        """Cancel the ongoing optimization process"""
        if self.processing:
            self.processing = False
            self.status_var.set(TEXTS["canceling"])
            # The thread will terminate on its next iteration


def main():
    root = tk.Tk()

    try:
        # Handle both development and bundled environments
        import sys, os
        import tempfile

        if getattr(sys, "frozen", False):
            # Running as bundled app (exe)
            base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))

            # For Windows: .ico file for taskbar/window icon
            if os.name == "nt":
                ico_path = os.path.join(base_path, "icon.ico")
                root.iconbitmap(default=ico_path)

            # Cross-platform method as backup
            png_path = os.path.join(base_path, "icon.png")
            icon = tk.PhotoImage(file=png_path)
            root.iconphoto(True, icon)
        else:
            # Running as script
            if os.name == "nt":
                root.iconbitmap("docs/images/icon.ico")
            icon = tk.PhotoImage(file="docs/images/icon.png")
            root.iconphoto(True, icon)

    except Exception as e:
        print(f"Could not set icon: {e}")

    app = ImageOptimizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

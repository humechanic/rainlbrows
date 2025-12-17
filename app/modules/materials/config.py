"""
Configuration for intensive materials files
Add file paths here that should be sent to users who have paid
"""
import os

# Base directory for materials (relative to project root or absolute path)
MATERIALS_BASE_DIR = "materials"

# List of material files to send
# Format: [{"type": "document|photo|video", "path": "path/to/file", "caption": "Optional caption"}]
MATERIALS_FILES = [
    # Example:
    # {"type": "document", "path": "materials/guide.pdf", "caption": "Руководство по продажам"},
    # {"type": "photo", "path": "materials/cheatsheet.jpg", "caption": "Шпаргалка"},
]

def get_materials_files():
    """Get list of material files with full paths"""
    files = []
    for material in MATERIALS_FILES:
        file_path = material["path"]
        # If relative path, make it absolute
        if not os.path.isabs(file_path):
            # Try relative to project root
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            file_path = os.path.join(project_root, file_path)
        
        if os.path.exists(file_path):
            files.append({
                "type": material["type"],
                "path": file_path,
                "caption": material.get("caption", "")
            })
    return files




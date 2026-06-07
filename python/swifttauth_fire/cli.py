import os
import shutil
import sys

def main():
    # Find the documentation template packed with your library
    package_dir = os.path.dirname(os.path.abspath(__file__))
    source_doc = os.path.join(package_dir, "AGENT-doc.md")
    target_doc = os.path.join(os.getcwd(), "AGENT-doc.md")

    if os.path.exists(target_doc):
        print("AGENT-doc.md already exists in the current directory.")
        sys.exit(0)

    if not os.path.exists(source_doc):
        print(f"Error: Documentation template not found at {source_doc}")
        sys.exit(1)

    try:
        shutil.copy(source_doc, target_doc)
        print("Created AGENT-doc.md in the current directory.")
    except Exception as e:
        print(f"Error copying documentation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

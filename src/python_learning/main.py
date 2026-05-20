def main():
    print("Hello from python-learning!")

#  Any file with this block is runnable
#
# _name__ is "__main__" only when the file is run directly.
# If another module does import main, __name__ becomes "main" and the block is skipped. This lets the same file be both:
# - An importable module (from python_learning.main import main)
# - A runnable script (python -m python_learning.main)
# Without the guard, importing the file would also execute its main logic — usually not what you want.
if __name__ == "__main__":
    main()

"""
index.py
========
Entry point for the Fraud Detection System.
"""

from ui.dashboard_complete import main
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    main()

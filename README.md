# Genetic Engineering Toolbox (基因工程工具箱)

## Introduction

The Genetic Engineering Toolbox is a desktop application designed to facilitate various genetic engineering tasks. This toolbox currently includes the following functionalities:
1. **Restriction Sites Finder (酶切位点搜寻)**: Finds restriction enzyme cut sites in a given DNA sequence.
2. **DNA to Protein (DNA 转蛋白质)**: Translates a DNA sequence into its corresponding protein sequences in three reading frames and identifies possible protein sequences.
3. **DNA Comparison (DNA 比较)**: (Feature to be implemented)
4. **Protein Comparison (蛋白质比较)**: (Feature to be implemented)

## Features

### Restriction Sites Finder

- **Input**: DNA sequence
- **Output**: Restriction enzymes that cut the DNA sequence, along with their cut positions. Also displays enzymes that do not cut the sequence.

### DNA to Protein

- **Input**: DNA sequence
- **Output**: Translated protein sequences for three reading frames and possible protein sequences extracted from these frames.
- **Filter**: A filter to display only those protein sequences with DNA lengths greater than a specified value.

## How to Build the App using PyInstaller

### Prerequisites

- Python 3.x
- PyQt5
- Biopython
- PyInstaller

### Installation

1. **Install Python 3.x**: Ensure you have Python 3.x installed on your system. You can download it from the official [Python website](https://www.python.org/).

2. **Install Required Packages**:
   Open a terminal or command prompt and run the following commands to install the required packages:

   ```
   pip install pyqt5 biopython pyinstaller
   ```
### Building the Application

1. **Navigate to the Project Directory: Ensure you are in the root directory of the project where your Python scripts are located.
    ```
    cd <repository_directory>
    ```

2. **Build the Application: Use PyInstaller to build the application. Run the following command:
    ```
    pyinstaller --name="基因工程工 具箱（汉化版）" --windowed --onefile App.py
    ```

3. **Run the Executable: Navigate to the dist directory and run the executable file GeneticEngineeringToolbox.exe (on Windows) to launch the application.

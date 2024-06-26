# DataGraphVisualization

Welcome to the repository of Team 17, dedicated to the development of our project within the "Software Patterns and Components" course. Here, we will share code, documentation, and project development information.

## Team Members:
1. **Dušica Trbović (SV42/2021)**
2. **Vesna Vasić (SV78/2021)**
3. **Ana Poparić (SV74/2021)**

## Project Description:
DataGraphVisualization is a web application designed to visualize data through interactive graphs. The application supports three different views:
- **Main View**: The primary graph visualization.
- **Bird View**: A high-level overview of the graph.
- **Tree View**: A hierarchical representation of the graph.

We offer two types of visualizers:
- **Simple Visualizer**: Basic graph visualization.
- **Block Visualizer**: Advanced, block-based graph visualization.

The application supports two data sources:
- **Football**: Data related to football.
- **Hotel**: Data related to hotels.

## Installation Guide:
To set up the project on your local machine, follow these steps:

1. **Create a virtual environment:**
    ```sh
    py -m venv .env
    ```
2. **Activate the virtual environment:**
    - On Windows:
        ```sh
        .env\Scripts\activate.bat
        ```
3. **Navigate to the main folder and install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```
4. **Run the setup script:**
    ```sh
    script.bat
    ```

After running the setup script, a link will be provided to access the web application in your browser.

## Project Structure:
The project structure is organized as follows:
- `main`: Main branch containing the stable version of the project.
- `develop`: Branch for developing new features.

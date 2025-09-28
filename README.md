<img src="icon.ico" alt="TrueConnect Logo" width="100">

# TrueConnect

TrueConnect is a simple yet powerful Instagram analytics tool that helps you manage your connections effectively. By analyzing your exported Instagram data (JSON format), it identifies **users who don’t follow you back** and those **you don’t follow back**, giving you full control over your social graph.

## 🚀 Features

- **Follower Analysis**: Upload your Instagram JSON export and instantly see who isn’t following you back.  
- **Following Analysis**: Find out whom you’re not following back.  
- **Clean Reports**: Generates clear, easy-to-read lists.  
- **Data Privacy**: All analysis happens locally on your machine, ensuring your data stays safe.  
- **Export Options**: Save results as PDF for future use.  


## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/developer-pranav/TrueConnect.git
   cd TrueConnect
   ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the project:
    ```bash
    python3 main.py
    ```

5. Upload your Instagram JSON file when prompted.

## 🧰 Tech Stack

- **Language**: Python  
- **Data Handling**: Pandas (for JSON parsing and analysis)  
- **Report Generation**: FPDF (for PDF export), CSV (native Python/Pandas)  
- **File Input**: Works with Instagram’s exported JSON data  
- **Environment**: Virtualenv for project isolation  

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

## 🤝 Contributing

Want to contribute? Follow these steps:

1. Fork the repository.  
2. Create a new branch (`git checkout -b feature/YourFeature`).  
3. Commit your changes (`git commit -am 'Add some feature'`).  
4. Push to the branch (`git push origin feature/YourFeature`).  
5. Create a new Pull Request.  

We appreciate your contributions!

## 📩 Contact

For any questions or suggestions, please open an issue or contact [Developer Pranav](mailto:developer.pranav3306@gmail.com).
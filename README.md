# Amazon Price Monitoring Project

This project is a web scraping application that allows users to search for products on Amazon and retrieve detailed information about them, including the product title, price, and image URL. The application is built using Python, BeautifulSoup for web scraping, and Streamlit for the user interface.

## Features

- **Search Products:** Users can input a product name to search for related products on Amazon.
- **Retrieve Product Information:** The application fetches product links and extracts detailed information for each product.
- **Display Results:** The results are displayed in a user-friendly interface using Streamlit.
- **Error Handling:** The application includes error handling and debugging messages to facilitate development.
- **Data Storage:** The obtained data is saved in a structured format for further analysis.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/RfigueroaS/Price-monitoring
    cd Price-monitoring
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501`.

3. Enter the product name you want to search for in the input field and press Enter.

4. The application will display the search results with detailed information about each product.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
# Market Research Dashboard

A powerful tool for conducting market research using Google Places API. This dashboard helps businesses analyze market potential, competition, and opportunities in specific locations.

## Features

- 🔍 Search for businesses within a specified radius
- 📊 Interactive visualizations of market data
- 💰 Price level analysis
- ⭐ Rating and review analysis
- 🏪 Business status tracking
- 📸 Photo availability filtering
- 📥 Export data to CSV
- 🎯 Multiple place type analysis

## Demo

Watch this quick demo to see the dashboard in action:

[demo.webm](https://github.com/user-attachments/assets/472dd537-e5b4-49fa-b877-03b83c2a0322)

## Prerequisites

- Python 3.8 or higher
- Google Maps API key with Places API enabled
- Google Cloud Platform account (billing required)

## Google Maps API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Places API for your project
4. Create credentials (API key)
5. Set up billing for your project
   - Note: Billing is required unless you have an educational account with free credits
   - Google provides $200 free credit monthly for new accounts
   - Educational accounts may have additional free credits

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/market-research-dashboard.git
cd market-research-dashboard
```

2. Create and activate a virtual environment:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install --use-pep517 -r requirements.txt
```

4. Create a `.env` file in the project root and add your Google Maps API key:
```bash
GOOGLE_MAPS_API_KEY=your_api_key_here
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run streamlit_app.py
```

2. The dashboard will open in your default web browser. Use the sidebar to:
   - Enter the latitude and longitude of your target location
   - Set the search radius in kilometers
   - Select one or more place types to analyze
   - Choose whether to filter for places with photos
   - Set the maximum number of results to fetch

3. Click "Analyze Market" to start the analysis

### Example Usage

Let's say you want to analyze the market for a new restaurant in Chennai, India:

1. Enter the coordinates:
   - Latitude: 13.0196719
   - Longitude: 80.2688418
   - Radius: 2.0 km

2. Select place types:
   - restaurant
   - cafe
   - bar

3. Set other parameters:
   - Maximum Results: 40
   - Only show results with photo: Checked

4. Click "Analyze Market" to see:
   - Market saturation
   - Price level distribution
   - Rating analysis
   - Business status distribution
   - Detailed results table

## Data Export

The dashboard allows you to export all analyzed data to CSV format for further analysis in spreadsheet software.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool uses the Google Places API, which requires billing setup on Google Cloud Platform. Users are responsible for managing their own API usage and associated costs.

## Support

If you encounter any issues or have questions, please open an issue in the GitHub repository. 

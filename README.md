```
                     ______                _ __   _____                                
                    / ____/___ ___  ____ _(_) /  / ___/______________ _____  ___  _____
                   / __/ / __ `__ \/ __ `/ / /   \__ \/ ___/ ___/ __ `/ __ \/ _ \/ ___/
                  / /___/ / / / / / /_/ / / /   ___/ / /__/ /  / /_/ / /_/ /  __/ /    
                 /_____/_/ /_/ /_/\__,_/_/_/   /____/\___/_/   \__,_/ .___/\___/_/     
                                                                    /_/                  
                                    [ Email Processing Made Simple ]

================================================================================

📧 Description
-------------
A command-line tool for fetching, processing, and summarizing emails using Gmail API
and local AI model integration. Efficiently processes emails and generates detailed
JSON reports with summaries.

🚀 Features
----------
- Gmail API Integration
- Local AI Model Summarization
- URL Extraction & Processing
- JSON Report Generation
- Progress Visualization
- Cross-Platform Support

⚙️ Installation
-------------
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Email-scraper.git
   cd Email-scraper
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Gmail API credentials:
   - Visit Google Cloud Console
   - Enable Gmail API
   - Download credentials.json
   - Place in project root directory
     

📁 Project Structure
-----------------

Email-scraper/
├── scr/
│ ├── main.py # Main application entry
│ ├── authemail.py # Gmail authentication
│ ├── scrape_emails.py # Email fetching logic
│ ├── process_emails.py # Email processing
│ ├── local_model.py # AI model integration
│ ├── report_generator.py # JSON report creation
│ └── ascii_art.py # Visual elements
├── requirements.txt
└── README.md

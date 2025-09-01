# Air-quality-predictor
A Streamlit web app that predicts air quality and shows safety insights

🌍 Air Quality Predictor

📂 Project Structure

Air-quality-predictor/
│── app.py                 # Web app code  
│── main.py                # Script to test predictions  
│── air_quality_model.pkl  # Trained ML model  
│── data/                  # Folder containing dataset  
│    └── air_quality.csv  
│── requirements.txt       # Python dependencies  
│── README.md              # Project documentation  

⚙️ Installation

Clone the repository

git clone https://github.com/Dipanjan01-max/Air-quality-predictor.git
cd Air-quality-predictor


Create a virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate    # for Linux/Mac  
venv\Scripts\activate       # for Windows  


Install dependencies

pip install -r requirements.txt

▶️ Usage
Run the web app
streamlit run app.py

Run the script directly
python main.py

📊 Dataset

The dataset contains various environmental indicators (e.g., temperature, humidity, gas concentrations) used for predicting air quality.
Here is the dataset:
https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india?utm_

🧠 Model

Trained using Scikit-learn (or specify the algorithm you used like RandomForest, XGBoost, etc.).

Saved as a .pkl file for easy reusability.

📈 Future Improvements

Add support for real-time AQI data via APIs

Deploy model on Heroku / Streamlit Cloud / Hugging Face Spaces

Enhance accuracy with deep learning models

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

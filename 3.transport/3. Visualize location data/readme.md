# Adafruit Web App

This web app fetches data from Adafruit IO and displays it using a secure serverless backend via Netlify.

## 🔗 Live App

[View Deployed App](https://your-app-name.netlify.app)

## ⚙️ Technologies Used

- HTML/CSS/JavaScript
- Adafruit IO
- Netlify Functions
- GitHub

## 🔒 Security

API key is stored as an environment variable on Netlify and accessed via a serverless function.

## 📁 Project Structure
my-adafruit-app/
├── index.html
├── style.css
├── script.js
└── netlify/functions/fetch-data.js


## 🚀 Setup Instructions

1. Clone repo
2. Add `.env` with your Adafruit IO key
3. Run locally with `netlify dev`
4. Deploy with `netlify deploy`

# Farm Functions on Cloudflare Workers

This project implements the cloud-side logic for the **Farm** IoT scenario from the *IoT for Beginners* curriculum, specifically for **Assignment 5: Migrate application to the cloud**.  
Instead of using Azure Functions, this version uses **Cloudflare Workers** to expose HTTP endpoints that control the relay on a smart farm system.

## 📦 Project Structure

```
farm-functions-cf/
├── public/              # Public folder (not used in this setup)
├── src/
│   ├── index.js         # Main Cloudflare Worker script
├── wrangler.jsonc       # Wrangler config file
├── package.json         # NPM config file
└── README.md            # Project documentation
```

## 🔧 Prerequisites

Make sure you have the following installed:

- [Node.js](https://nodejs.org/) (v18+ recommended)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/install-and-upgrade/)  
  Install using:
  ```bash
  npm install -g wrangler
  ```

- A [Cloudflare account](https://dash.cloudflare.com/)
- A registered **workers.dev** subdomain

## 🚀 Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/HoTrungQuan2004/IoT-and-Smart-devices.git
   cd IoT-and-Smart-devices/2.Farm/5-migrate-application-to-the-cloud/Farm/farm/farm-functions-cf
   ```

2. **Install Dependencies**

   ```bash
   npm install
   ```

3. **Configure Wrangler**

   Update the `wrangler.jsonc` file with your Cloudflare `account_id` and desired worker `name`.  
   You can find your account ID on the Cloudflare dashboard under **Workers & Pages > Overview**.

4. **Deploy to Cloudflare**

   ```bash
   npx wrangler deploy
   ```

   You will be prompted to register a `workers.dev` subdomain if you haven’t already.  
   After deployment, you’ll get URLs like:

   - `https://<your-subdomain>.workers.dev/relay_on`
   - `https://<your-subdomain>.workers.dev/relay_off`

## 🌐 Endpoints

| Method | URL                                 | Description           |
|--------|-------------------------------------|-----------------------|
| GET    | `/relay_on`                         | Triggers relay ON     |
| GET    | `/relay_off`                        | Triggers relay OFF    |

## 📖 How It Works

These endpoints are designed to simulate the relay control functionality of a smart farm. In a real deployment:

- **IoT devices** (like ESP32 or Raspberry Pi) send requests to the above endpoints.
- **Cloudflare Workers** handle the request and respond appropriately.
- **The relay state is toggled** based on the triggered URL (`/relay_on` or `/relay_off`).

This replicates the functionality of the Azure Functions used in the original curriculum.

## ✅ To Do

- Add request authentication (optional)
- Expand to support additional endpoints (e.g., temperature logging)

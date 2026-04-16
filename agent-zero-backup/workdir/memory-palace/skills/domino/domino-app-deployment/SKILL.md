---
name: "domino-app-deployment"
description: "Deploy web applications to Domino Data Lab — React/Vite, Streamlit, Dash, Flask, Gradio, FastAPI, Shiny. Covers app.sh configuration, proxy architecture, CI/CD with GitHub Actions, and troubleshooting."
version: "1.0.0"
author: "Domino Data Lab / Tolu"
tags: ["domino", "mlops", "app-deployment", "react", "vite", "streamlit", "flask", "gradio", "dash", "fastapi", "cicd", "github-actions"]
trigger_patterns:
  - "domino app deployment"
  - "deploy app to domino"
  - "domino react vite"
  - "domino streamlit dash flask"
  - "domino app.sh"
  - "domino reverse proxy"
  - "domino app cicd"
  - "domino app troubleshooting"
  - "deploy web app domino"
---

# Domino App Deployment Skill

Deploy web applications to Domino Data Lab with expertise in React (Vite), Streamlit, Dash, Flask, Gradio, FastAPI, and Shiny behind Domino's reverse proxy. Covers app.sh configuration, port binding, base path handling, CI/CD, and troubleshooting.

## Activation

Activate this skill when users want to:
- Deploy any web application to Domino
- Configure React/Vite apps for Domino's proxy
- Set up Streamlit, Dash, Flask, Gradio, FastAPI, or Shiny apps
- Configure app.sh entry point scripts
- Set up CI/CD pipelines for Domino apps
- Troubleshoot broken routing, 404s, or connection issues

---

## Domino App Architecture

Domino apps run in containers behind a reverse proxy that:
1. Authenticates users via Domino's auth system
2. Strips the URL prefix before forwarding to your app
3. Routes traffic to your app container
4. Handles infrastructure provisioning, routing, and resource management

```
User Request: https://domino.company.com/jsmith/myproject/app/dashboard/settings

Domino Proxy Layer:
├── Authenticates user
├── Strips prefix: /jsmith/myproject/app/dashboard/
├── Forwards to container port 8888
└── Injects headers: X-Domino-User, X-Domino-Project

Your App Container:
└── Receives request at port 8888, path: /settings
```

**Note:** Port selection is flexible; port 8888 is no longer required. You can use any port your application prefers.

### Critical Configuration Points

1. **Host Binding**: Bind to `0.0.0.0` (not localhost) so Domino can reach your app
2. **Relative Base Path**: Use `base: './'` in Vite config for React apps
3. **app.sh**: Entry point script (launch file) that Domino executes

### Domino Environment Variables

| Variable | Description |
|----------|-------------|
| `DOMINO_PROJECT_NAME` | Current project name |
| `DOMINO_PROJECT_OWNER` | Project owner username |
| `DOMINO_RUN_ID` | Current run identifier |
| `DOMINO_STARTING_USERNAME` | User who started the app |

---

## React with Vite

### Vite Configuration (vite.config.js)

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],

  // CRITICAL: Use relative base path for Domino proxy
  base: './',

  server: {
    host: '0.0.0.0',
    port: 8888,
    strictPort: true,
  },

  preview: {
    host: '0.0.0.0',
    port: 8888,
    strictPort: true,
  },

  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  }
})
```

| Option | Value | Purpose |
|--------|-------|---------|
| `base` | `'./'` | Makes all asset paths relative |
| `server.host` | `'0.0.0.0'` | Binds to all interfaces |
| `server.port` | `8888` | Domino's expected port |
| `strictPort` | `true` | Fails if port unavailable |

### Why React Apps Break Without Proper Configuration

1. React builds assume assets are served from root `/`
2. Browser requests `/static/js/main.js` → 404 error
3. Should request `/owner/project/app/name/static/js/main.js`

**Solution**: Use relative paths with `base: './'` in Vite config.

### Production app.sh

```bash
#!/bin/bash
set -e

echo "=== Domino Vite React App ==="
echo "Project: $DOMINO_PROJECT_NAME"
echo "Owner: $DOMINO_PROJECT_OWNER"

cd /mnt/code
npm ci
npm run build
npx serve -s dist -l 8888 --no-clipboard
```

The `-s` flag enables single-page application mode — serves `index.html` for all routes that don't match a file (required for React Router).

### Connecting to Model API Endpoints

```javascript
// src/api/modelApi.js
const MODEL_API_URL = import.meta.env.VITE_MODEL_API_URL;
const MODEL_API_TOKEN = import.meta.env.VITE_MODEL_API_TOKEN;

export async function predict(inputData) {
  const response = await fetch(MODEL_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${MODEL_API_TOKEN}`,
    },
    body: JSON.stringify({ data: inputData }),
  });
  if (!response.ok) throw new Error(`API error: ${response.status}`);
  return response.json();
}
```

### Client-Side Routing (React Router)

**Option 1: BrowserRouter with basename**
```javascript
import { BrowserRouter } from 'react-router-dom';

const basename = window.location.pathname.replace(/\/[^/]*$/, '');

ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter basename={basename}>
    <App />
  </BrowserRouter>
);
```

**Option 2: HashRouter (simpler)**
```javascript
import { HashRouter } from 'react-router-dom';

ReactDOM.createRoot(document.getElementById('root')).render(
  <HashRouter>
    <App />
  </HashRouter>
);
```
URLs will be: `https://domino.company.com/owner/project/app/name/#/dashboard`

### Development in Domino Workspace

```bash
#!/bin/bash
cd /mnt/code
npm install
npm run dev -- --host 0.0.0.0 --port 8888
```

Preview URL: `https://<domino-url>/<owner>/<project>/notebookSession/<run-id>/proxy/8888/`

### Complete React Project Structure

```
my-react-app/
├── src/
│   ├── api/
│   │   └── modelApi.js
│   ├── components/
│   ├── App.jsx
│   └── main.jsx
├── public/
├── vite.config.js
├── package.json
├── app.sh
├── .env.example
└── .gitignore
```

---

## Streamlit

### app.sh
```bash
#!/bin/bash
set -e

streamlit run app.py \
    --server.port 8888 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false
```

### With Custom Configuration
```bash
#!/bin/bash
set -e

mkdir -p ~/.streamlit
cat > ~/.streamlit/config.toml << 'EOF'
[server]
port = 8888
address = "0.0.0.0"
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1976d2"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f5f5f5"
textColor = "#212121"
EOF

streamlit run app.py
```

### Example Streamlit App

```python
import streamlit as st
import os
import requests

st.set_page_config(page_title="ML Dashboard", page_icon="📊", layout="wide")
st.title("ML Model Dashboard")

with st.expander("Environment Info"):
    st.write(f"Project: {os.environ.get('DOMINO_PROJECT_NAME', 'N/A')}")
    st.write(f"User: {os.environ.get('DOMINO_STARTING_USERNAME', 'N/A')}")

feature1 = st.number_input("Feature 1", value=0.0)
feature2 = st.number_input("Feature 2", value=0.0)

if st.button("Predict"):
    model_url = os.environ.get('MODEL_API_URL')
    model_token = os.environ.get('MODEL_API_TOKEN')
    if model_url and model_token:
        response = requests.post(model_url,
            headers={'Authorization': f'Bearer {model_token}', 'Content-Type': 'application/json'},
            json={'data': {'feature1': feature1, 'feature2': feature2}})
        st.json(response.json())
    else:
        st.error("Model API not configured")
```

**requirements.txt:** `streamlit>=1.28.0`, `requests>=2.28.0`, `pandas>=2.0.0`

---

## Dash (Plotly)

### app.sh
```bash
#!/bin/bash
set -e
python app.py
```

### Example Dash App

```python
import os
import dash
from dash import html, dcc, callback, Input, Output
import requests

app = dash.Dash(__name__, routes_pathname_prefix='/')

app.layout = html.Div([
    html.H1("ML Model Dashboard"),
    html.Div([
        html.Label("Feature 1:"), dcc.Input(id='feature1', type='number', value=0),
        html.Label("Feature 2:"), dcc.Input(id='feature2', type='number', value=0),
        html.Button('Predict', id='predict-btn', n_clicks=0),
    ]),
    html.Div(id='prediction-output'),
    html.Div([
        html.P(f"Project: {os.environ.get('DOMINO_PROJECT_NAME', 'N/A')}"),
        html.P(f"User: {os.environ.get('DOMINO_STARTING_USERNAME', 'N/A')}"),
    ], style={'marginTop': '20px', 'color': 'gray'})
])

@callback(Output('prediction-output', 'children'),
    Input('predict-btn', 'n_clicks'), Input('feature1', 'value'), Input('feature2', 'value'),
    prevent_initial_call=True)
def predict(n_clicks, feature1, feature2):
    model_url = os.environ.get('MODEL_API_URL')
    model_token = os.environ.get('MODEL_API_TOKEN')
    if not model_url or not model_token:
        return html.P("Model API not configured", style={'color': 'red'})
    try:
        response = requests.post(model_url,
            headers={'Authorization': f'Bearer {model_token}', 'Content-Type': 'application/json'},
            json={'data': {'feature1': feature1, 'feature2': feature2}})
        return html.Pre(str(response.json()))
    except Exception as e:
        return html.P(f"Error: {str(e)}", style={'color': 'red'})

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8888, debug=False)  # CRITICAL: Bind to 0.0.0.0:8888
```

**requirements.txt:** `dash>=2.14.0`, `requests>=2.28.0`, `pandas>=2.0.0`, `plotly>=5.18.0`

---

## Flask

### app.sh
```bash
#!/bin/bash
set -e
python app.py
```

### Example Flask App

```python
import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
        project=os.environ.get('DOMINO_PROJECT_NAME', 'N/A'),
        user=os.environ.get('DOMINO_STARTING_USERNAME', 'N/A'))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    model_url = os.environ.get('MODEL_API_URL')
    model_token = os.environ.get('MODEL_API_TOKEN')
    if not model_url or not model_token:
        return jsonify({'error': 'Model API not configured'}), 500
    try:
        response = requests.post(model_url,
            headers={'Authorization': f'Bearer {model_token}', 'Content-Type': 'application/json'},
            json={'data': data})
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=False)  # CRITICAL: Bind to 0.0.0.0:8888
```

### Flask with Gunicorn (Production)
```bash
#!/bin/bash
set -e
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:8888 --workers 4 --timeout 120
```

**requirements.txt:** `flask>=3.0.0`, `gunicorn>=21.0.0`, `requests>=2.28.0`

---

## Gradio

### app.sh
```bash
#!/bin/bash
set -e
python app.py
```

### Example Gradio App

```python
import os
import gradio as gr
import requests

def predict(feature1, feature2):
    model_url = os.environ.get('MODEL_API_URL')
    model_token = os.environ.get('MODEL_API_TOKEN')
    if not model_url or not model_token:
        return "Model API not configured"
    try:
        response = requests.post(model_url,
            headers={'Authorization': f'Bearer {model_token}', 'Content-Type': 'application/json'},
            json={'data': {'feature1': feature1, 'feature2': feature2}})
        return str(response.json())
    except Exception as e:
        return f"Error: {str(e)}"

demo = gr.Interface(
    fn=predict,
    inputs=[gr.Number(label="Feature 1"), gr.Number(label="Feature 2")],
    outputs=gr.Textbox(label="Prediction"),
    title="ML Model Interface",
    description=f"Project: {os.environ.get('DOMINO_PROJECT_NAME', 'N/A')}"
)

if __name__ == '__main__':
    demo.launch(server_name='0.0.0.0', server_port=8888, share=False)  # CRITICAL: Bind to 0.0.0.0:8888
```

**requirements.txt:** `gradio>=4.0.0`, `requests>=2.28.0`

---

## Panel (HoloViz)

### app.sh
```bash
#!/bin/bash
set -e
panel serve app.py --address 0.0.0.0 --port 8888 --allow-websocket-origin="*"
```

### Example Panel App

```python
import os
import panel as pn
import requests

pn.extension()

feature1_input = pn.widgets.FloatInput(name='Feature 1', value=0)
feature2_input = pn.widgets.FloatInput(name='Feature 2', value=0)
predict_button = pn.widgets.Button(name='Predict', button_type='primary')
output = pn.pane.Markdown("Click Predict to get results")

def predict(event):
    model_url = os.environ.get('MODEL_API_URL')
    model_token = os.environ.get('MODEL_API_TOKEN')
    if not model_url or not model_token:
        output.object = "**Error:** Model API not configured"
        return
    try:
        response = requests.post(model_url,
            headers={'Authorization': f'Bearer {model_token}', 'Content-Type': 'application/json'},
            json={'data': {'feature1': feature1_input.value, 'feature2': feature2_input.value}})
        output.object = f"**Result:** {response.json()}"
    except Exception as e:
        output.object = f"**Error:** {str(e)}"

predict_button.on_click(predict)

layout = pn.Column("# ML Model Dashboard",
    f"Project: {os.environ.get('DOMINO_PROJECT_NAME', 'N/A')}",
    feature1_input, feature2_input, predict_button, output)

layout.servable()
```

---

## FastAPI

### app.sh
```bash
#!/bin/bash
set -e
uvicorn app:app --host 0.0.0.0 --port 8888
```

### Example FastAPI App

```python
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import httpx

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return f"""<html><body>
    <h1>ML Dashboard</h1>
    <p>Project: {os.environ.get('DOMINO_PROJECT_NAME', 'N/A')}</p>
    <p>User: {os.environ.get('DOMINO_STARTING_USERNAME', 'N/A')}
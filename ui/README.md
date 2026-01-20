# UI

Scope: Unified user interface.

Constraints:
- No direct DB access.
- All data access via core-services APIs.
- No direct network calls outside /transport.

## Local development

```bash
npm install
npm run dev
```

Open `http://localhost:5173` to view the dashboard.

### Transport integration

Set the transport base URL to proxy core-services APIs:

```bash
export VITE_TRANSPORT_BASE_URL="http://localhost:8081"
```

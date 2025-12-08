# Chrome DevTools MCP Usage Guide

Collected from twenim project for Occam5 integration.

## Core Pattern

```
1. Open/select page
2. Take snapshot for UI state
3. Manipulate elements (click, fill)
4. Evaluate JavaScript for internal state
5. Check console/network logs
```

## MCP Tool Reference

### Page Navigation

```javascript
// List all open pages
list_pages()

// Select page by index
select_page({ pageIdx: 0 })

// Open new page
new_page({ url: 'http://localhost:9001' })

// Navigate current page
navigate_page({ type: 'url', url: '...' })
navigate_page({ type: 'reload', ignoreCache: true })
```

### UI State Inspection

```javascript
// Accessibility tree snapshot (returns uid, text, state)
take_snapshot()

// Screenshot
take_screenshot({ fullPage: true })
```

### Element Manipulation

```javascript
// Click element by uid
click({ uid: '73_159' })

// Fill input field
fill({ uid: '73_108', value: 'test@email.com' })

// Keyboard input
press_key({ key: 'Enter' })
press_key({ key: 'Control+Shift+R' })
```

### JavaScript Evaluation

```javascript
// Access internal state
evaluate_script({
  function: `() => {
    return {
      cookie: document.cookie,
      localStorage: localStorage.getItem('key'),
      dom: document.body.innerText.includes('text')
    };
  }`
})

// Call internal functions
evaluate_script({
  function: `() => {
    someService.doAction();
    return 'done';
  }`
})

// Async operations
evaluate_script({
  function: `async () => {
    await new Promise(r => setTimeout(r, 1000));
    return document.body.innerText.includes('loaded');
  }`
})
```

### Debugging Tools

```javascript
// Console messages
list_console_messages({ types: ['error', 'warn'] })
get_console_message({ msgid: 123 })

// Network requests
list_network_requests({ resourceTypes: ['fetch', 'xhr'] })
get_network_request({ reqid: 456 })
```

## CDP (Chrome DevTools Protocol) Direct Access

twenim uses CDP via WebSocket for programmatic control:

```python
import json
from websocket import create_connection

# Get browser WebSocket URL
CDP_HOST = "localhost"
CDP_PORT = 9222

# Get pages
url = f"http://{CDP_HOST}:{CDP_PORT}/json"
# Returns list of pages with id, url, webSocketDebuggerUrl

# Connect to page
ws_url = page["webSocketDebuggerUrl"]
ws = create_connection(ws_url, timeout=10)

# Execute script
msg = {
    "id": 1,
    "method": "Runtime.evaluate",
    "params": {
        "expression": "document.title",
        "returnByValue": True
    }
}
ws.send(json.dumps(msg))
response = json.loads(ws.recv())
```

### Starting Chrome with Remote Debugging

```python
subprocess.Popen([
    "google-chrome",
    "--remote-debugging-port=9222",
    "--remote-allow-origins=*",
    "--no-first-run",
    "--no-default-browser-check",
    "--user-data-dir=~/.chrome-mcp",
    "http://localhost:9001",
], env={"DISPLAY": ":100"})
```

## Common Test Patterns

### Login Flow

```javascript
// 1. Navigate
navigate_page({ url: '/signIn' })

// 2. Fill form
fill({ uid: 'email_input', value: 'test@example.com' })
fill({ uid: 'password_input', value: 'password123' })

// 3. Submit
click({ uid: 'submit_button' })

// 4. Verify
wait_for({ text: 'Welcome' })
```

### Data Extraction

```javascript
// Scroll + extract
evaluate_script({
  function: `() => {
    window.scrollTo(0, 3000);
    const items = document.querySelectorAll('[data-item]');
    return Array.from(items).map(el => ({
      title: el.textContent.trim(),
      url: el.querySelector('a')?.href
    }));
  }`
})
```

### State Manipulation (Testing)

```javascript
// Set cookies/localStorage
evaluate_script({
  function: `() => {
    document.cookie = 'testMode=true; path=/';
    localStorage.setItem('feature_flag', 'enabled');
    return 'done';
  }`
})

// Reload to apply
navigate_page({ type: 'reload', ignoreCache: true })
```

## Occam5 Implementation Notes

### MCP Integration Pattern

Occam5 should use the chrome-devtools MCP server directly. Key tools:
- `mcp__chrome-devtools__navigate_page`
- `mcp__chrome-devtools__take_snapshot`
- `mcp__chrome-devtools__click`
- `mcp__chrome-devtools__fill`
- `mcp__chrome-devtools__evaluate_script`
- `mcp__chrome-devtools__list_console_messages`

### Caveats

1. **Cookie vs JWT**: Cookie changes apply immediately, but JWT-embedded values require re-login
2. **Session sharing**: Tabs share cookies; use incognito for isolated tests
3. **Async waits**: Use `wait_for` or in-script delays for dynamic content
4. **UID volatility**: Snapshot UIDs can change; re-take snapshot after navigation

---
*Extracted from twenim for Occam5 migration - Cycle 63*

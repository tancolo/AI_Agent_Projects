# MapleWay - AI Agent Guide

This repository contains the **MapleWay Browser Extension**, a tool for tracking Alberta Advantage Immigration Program (AAIP) data.

## 1. Project Overview & Environment

- **Type**: Chrome Browser Extension (Manifest V3)
- **Language**: Vanilla JavaScript (ES6+), HTML5, CSS3
- **Root Directory**: `D:\Dev-Env\Antigravity_Projects\mapleway\codebase\VanillaJS`
- **Package Manager**: None (Pure Vanilla JS project)

**Note**: Do not introduce build tools (Webpack, Vite) or frameworks (React, Vue) unless explicitly requested. Maintain the lightweight, vanilla nature of the project.

## 2. Development & Build

Since this is a vanilla project, there is no build step.

### Running the Extension
1.  Open Chrome/Edge.
2.  Navigate to `chrome://extensions/`.
3.  Enable **Developer mode**.
4.  Click **Load unpacked**.
5.  Select the `codebase/VanillaJS` directory.

### "Building"
- Just save the files.
- Reload the extension in `chrome://extensions/` by clicking the refresh icon on the card.
- Refresh the target web page (e.g., https://www.alberta.ca/aaip-processing-information) to inject the new content scripts.

## 3. Testing & Verification

**There are no automated tests.** Agents must perform manual verification or create temporary test scripts if complex logic is added.

### Manual Testing Protocol
1.  **Reload**: Always reload the extension after edits.
2.  **Navigate**: Go to the target URL (AAIP processing info).
3.  **Interact**: Open the popup, select options, and click buttons.
4.  **Console**: Check the "Inspect views: service worker" (if applicable) or right-click the popup > Inspect to see the console for errors. Check the web page console for content script errors.

### Single Feature Verification
To verify a specific function (e.g., `calculateTotalInvitations`), you can:
1.  Create a temporary test file (e.g., `test.js`) and run it with `node` if it's pure logic.
2.  Or use the browser console context of the extension to call the function.

## 4. Code Style & Conventions

Follow the existing patterns found in `popup/popup.js` and `scripts/content.js`.

### JavaScript
- **Indentation**: 4 spaces.
- **Semicolons**: **ALWAYS** use semicolons.
- **Quotes**: Single quotes `'` preferred. Use backticks \` for template literals.
- **Variables**: `const` for constants, `let` for reassignable variables. Avoid `var`.
- **Async/Await**: Preferred over `.then()` chains for clarity.
- **Error Handling**: Use `try/catch` blocks for async operations, especially message passing.

### Documentation
- Use **JSDoc** comments for functions.
  ```javascript
  /**
   * Calculates the total number of invitations.
   * @param {Array} data - The array of draw data.
   * @returns {number} The total count.
   */
  function calculateTotal(data) { ... }
  ```

### CSS
- **Structure**: Vanilla CSS.
- **Naming**: Kebab-case for classes (e.g., `.total-row`, `.hidden`).
- **Formatting**: 4 spaces or 2 spaces (match file context).

## 5. Directory Structure

- `codebase/VanillaJS/`
    - `manifest.json`: Configuration V3.
    - `popup/`: UI logic (`popup.html`, `popup.css`, `popup.js`).
    - `scripts/`: Background/Content scripts (`content.js`).
    - `icons/`: Extension assets.

## 6. Agent Rules (Cursor/Copilot)

- **No "Magic" Fixes**: Do not suppress errors with `// @ts-ignore` or similar. Fix the root cause.
- **Console Logs**: Use `console.log` for debugging but remove them or switch to `console.debug` before "committing" (finalizing) the task, unless necessary for user feedback.
- **Manifest V3**: Ensure all chrome API calls are compatible with Manifest V3 (e.g., `chrome.action` instead of `chrome.browserAction`, Service Workers instead of background pages).

## 7. Common Tasks

### Adding a new UI element
1.  Edit `popup/popup.html` to add the element.
2.  Edit `popup/popup.css` for styling.
3.  Edit `popup/popup.js` to handle logic/events.

### Modifying Scraper Logic
1.  Edit `scripts/content.js`.
2.  **CRITICAL**: You must reload the extension AND refresh the web page for content script changes to take effect.

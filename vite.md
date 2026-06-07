# My Dashboard — a Vite + React learning project

A personal dashboard built step by step, for people who know HTML but are new to React and Vite. Each step of the build introduces exactly one new concept.

## What we're building

A live personal dashboard with:

- Stat cards showing key numbers (revenue, users, orders)
- A line chart showing trends over time
- Data loaded from an API
- Everything updates without a page reload

## The 5-step learning journey

### Step 1 — Project setup
Run Vite, understand every file it creates, strip out the starter noise. You'll learn what `main.jsx` does, how Vite's hot reload works, and how JSX relates to HTML.

### Step 2 — Your first component
Build a reusable `StatCard` component. The big idea: instead of copy-pasting the same `<div>` three times, you write it once and use it like a custom HTML tag — `<StatCard label="Revenue" value="$4,200" />`. This is what props are.

### Step 3 — Making it interactive
Add a button that updates a number live with no page reload. This is `useState` — React's way of remembering data that can change. You'll see exactly why React re-renders the UI automatically when state changes.

### Step 4 — Loading real data
Fetch numbers from an API when the dashboard loads. This is `useEffect` — React's way of saying "run this code once, after the page appears." You'll also handle loading states so the UI doesn't flash blank content.

### Step 5 — Adding a chart
Install Recharts and drop a line graph into the dashboard. One `npm install`, one import, a few JSX tags — and you have an animated chart driven by your real data.

## Concepts covered

| Concept | What it maps to in HTML/JS |
|---|---|
| Components | Like making your own HTML tags |
| Props | Like HTML attributes (`class`, `href`, etc.) |
| `useState` | Like a variable that automatically refreshes the page when it changes |
| `useEffect` | Like `window.onload`, but more precise |
| `npm install` | Like adding a `<script>` tag, but managed |

## Tech stack

- **Vite** — the build tool and dev server (replaces manually writing `<script>` tags)
- **React** — the UI library
- **Recharts** — charting library built for React

## Getting started

```bash
npm create vite@latest my-dashboard -- --template react
cd my-dashboard
npm install
npm run dev
```

Then open `http://localhost:5173`.

## Project structure (after all 5 steps)

```
src/
├── components/
│   ├── StatCard.jsx     # reusable stat card (Step 2)
│   └── Chart.jsx        # line chart wrapper (Step 5)
├── App.jsx              # root component, wires everything together
└── main.jsx             # entry point — don't touch this
```

## Prerequisites

- Node.js installed (run `node -v` to check — you need v18 or higher)
- Basic HTML and CSS knowledge
- No prior React experience needed

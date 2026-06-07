# SwifttAuth-Fire

Exclusive sign-in with Google for simple, lightning-fast authentication scaffolding. Perfect for hackathons and rapid prototyping!

Say goodbye to the headaches of configuring Firebase Auth popups vs. redirects. This library gives you everything you need in **5 lines of code** on the frontend, and simple decorators/dependencies on the backend.

## Project Structure

This repository is split into two packages to support full-stack scaffolding:

1. **`js/`** (NPM Package): The frontend wrapper. Supports React, Next.js, Vite, and Vanilla JS.
2. **`python/`** (PIP Package): The backend verification library. Supports Django and FastAPI.

## Documentation

- **Frontend Setup (JS/TS):** See [js/AGENT-doc.md](./js/AGENT-doc.md) for installation, environment variables, and usage.
- **Backend Setup (Python):** See [python/AGENT-doc.md](./python/AGENT-doc.md) for critical Service Account JSON setup, Django, and FastAPI usage.

## Publishing (For Later)

When you're ready to publish this to `npm` and `pip`:

### Publishing to NPM
```bash
cd js
npm publish --access public
```

### Publishing to PyPI
```bash
cd python
python -m pip install build twine
python -m build
twine upload dist/*
```

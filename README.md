# Operaton Documentation

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## 🚀 Quick Start

### Installation

```bash
npm install
```

### Local Development

```bash
npm run start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### Build

```bash
npm run build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## 🧪 Testing & Validation

### Check Broken References

```bash
# Quick check for broken asset references
npm run check:refs

# Verbose mode (shows all references being checked)
npm run check:refs:verbose

# Full test suite (checks references + builds)
npm test
```

The broken references checker scans all markdown files for:
- ✅ Broken image links
- ✅ Missing assets (PNG, SVG, BPMN, etc.)
- ✅ Invalid file paths
- 📊 Generates detailed report: `broken-asset-references.md`

**Exit codes:**
- `0` - All references valid ✅
- `1` - Broken references found ❌

## 📁 Project Structure

```
operaton-documentation/
├── docs/                      # Documentation content
│   ├── assets/               # Versioned assets (images, diagrams)
│   │   ├── documentation/
│   │   ├── get-started/
│   │   └── security/
│   ├── documentation/        # Main documentation
│   ├── get-started/          # Getting started guides
│   └── security/             # Security documentation
├── static/                   # Static assets (not versioned)
│   └── img/                  # Theme assets (logo, favicon, etc.)
├── src/                      # React components & plugins
│   ├── components/           # Custom components (e.g., BpmnViewer)
│   ├── plugins/              # Docusaurus plugins
│   └── theme/                # Theme customizations
├── scripts/                  # Utility scripts
│   └── check-broken-references.js
└── docusaurus.config.ts      # Docusaurus configuration
```

## 📝 Documentation Guidelines

### Adding Images

**For documentation images** (versioned with docs):
```markdown
![Description](../assets/documentation/section/image.png)
```

**For images with specific sizing** (use JSX):
```jsx
<img 
  src={require('../assets/documentation/section/image.png').default} 
  width={150}
  alt="Description"
/>
```

**For theme assets** (non-versioned):
```markdown
![Logo](/img/operaton-logo.svg)
```

### Asset Organization

- **Documentation assets**: `docs/assets/` - Versioned with documentation
- **Theme assets**: `static/img/` - Site-wide assets (logo, favicon, social cards)
- **BPMN files**: Keep alongside markdown files for BPMN viewer integration

### BPMN Diagrams

Include interactive BPMN diagrams in documentation:

```markdown
<BpmnViewer diagramPath="./bpmn/my-process.bpmn" />
```

The BPMN viewer component automatically renders interactive diagrams from `.bpmn` files.

## 🔄 Versioning

Create a new documentation version:

```bash
npm run docusaurus docs:version 1.1.0
```

**Note:** Docusaurus versioning includes:
- ✅ All markdown content in `docs/`
- ✅ All assets in `docs/assets/` (images, diagrams)
- ✅ Sidebar configuration
- ❌ Static assets in `static/img/` (shared across versions)

## 🛠️ Maintenance

### Update Dependencies

```bash
npm update
```

This command updates the dependencies from `package.json`.

### Clear Cache

```bash
npm run clear
```

Clears Docusaurus cache. Use when experiencing build issues.

### Verify Documentation Quality

Before committing changes:

```bash
# 1. Check for broken references
npm run check:refs

# 2. Test build
npm run build

# 3. Run full test suite
npm test
```

## 🤝 Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Run `npm test` to verify
4. Commit with descriptive messages
5. Create a pull request

### Commit Message Format

```
feat: add new feature
fix: correct broken link
docs: update installation guide
chore: update dependencies
```

## 📚 Additional Resources

- [Docusaurus Documentation](https://docusaurus.io/)
- [Markdown Guide](https://www.markdownguide.org/)
- [BPMN 2.0 Specification](https://www.omg.org/spec/BPMN/2.0/)

---

**Status:** Documentation in active development 🚧
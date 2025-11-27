# Broken Asset References Report

**Generated:** 2025-11-27 10:22:47

## Summary

- Markdown files scanned: 413
- Total asset references: 541
- Working references: 536
- **Broken references: 4**

## Broken References by File

### documentation\user-guide\process-engine\variables.md

**1 broken reference:**

- **Line 21:** `./img/variables-3.png`
  - Type: image
  - Tried to resolve to: `C:\Users\mail\Development\documentation\docs\documentation\user-guide\process-engine\img\variables-3.png`
  - Full reference: `![Example img](./img/variables-3.png)`

### documentation\webapps\cockpit\extend\plugins.md

**2 broken references:**

- **Line 503:** `./../img/plugin-points/plugin-point-case-definition-diagram-overlay.png`
  - Type: image
  - Tried to resolve to: `C:\Users\mail\Development\documentation\docs\documentation\webapps\cockpit\img\plugin-points\plugin-point-case-definition-diagram-overlay.png`
  - Full reference: `![Example img](./../img/plugin-points/plugin-point-case-definition-diagram-overl...`

- **Line 550:** `./../img/plugin-points/plugin-point-case-instance-diagram-overlay.png`
  - Type: image
  - Tried to resolve to: `C:\Users\mail\Development\documentation\docs\documentation\webapps\cockpit\img\plugin-points\plugin-point-case-instance-diagram-overlay.png`
  - Full reference: `![Example img](./../img/plugin-points/plugin-point-case-instance-diagram-overlay...`

### get-started\quick-start\user-task.md

**1 broken reference:**

- **Line 101:** `./img/start-form-generic.png`
  - Type: image
  - Tried to resolve to: `C:\Users\mail\Development\documentation\docs\get-started\quick-start\img\start-form-generic.png`
  - Full reference: `![Example image](./img/start-form-generic.png)`

## Quick Fix Guide

For each broken reference, you can:

1. **Find the missing asset:** Search for it in your project or recreate it
2. **Fix the path:** Update the markdown to point to the correct location
3. **Remove the reference:** If the asset is no longer needed

## Missing Assets List

- **plugin-point-case-definition-diagram-overlay.png** - Referenced in 1 file
  - documentation\webapps\cockpit\extend\plugins.md
- **plugin-point-case-instance-diagram-overlay.png** - Referenced in 1 file
  - documentation\webapps\cockpit\extend\plugins.md
- **start-form-generic.png** - Referenced in 1 file
  - get-started\quick-start\user-task.md
- **variables-3.png** - Referenced in 1 file
  - documentation\user-guide\process-engine\variables.md

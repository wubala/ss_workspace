## [ERR-20260419-001] freeform_ui_automation_menu_access

**Logged**: 2026-04-19T11:33:00+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
Automating Freeform via AppleScript menu item names failed when trying to click the Chinese-labeled File > 新建板 entry.

### Error
```
System Events error: cannot get menu item "新建板" of menu 1 of menu bar item "文件" of menu bar 1 of application process "Freeform". (-1728)
```

### Context
Attempted direct menu-item click in Freeform on macOS. App was frontmost, but menu hierarchy was not exposed as expected.

### Suggested Fix
Prefer keyboard shortcuts and UI tree inspection for Freeform automation instead of assuming localized menu item names are directly addressable.

### Metadata
- Reproducible: unknown
- Related Files: scripts/
- See Also: none

---

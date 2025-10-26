# WCAG 2.2 Level AA Quick Checklist

Reference: https://w3.org/WAI/WCAG22 (accessed 2025-10-25)

## New in WCAG 2.2 (9 criteria)

### Level A
- 2.4.11 Focus Not Obscured (Minimum)
- 2.5.7 Dragging Movements
- 2.5.8 Target Size (Minimum) - 24x24 CSS pixels

### Level AA
- 2.4.12 Focus Not Obscured (Enhanced)
- 2.4.13 Focus Appearance
- 3.2.6 Consistent Help
- 3.3.7 Redundant Entry
- 3.3.8 Accessible Authentication (Minimum)
- 3.3.9 Accessible Authentication (Enhanced) - Level AAA

## Critical Level AA Checks

### Perceivable
- 1.4.3 Contrast (Minimum): 4.5:1 text, 3:1 large text
- 1.4.5 Images of Text: Avoid except logos
- 1.4.10 Reflow: No 2D scroll at 320px width
- 1.4.11 Non-text Contrast: 3:1 for UI components
- 1.4.12 Text Spacing: Allow user override

### Operable
- 2.4.7 Focus Visible: Keyboard focus indicator
- 2.5.8 Target Size: Min 24x24 CSS pixels (new in 2.2)

### Understandable
- 3.2.6 Consistent Help: Same location across pages (new in 2.2)
- 3.3.7 Redundant Entry: Auto-fill previously entered data (new in 2.2)

### Robust
- 4.1.3 Status Messages: Use ARIA live regions

## Design Token Accessibility

- Contrast tokens must meet 4.5:1 threshold
- Touch target tokens ≥24x24 CSS pixels
- Focus indicator tokens must be visible
- Document contrast ratios in token metadata

---
name: Warm Editorial
colors:
  surface: '#fdf8f7'
  surface-dim: '#ddd9d8'
  surface-bright: '#fdf8f7'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f7f3f1'
  surface-container: '#f1edec'
  surface-container-high: '#ece7e6'
  surface-container-highest: '#e6e1e0'
  on-surface: '#1c1b1b'
  on-surface-variant: '#4d4540'
  inverse-surface: '#313030'
  inverse-on-surface: '#f4f0ee'
  outline: '#7e756f'
  outline-variant: '#cfc4bd'
  surface-tint: '#635d5a'
  primary: '#181512'
  on-primary: '#ffffff'
  primary-container: '#2d2926'
  on-primary-container: '#96908b'
  inverse-primary: '#cdc5c0'
  secondary: '#6e5b44'
  on-secondary: '#ffffff'
  secondary-container: '#f5dcbe'
  on-secondary-container: '#725f48'
  tertiary: '#151618'
  on-tertiary: '#ffffff'
  tertiary-container: '#292a2c'
  on-tertiary-container: '#919193'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e9e1dc'
  primary-fixed-dim: '#cdc5c0'
  on-primary-fixed: '#1e1b18'
  on-primary-fixed-variant: '#4b4642'
  secondary-fixed: '#f8dec1'
  secondary-fixed-dim: '#dbc3a6'
  on-secondary-fixed: '#261907'
  on-secondary-fixed-variant: '#55442e'
  tertiary-fixed: '#e3e2e4'
  tertiary-fixed-dim: '#c7c6c8'
  on-tertiary-fixed: '#1a1c1d'
  on-tertiary-fixed-variant: '#464749'
  background: '#fdf8f7'
  on-background: '#1c1b1b'
  surface-variant: '#e6e1e0'
typography:
  h1:
    fontFamily: Newsreader
    fontSize: 48px
    fontWeight: '600'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  h2:
    fontFamily: Newsreader
    fontSize: 32px
    fontWeight: '500'
    lineHeight: '1.2'
  h3:
    fontFamily: Newsreader
    fontSize: 24px
    fontWeight: '500'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Newsreader
    fontSize: 20px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Newsreader
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  label-caps:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.1em
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.4'
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1200px
  reading-width: 720px
  gutter: 24px
  margin-mobile: 20px
  section-gap: 80px
---

## Brand & Style

The design system is centered on the concept of "Digital Slow Living." It prioritizes the reading experience by reducing visual noise and using a palette that mimics high-quality paper and ink. The target audience includes long-form readers, thinkers, and creative writers who value clarity and a calm browsing environment.

The design style is **Minimalism** with an **Editorial** influence. It leverages generous white space (macro-spacing) to allow content to breathe, creating an airy feel that prevents cognitive overload. The aesthetic is sophisticated and timeless, evoking the feeling of a premium physical journal rather than a cluttered digital interface.

## Colors

The palette is strictly limited to organic, warm tones. The primary background uses a soft cream to reduce eye strain compared to pure white. A slightly deeper beige is used for secondary surfaces, such as sidebars or footer areas, to create subtle depth without relying on shadows.

The primary "ink" color is a dark charcoal, providing high contrast for readability while feeling softer and more natural than true black. An accent taupe is used sparingly for secondary elements like categories or dates to maintain the minimalist hierarchy.

## Typography

This design system uses a dual-font strategy to balance literary tradition with modern usability. **Newsreader** is the workhorse, used for both headlines and body text to create a cohesive, book-like flow. Its variable weights allow for elegant emphasis without disrupting the visual rhythm.

**Plus Jakarta Sans** is used exclusively for functional UI elements—labels, buttons, and navigation metadata. This distinction helps the user subconsciously separate "the content" from "the interface." Line heights for body text are intentionally generous (1.6) to facilitate effortless vertical scanning.

## Layout & Spacing

The layout utilizes a **Fixed Grid** model for desktop to ensure the reading experience remains optimized. The central content column is restricted to a 720px "reading width" to maintain ideal characters-per-line counts. 

A 12-column grid is used for the overall container, allowing for flexible sidebar placements or gallery layouts. Spacing follows an 8px rhythmic scale, but the design system encourages "over-spacing" between major sections (80px+) to emphasize the airy, minimalist philosophy. On mobile, margins are reduced to 20px, but vertical gaps remain large to maintain the brand feel.

## Elevation & Depth

To maintain the minimalist aesthetic, the design system avoids heavy drop shadows. Depth is communicated through **Tonal Layers** and **Low-Contrast Outlines**.

1.  **Surface Tiers:** Backgrounds are layered with the primary cream (#FDFBF7) as the base and the secondary beige (#F5F0E6) for inset elements or cards.
2.  **Ghost Borders:** When structural separation is required, a very thin (1px) border in a slightly darker taupe is used.
3.  **Elevation:** For interactive hover states, a very subtle, diffused ambient shadow (4% opacity charcoal) may be used to lift an element slightly, but the preference is always to use color shifts or underline transitions first.

## Shapes

The shape language is **Soft** and understated. A 0.25rem (4px) corner radius is applied to buttons and input fields to take the "edge" off the design without making it feel overly playful or "bubbly." Images should either be sharp-edged for a classic editorial look or follow the soft 4px radius for a more contemporary feel. The goal is to feel organic and architectural.

## Components

**Buttons**
Primary buttons utilize the dark charcoal background with cream text. Secondary buttons are "Ghost" style—thin borders with label-caps typography. Hover states involve a subtle background color shift.

**Cards**
Article cards should be minimalist. Use high-quality imagery followed by a category label (label-caps), a headline (H3), and a short excerpt. No heavy borders or shadows; use whitespace to define the card boundaries.

**Input Fields**
Simple, clean lines. Use a bottom-border only or a very light taupe outline. Focus states should transition the border color to the primary charcoal.

**Metadata Chips**
Small, rectangular chips with the secondary beige background and Plus Jakarta Sans typography. No heavy rounding; keep them soft but professional.

**Navigation**
The header should be transparent or utilize the primary background color, with simple text links. A "sticky" behavior is recommended for the header, but it should be visually lightweight to avoid encroaching on the reading space.
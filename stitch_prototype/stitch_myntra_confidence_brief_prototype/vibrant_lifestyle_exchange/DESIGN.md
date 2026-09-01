---
name: Vibrant Lifestyle Exchange
colors:
  surface: '#f9f9f9'
  surface-dim: '#dadada'
  surface-bright: '#f9f9f9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3f4'
  surface-container: '#eeeeee'
  surface-container-high: '#e8e8e8'
  surface-container-highest: '#e2e2e2'
  on-surface: '#1a1c1c'
  on-surface-variant: '#5b4042'
  inverse-surface: '#2f3131'
  inverse-on-surface: '#f0f1f1'
  outline: '#8f6f72'
  outline-variant: '#e3bdc0'
  surface-tint: '#bd0043'
  primary: '#b90041'
  on-primary: '#ffffff'
  primary-container: '#df2457'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb2ba'
  secondary: '#5a5d73'
  on-secondary: '#ffffff'
  secondary-container: '#dbdef8'
  on-secondary-container: '#5e6177'
  tertiary: '#006a34'
  on-tertiary: '#ffffff'
  tertiary-container: '#008644'
  on-tertiary-container: '#f6fff3'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffd9dc'
  primary-fixed-dim: '#ffb2ba'
  on-primary-fixed: '#400011'
  on-primary-fixed-variant: '#910031'
  secondary-fixed: '#dee1fa'
  secondary-fixed-dim: '#c2c5de'
  on-secondary-fixed: '#161b2d'
  on-secondary-fixed-variant: '#42465a'
  tertiary-fixed: '#7dfca2'
  tertiary-fixed-dim: '#5fde88'
  on-tertiary-fixed: '#00210c'
  on-tertiary-fixed-variant: '#005227'
  background: '#f9f9f9'
  on-background: '#1a1c1c'
  surface-variant: '#e2e2e2'
  text-muted: '#94969F'
  border-light: '#E9E9EB'
  background-alt: '#F5F5F6'
  confidence-tint: '#FFF9FB'
typography:
  display-lg:
    fontFamily: Hanken Grotesk
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: 0.5px
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 20px
    fontWeight: '700'
    lineHeight: 24px
  nav-link:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.3px
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-sm:
    fontFamily: Hanken Grotesk
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  label-xs:
    fontFamily: Hanken Grotesk
    fontSize: 10px
    fontWeight: '700'
    lineHeight: 12px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  container-max-width: 1280px
  gutter: 1.5rem
  margin-x: 2.5rem
  stack-sm: 0.5rem
  stack-md: 1rem
  stack-lg: 2rem
---

## Brand & Style

This design system embodies a **Corporate / Modern** aesthetic with a high-energy, fashion-forward edge. It is designed for a diverse, trend-conscious audience that values efficiency and visual inspiration. The UI is characterized by high-density information layouts balanced by generous white space and a vibrant, iconic primary color.

The emotional response should be one of confidence, accessibility, and excitement. By utilizing clean lines and a structured grid, the system provides a reliable shopping experience, while the "Confidence Brief" elements introduce an editorial and trustworthy tone through soft color washes and delicate iconography.

## Colors

The palette is anchored by the signature brand pink, used strategically for calls to action, active states, and promotional highlights. The primary text color is a deep charcoal, providing superior legibility against the white background, while a muted gray is reserved for secondary information and metadata.

A specialized "Confidence Tint" is utilized for background containers that house editorial content or trust-building messaging. This soft pink hue differentiates these sections from standard product grids.

## Typography

The design system utilizes a clean, geometric sans-serif to maintain a professional and contemporary feel. Navigation items and headlines use a bold weight to establish clear hierarchy and brand authority. 

Uppercase styling is applied to top-level navigation categories to increase visibility. For mobile viewports, display sizes are scaled down to ensure that product titles and category headers remain readable without excessive wrapping.

## Layout & Spacing

This design system uses a **fixed grid** model for desktop, centered on the viewport with a maximum width to ensure optimal line lengths for product information. The grid consists of 12 columns with a standard gutter.

- **Desktop:** 12-column grid, 40px side margins.
- **Tablet:** 8-column grid, 24px side margins.
- **Mobile:** 4-column grid, 16px side margins.

The spacing rhythm follows a 4px baseline, ensuring that all vertical increments (padding, margins, line heights) are multiples of 4 for visual consistency and mathematical balance.

## Elevation & Depth

Hierarchy is primarily achieved through **low-contrast outlines** and **tonal layers** rather than heavy shadows. 

- **Surface Level 0:** Background white (#FFFFFF).
- **Surface Level 1:** Hover states on cards use a subtle ambient shadow (0px 4px 12px rgba(0,0,0,0.05)).
- **Sticky Header:** Uses a slight bottom border (#E9E9EB) and high-z-index to stay above content during scroll.
- **Dropdowns/Modals:** Defined by crisp 1px borders and a slightly more pronounced shadow to separate from the main canvas.

## Shapes

The shape language is **Soft**, favoring subtle corner radii over sharp edges or aggressive rounding. This approach maintains a professional "fashion catalog" look while feeling modern and approachable. 

Buttons and input fields follow the `rounded-sm` (4px) standard, while larger containers like cards or promotional banners may use `rounded-md` (8px). Badges and pills (like the "NEW" indicator) use full pill-rounding to differentiate them from functional UI elements.

## Components

### Navigation
The header is sticky and full-width. Navigation links are bold and uppercase. The search bar is centered, using a light gray background (#F5F5F6) and minimal borders. Icons for Profile, Wishlist, and Bag are accompanied by labels for maximum clarity.

### Buttons
Primary buttons are solid brand pink with white text. Secondary buttons are outlined in the primary text color. All buttons use 4px rounded corners and transitions on hover (opacity or slight darken).

### Cards
Product cards are minimalist. They feature a borderless image on top, followed by a product title (bold) and brand name. Subtle 1px borders appear only on hover or to separate distinct category blocks.

### Input Fields
Inputs are clean with a 1px border (#E9E9EB). Focus states are indicated by a color shift of the border to the primary brand pink or a 1px solid black.

### Confidence Brief
A specialized component for trust-building. It features a #FFF9FB background, a sparkle icon in the top right, and high-quality editorial typography. This section is used to communicate shipping guarantees, authenticity, and brand promises.
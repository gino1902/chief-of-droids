/**
 * elevate-tokens.js
 * Elevate theme — JS/TS design tokens
 * Canonical source: shared/elevate-theme/tokens.json
 * Derived from:     shared/Elevate-theme-colors.md
 *
 * Usage (React / plain JS):
 *   import { elevateColors, elevateTokens } from './elevate-tokens.js';
 *
 * Usage (Tailwind v3 only — see elevate-tailwind-v4.css for v4):
 *   const { tailwindElevate } = require('./elevate-tokens.js');
 *   module.exports = { theme: { extend: { colors: tailwindElevate } } };
 *
 * Font: TWK Everett Light — load via @font-face or a font provider at runtime.
 *
 * Tailwind version note:
 *   tailwindElevate targets Tailwind CSS v3 (tailwind.config.js).
 *   Tailwind v4 uses a CSS-first @theme directive — use elevate-tailwind-v4.css instead.
 */

/** Raw palette — hex values keyed by OOXML role name */
export const elevateColors = {
  dk1:     '#000000', // Primary dark / text
  lt1:     '#FFFFFF', // Primary light / background
  dk2:     '#0F0E2B', // Near-black navy
  lt2:     '#FFFAF0', // Warm cream
  accent1: '#1F24E9', // Electric blue — primary brand
  accent2: '#6DA5FF', // Sky blue
  accent3: '#C5D8F6', // Ice blue (light)
  accent4: '#425F8B', // Steel blue (muted)
  accent5: '#6164EB', // Violet-blue
  accent6: '#8E8FEC', // Periwinkle (soft)
  // Aliases — keep in sync with accent1/accent2 if palette changes
  hyperlink:          '#1F24E9', // = accent1
  followedHyperlink:  '#6DA5FF', // = accent2
};

/** Semantic tokens — use these in components, not raw hex */
export const elevateTokens = {
  color: {
    text:           elevateColors.dk1,
    background:     elevateColors.lt1,
    surface:        elevateColors.lt2,      // warm cream — cards, panels
    surfaceDark:    elevateColors.dk2,      // navy — dark backgrounds
    brand:          elevateColors.accent1,  // primary CTA, active states
    brandLight:     elevateColors.accent2,  // secondary, hover
    brandLightest:  elevateColors.accent3,  // tints, highlights
    brandMuted:     elevateColors.accent4,  // subdued UI elements
    brandAlt:       elevateColors.accent5,  // alternate accent
    brandSoft:      elevateColors.accent6,  // soft accent, badges
    link:           elevateColors.accent1,
    linkVisited:    elevateColors.accent2,
  },
  font: {
    family: '"TWK Everett Light", system-ui, sans-serif',
  },
};

/**
 * Tailwind v3 color extension
 * Registers colors under the 'elevate' namespace.
 * Usage in JSX: className="bg-elevate-brand text-elevate-lt1"
 *
 * NOTE: Use elevate-lt1 (not Tailwind's built-in 'white') for Elevate-themed whites
 * to keep all colors within the token system.
 *
 * Tailwind v4 users: see elevate-tailwind-v4.css — this export is not compatible
 * with v4's CSS-first @theme configuration.
 */
export const tailwindElevate = {
  elevate: {
    // Raw palette
    dk1:               elevateColors.dk1,
    lt1:               elevateColors.lt1,
    dk2:               elevateColors.dk2,
    lt2:               elevateColors.lt2,
    accent1:           elevateColors.accent1,
    accent2:           elevateColors.accent2,
    accent3:           elevateColors.accent3,
    accent4:           elevateColors.accent4,
    accent5:           elevateColors.accent5,
    accent6:           elevateColors.accent6,
    // Semantic aliases
    text:              elevateColors.dk1,
    background:        elevateColors.lt1,
    surface:           elevateColors.lt2,
    'surface-dark':    elevateColors.dk2,
    brand:             elevateColors.accent1,
    'brand-light':     elevateColors.accent2,
    'brand-lightest':  elevateColors.accent3,
    'brand-muted':     elevateColors.accent4,
    'brand-alt':       elevateColors.accent5,
    'brand-soft':      elevateColors.accent6,
    link:              elevateColors.accent1,
    'link-visited':    elevateColors.accent2,
  },
};

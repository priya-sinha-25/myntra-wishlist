"""Shared CSS matching Stitch Myntra prototype."""

MYNTRA_STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&display=swap');
:root {
  --primary: #FF3F6C;
  --primary-dark: #b90041;
  --on-surface: #1a1c1c;
  --text-muted: #94969F;
  --border-light: #E9E9EB;
  --background: #f9f9f9;
  --background-alt: #F5F5F6;
  --confidence-tint: #FFF9FB;
  --tertiary: #006a34;
  --tertiary-container: #008644;
  --inverse-surface: #2f3131;
  --surface-lowest: #ffffff;
  --surface-container-low: #f3f3f4;
  --surface-variant: #e2e2e2;
  --margin-x: 2.5rem;
}
* { box-sizing: border-box; }
.myntra-mvp {
  font-family: 'Hanken Grotesk', sans-serif;
  color: var(--on-surface);
  background: var(--background);
  min-height: 100vh;
}
.myntra-mvp .header {
  position: sticky; top: 0; z-index: 100;
  background: var(--surface-lowest);
  box-shadow: 0 1px 8px rgba(0,0,0,0.04);
  height: 80px;
  display: flex; align-items: center;
  padding: 0 var(--margin-x);
  justify-content: space-between;
}
.myntra-mvp .logo {
  display: flex; align-items: center; flex-shrink: 0; text-decoration: none;
}
.myntra-mvp .logo img {
  height: 44px; width: auto; display: block;
}
.myntra-mvp .nav { display: flex; gap: 24px; align-items: center; height: 80px; margin-left: 40px; }
.myntra-mvp .nav a {
  font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.3px;
  color: #5b4042; text-decoration: none; height: 80px; display: flex; align-items: center;
  padding: 0 4px; border-bottom: 4px solid transparent;
}
.myntra-mvp .nav a.nav-home-link {
  font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.3px;
  color: #5b4042; text-decoration: none; height: 80px; display: flex; align-items: center;
  padding: 0 4px; border-bottom: 4px solid transparent; cursor: pointer;
}
#mvp-nav-home:checked ~ .header .nav a.nav-home-link {
  color: var(--on-surface); border-bottom-color: var(--primary);
}
.myntra-mvp .nav a.active { color: var(--on-surface); border-bottom-color: var(--primary); }
.myntra-mvp .search {
  flex: 1; max-width: 500px; margin-left: 48px;
  display: flex; align-items: center; background: var(--background-alt);
  border-radius: 8px; padding: 8px 16px;
}
.myntra-mvp .search input {
  border: none; background: transparent; outline: none; width: 100%;
  margin-left: 12px; font-size: 14px;
}
.myntra-mvp .utilities { display: flex; gap: 32px; margin-left: 40px; align-items: center; position: relative; z-index: 110; }
.myntra-mvp .util-item {
  display: flex; flex-direction: column; align-items: center;
  font-size: 12px; color: var(--on-surface); cursor: pointer;
  border: none; background: transparent; padding: 0; position: relative;
  text-decoration: none;
}
.myntra-mvp .util-item-static { cursor: default; }
.myntra-mvp .util-label { margin-top: 4px; font-size: 12px; }
.myntra-mvp .profile-avatar {
  width: 32px; height: 32px; border-radius: 50%; background: var(--primary);
  display: flex; align-items: center; justify-content: center;
}
.myntra-mvp .profile-avatar .material-symbols-outlined { color: white; font-size: 18px; }
.myntra-mvp .search-icon { color: #5b4042; font-size: 20px; }
.myntra-mvp .util-item:hover .icon { color: var(--primary); }
.myntra-mvp .util-item .icon { font-size: 22px; color: #5b4042; }
.myntra-mvp .mvp-nav-radio {
  position: absolute; opacity: 0; width: 0; height: 0;
  pointer-events: none; margin: 0; padding: 0;
}
.myntra-mvp .screen { display: none; }
#mvp-nav-home:checked ~ #screen-home { display: block; }
#mvp-nav-wishlist:checked ~ #screen-wishlist { display: block; }
#mvp-nav-bag:checked ~ #screen-bag { display: block; }
#mvp-nav-home:checked ~ .header #nav-home .icon,
#mvp-nav-wishlist:checked ~ .header #nav-wishlist .icon,
#mvp-nav-bag:checked ~ .header #nav-bag .icon { color: var(--primary); }
.myntra-mvp .modal-radio {
  position: absolute; opacity: 0; pointer-events: none; width: 0; height: 0;
}
.myntra-mvp .modal-backdrop {
  position: fixed; inset: 0; top: 80px; background: rgba(26,28,28,0.4);
  align-items: center; justify-content: center; z-index: 200;
  padding: 24px;
  display: none;
}
.myntra-mvp .modal-radio:checked + .modal-backdrop { display: flex; }
.myntra-mvp .modal-dismiss {
  position: absolute; inset: 0; top: 0; cursor: default;
}
.myntra-mvp .brief-modal,
.myntra-mvp .locked-modal { position: relative; z-index: 1; }
.myntra-mvp .modal-close-btn {
  border: none; background: transparent; cursor: pointer; text-decoration: none;
  color: inherit; display: inline-flex; align-items: center; justify-content: center;
}
.myntra-mvp .loading-overlay {
  display: none; position: fixed; inset: 0; top: 80px; z-index: 250;
  background: rgba(26,28,28,0.5); align-items: center; justify-content: center;
}
.myntra-mvp .loading-overlay.open { display: flex; }
.myntra-mvp .loading-box {
  background: white; padding: 24px 32px; border-radius: 12px; text-align: center;
  box-shadow: 0 12px 40px rgba(0,0,0,0.2);
}
.myntra-mvp .badge {
  position: absolute; top: -4px; right: -4px;
  background: var(--primary); color: white; font-size: 10px;
  width: 16px; height: 16px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center; font-weight: 700;
  pointer-events: none;
}
.myntra-mvp .promo-tab {
  position: fixed; right: 0; top: 50%; transform: translateY(-50%) rotate(180deg);
  writing-mode: vertical-rl; background: var(--inverse-surface); color: white;
  padding: 16px 8px; font-size: 10px; font-weight: 700; text-transform: uppercase;
  z-index: 50; cursor: pointer; pointer-events: auto;
}
.myntra-mvp .main { padding-top: 0; }
.myntra-mvp .category-grid {
  display: grid; grid-template-columns: repeat(6, 1fr); gap: 24px;
  padding: 40px var(--margin-x); max-width: 1920px; margin: 0 auto;
}
.myntra-mvp .category-tile {
  background: #FEF4E8; padding: 8px; cursor: pointer;
  transition: box-shadow 0.3s;
}
.myntra-mvp .category-tile:hover { box-shadow: 0 8px 24px rgba(0,0,0,0.1); }
.myntra-mvp .category-tile img { width: 100%; aspect-ratio: 4/5; object-fit: cover; }
.myntra-mvp .category-info {
  background: rgba(255,255,255,0.9); padding: 16px; text-align: center;
  margin: -16px 8px 0; position: relative; z-index: 1;
}
.myntra-mvp .shop-title {
  text-align: center; font-size: 40px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.15em; margin: 32px 0 0;
}
.myntra-mvp .wishlist-header {
  display: flex; justify-content: space-between; align-items: flex-end;
  padding: 48px var(--margin-x) 16px; border-bottom: 1px solid var(--border-light);
  max-width: 1280px; margin: 0 auto;
}
.myntra-mvp .wishlist-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px;
  padding: 32px var(--margin-x); max-width: 1280px; margin: 0 auto;
}
.myntra-mvp .product-card {
  background: var(--background); display: flex; flex-direction: column;
  transition: box-shadow 0.3s; position: relative;
}
.myntra-mvp .product-card:hover { box-shadow: 0 12px 32px rgba(0,0,0,0.12); }
.myntra-mvp .product-card.selected { outline: 2px solid var(--primary); outline-offset: 2px; }
.myntra-mvp .product-card.locked { opacity: 0.9; }
.myntra-mvp .product-img-wrap { position: relative; aspect-ratio: 3/4; overflow: hidden; background: var(--surface-container-low); }
.myntra-mvp .product-img-wrap img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s; }
.myntra-mvp .product-card:hover .product-img-wrap img { transform: scale(1.05); }
.myntra-mvp .product-card.locked .product-img-wrap img { filter: grayscale(20%); }
.myntra-mvp .lock-overlay {
  position: absolute; inset: 0; background: rgba(255,255,255,0.2);
  backdrop-filter: blur(2px); display: flex; align-items: center; justify-content: center;
  text-decoration: none; color: inherit;
}
.myntra-mvp .lock-circle {
  background: white; padding: 16px; border-radius: 50%; box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}
.myntra-mvp .rating-badge {
  position: absolute; bottom: 0; left: 0; right: 0;
  background: linear-gradient(transparent, rgba(0,0,0,0.6)); padding: 12px;
}
.myntra-mvp .rating-pill {
  background: white; padding: 4px 8px; border-radius: 4px; font-size: 10px; font-weight: 700;
  display: inline-flex; align-items: center; gap: 4px;
}
.myntra-mvp .card-body { padding: 16px; border: 1px solid var(--border-light); border-top: none; flex: 1; display: flex; flex-direction: column; gap: 8px; }
.myntra-mvp .brand { font-size: 20px; font-weight: 700; margin: 0; }
.myntra-mvp .product-name { font-size: 14px; color: #5b4042; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.myntra-mvp .price-row { display: flex; align-items: center; gap: 8px; }
.myntra-mvp .price { font-weight: 700; font-size: 12px; }
.myntra-mvp .mrp { font-size: 10px; color: var(--text-muted); text-decoration: line-through; }
.myntra-mvp .off { font-size: 10px; color: var(--primary); font-weight: 700; }
.myntra-mvp .saved { font-size: 10px; color: var(--text-muted); margin-top: 4px; }
.myntra-mvp .brief-box {
  background: var(--confidence-tint); padding: 12px; border-radius: 4px;
  border: 1px solid rgba(227,189,192,0.3); display: flex; gap: 8px; align-items: flex-start; margin-top: auto;
}
.myntra-mvp .brief-box.locked {
  background: var(--surface-container-low); border-color: var(--border-light);
  justify-content: center; text-decoration: none; color: inherit; cursor: pointer;
}
.myntra-mvp .brief-box .sparkle { color: var(--primary); font-size: 18px; }
.myntra-mvp .brief-ready { font-size: 12px; color: var(--primary); font-weight: 500; text-transform: uppercase; margin: 0; }
.myntra-mvp .brief-sub { font-size: 10px; color: #5b4042; margin: 4px 0 0; }
.myntra-mvp .btn-primary {
  width: 100%; background: var(--primary); color: white; border: none;
  padding: 12px; font-size: 14px; font-weight: 700; text-transform: uppercase;
  cursor: pointer; border-radius: 4px; margin-top: 12px;
  display: block; text-align: center; text-decoration: none; box-sizing: border-box;
}
.myntra-mvp label.btn-primary,
.myntra-mvp label.btn-disabled,
.myntra-mvp label.btn-outline { cursor: pointer; }
.myntra-mvp .btn-primary:hover { background: #e7355f; }
.myntra-mvp .btn-disabled {
  width: 100%; background: var(--surface-variant); color: var(--text-muted);
  border: none; padding: 12px; font-size: 14px; font-weight: 700;
  text-transform: uppercase; cursor: pointer; border-radius: 4px; margin-top: 12px;
  display: block; text-align: center; text-decoration: none; box-sizing: border-box;
}
.myntra-mvp .btn-in-bag {
  width: 100%; background: var(--tertiary); color: white; border: none;
  padding: 12px; font-size: 12px; font-weight: 500; text-transform: uppercase;
  border-radius: 4px; display: flex; align-items: center; justify-content: center; gap: 8px;
}
.myntra-mvp .brief-modal {
  width: 100%; max-width: 560px; background: var(--confidence-tint);
  border-radius: 12px; box-shadow: 0 24px 48px rgba(0,0,0,0.2);
  overflow: hidden; animation: fadeInUp 0.5s ease-out;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
.myntra-mvp .modal-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 24px 24px 12px; border-bottom: 1px solid var(--surface-variant);
}
.myntra-mvp .modal-title { display: flex; align-items: center; gap: 8px; color: var(--primary); font-size: 20px; font-weight: 700; }
.myntra-mvp .product-row {
  display: flex; gap: 16px; padding: 16px 24px; background: rgba(255,255,255,0.5);
}
.myntra-mvp .product-thumb { width: 64px; height: 80px; border-radius: 4px; object-fit: cover; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.myntra-mvp .size-hero {
  text-align: center; padding: 32px 24px; border-bottom: 1px solid var(--surface-variant);
}
.myntra-mvp .size-label { font-size: 12px; color: #5b4042; text-transform: uppercase; letter-spacing: 0.15em; }
.myntra-mvp .size-circle {
  width: 80px; height: 80px; border-radius: 50%; background: var(--primary);
  color: white; font-size: 40px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  margin: 16px auto; box-shadow: 0 8px 24px rgba(255,63,108,0.3);
}
.myntra-mvp .insights { padding: 16px 24px; background: rgba(255,255,255,0.3); }
.myntra-mvp .insights h4 { font-size: 12px; text-transform: uppercase; color: #5b4042; margin: 0 0 12px; }
.myntra-mvp .insight-item { display: flex; gap: 12px; margin-bottom: 12px; font-size: 14px; }
.myntra-mvp .insight-item .check { color: var(--tertiary-container); font-size: 20px; }
.myntra-mvp .modal-footer {
  padding: 24px; background: white; display: flex; flex-direction: column; gap: 12px;
  box-shadow: 0 -4px 20px rgba(0,0,0,0.05);
}
.myntra-mvp .modal-actions { display: flex; gap: 16px; }
.myntra-mvp .btn-outline {
  flex: 1; border: 1px solid #8f6f72; background: transparent; color: var(--on-surface);
  padding: 12px; font-size: 12px; font-weight: 500; text-transform: uppercase;
  cursor: pointer; border-radius: 4px; text-decoration: none;
  display: flex; align-items: center; justify-content: center; box-sizing: border-box;
}
.myntra-mvp .mvp-bag-form { margin: 0; flex: 2; display: flex; }
.myntra-mvp .mvp-bag-form-inline { flex: none; display: inline-flex; }
.myntra-mvp .mvp-bag-form .btn-add-bag { width: 100%; }
.myntra-mvp .btn-add-bag {
  flex: 2; background: var(--primary); color: white; border: none;
  padding: 12px; font-size: 12px; font-weight: 500; text-transform: uppercase;
  cursor: pointer; border-radius: 4px; box-shadow: 0 4px 12px rgba(255,63,108,0.2);
  text-decoration: none; display: flex; align-items: center; justify-content: center;
}
.myntra-mvp .toast { display: none; }
.myntra-mvp .ai-footer { text-align: center; font-size: 10px; color: #5b4042; text-transform: uppercase; opacity: 0.6; }
.myntra-mvp .locked-modal {
  max-width: 384px; background: white; border-radius: 12px; padding: 32px;
  text-align: center; box-shadow: 0 24px 48px rgba(0,0,0,0.2);
}
.myntra-mvp .progress-box {
  background: var(--surface-container-low); border-radius: 8px; padding: 16px;
  text-align: left; margin: 24px 0; position: relative; overflow: hidden;
}
.myntra-mvp .progress-box::before {
  content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
  background: var(--primary); border-radius: 4px 0 0 4px;
}
.myntra-mvp .progress-bar { height: 8px; background: var(--surface-variant); border-radius: 999px; overflow: hidden; margin-top: 8px; }
.myntra-mvp .progress-fill { height: 100%; background: var(--primary); border-radius: 999px; }
.myntra-mvp .similar-thumbs { display: flex; gap: 8px; margin-top: 8px; }
.myntra-mvp .similar-thumb { flex: 1; aspect-ratio: 3/4; border-radius: 8px; overflow: hidden; position: relative; }
.myntra-mvp .similar-thumb img { width: 100%; height: 100%; object-fit: cover; }
.myntra-mvp .toast {
  position: fixed; top: 96px; right: var(--margin-x); z-index: 300;
  background: white; box-shadow: 0 8px 32px rgba(0,0,0,0.15); border-radius: 8px;
  padding: 16px; display: flex; align-items: center; gap: 16px;
  animation: slideIn 0.5s ease-out;
}
@keyframes slideIn {
  from { transform: translateX(120%); }
  to { transform: translateX(0); }
}
.myntra-mvp .toast-icon {
  width: 40px; height: 40px; background: var(--tertiary-container); border-radius: 50%;
  display: flex; align-items: center; justify-content: center; color: white;
}
.myntra-mvp .filter-btn {
  background: var(--surface-container-low); border: none; padding: 8px 16px;
  border-radius: 4px; font-size: 12px; text-transform: uppercase; cursor: pointer;
  display: flex; align-items: center; gap: 8px; text-decoration: none; color: inherit;
}
.myntra-mvp .bag-empty-cta {
  max-width: 280px; margin-top: 16px; display: block; text-align: center;
}
.myntra-mvp .locked-hint {
  font-size: 11px; color: var(--primary); margin: 0; cursor: pointer;
  text-align: center; font-weight: 500; display: block;
}
.myntra-mvp .locked-hint:hover { text-decoration: underline; }
.myntra-mvp .bag-header {
  display: flex; justify-content: space-between; align-items: flex-end;
  padding: 48px var(--margin-x) 16px; border-bottom: 1px solid var(--border-light);
  max-width: 1280px; margin: 0 auto;
}
.myntra-mvp .bag-layout {
  display: grid; grid-template-columns: 1fr 320px; gap: 32px;
  padding: 32px var(--margin-x); max-width: 1280px; margin: 0 auto;
}
.myntra-mvp .bag-items-list { display: flex; flex-direction: column; gap: 16px; }
.myntra-mvp .bag-item-row {
  display: flex; gap: 16px; align-items: flex-start; background: white;
  border: 1px solid var(--border-light); padding: 16px; border-radius: 4px;
}
.myntra-mvp .bag-item-row img { width: 80px; height: 100px; object-fit: cover; border-radius: 4px; }
.myntra-mvp .bag-item-info { flex: 1; }
.myntra-mvp .bag-item-info h4 { margin: 0 0 4px; font-size: 16px; }
.myntra-mvp .bag-item-info p { margin: 0 0 8px; font-size: 13px; color: #5b4042; }
.myntra-mvp .bag-item-size { font-size: 12px; color: var(--text-muted); display: block; margin-bottom: 4px; }
.myntra-mvp .bag-item-price { font-weight: 700; font-size: 14px; }
.myntra-mvp .bag-remove {
  border: none; background: transparent; cursor: pointer; color: var(--text-muted); padding: 4px;
  text-decoration: none; display: inline-flex; align-items: center; justify-content: center;
}
.myntra-mvp .bag-empty {
  grid-column: 1 / -1; display: flex; flex-direction: column; align-items: center;
  justify-content: center; padding: 64px 24px; text-align: center; color: #5b4042;
}
.myntra-mvp .bag-empty h2 { margin: 16px 0 8px; font-size: 24px; }
.myntra-mvp .bag-summary {
  background: white; border: 1px solid var(--border-light); border-radius: 4px;
  padding: 24px; height: fit-content; position: sticky; top: 96px;
}
.myntra-mvp .bag-summary h3 { margin: 0 0 16px; font-size: 14px; text-transform: uppercase; }
.myntra-mvp .summary-row {
  display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 14px;
}
.myntra-mvp .summary-row.muted { color: var(--text-muted); font-size: 13px; }
.myntra-mvp .summary-row.total {
  border-top: 1px solid var(--border-light); padding-top: 12px; margin-top: 8px;
  font-weight: 700; font-size: 16px;
}
.myntra-mvp .bag-demo-note { font-size: 10px; color: var(--text-muted); text-align: center; margin-top: 12px; }
.myntra-mvp .toast-link {
  border: none; background: transparent; color: var(--primary); font-size: 14px;
  font-weight: 700; text-transform: uppercase; cursor: pointer; padding: 0;
}
label.toast-link { display: inline-block; }
a.filter-btn { cursor: pointer; text-decoration: none; color: inherit; }
.myntra-mvp .material-symbols-outlined,
.material-symbols-outlined {
  font-family: 'Material Symbols Outlined';
  font-weight: normal;
  font-style: normal;
  font-size: 24px;
  line-height: 1;
  letter-spacing: normal;
  text-transform: none;
  display: inline-block;
  white-space: nowrap;
  direction: ltr;
  -webkit-font-smoothing: antialiased;
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
</style>
"""

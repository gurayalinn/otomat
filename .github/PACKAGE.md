<h1> PACKAGES </h1>

<details open>
<summary><strong>TOOLS LIST</strong></summary>

- [sanitize](#sanitize)
- [normalize](#normalize)
- [htmx](#htmx)
- [jquery](#jquery)
- [tailwindcss](#tailwindcss)
- [fontawesome-free](#fontawesome-free)
- [fonts](#fonts)
- [favicon](#favicon)

</details>

### sanitize

<details>
<summary>details</summary>

[package](https://www.jsdelivr.com/package/npm/sanitize.css) -
[repo](https://github.com/csstools/sanitize.css/)

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/sanitize.css@13.0.0/sanitize.min.css"
/>
```

</details>

---

### normalize

<details>
<summary>details</summary>

[package](https://www.jsdelivr.com/package/npm/normalize.css) -
[repo](https://github.com/necolas/normalize.css/)

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/normalize.css@8.0.1/normalize.min.css"
/>
```

</details>

---

### htmx

<details>
<summary>details</summary>

[package](https://www.jsdelivr.com/package/npm/htmx.org) -
[repo](https://github.com/bigskysoftware/htmx/)

```html
<script src="https://cdn.jsdelivr.net/npm/htmx.org@1.9.10/dist/ext/ws.min.js"></script>
```

</details>

---

### jquery

<details>
<summary>details</summary>

[package](https://www.jsdelivr.com/package/npm/jquery) -
[repo](https://github.com/jquery/jquery/)

```html
<script
  src="https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js"
  integrity="sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo="
  crossorigin="anonymous"
></script>
```

</details>

---

### tailwindcss

<details>
<summary>details</summary>

[package](https://www.jsdelivr.com/package/npm/tailwindcss) -
[repo](https://github.com/tailwindlabs/tailwindcss/)

```html
<script src="https://cdn.jsdelivr.net/npm/tailwindcss@3.4.1/lib/index.min.js"></script>

<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/tailwindcss@3.4.1/base.min.css"
/>
```

</details>

---

### fontawesome-free

<details>
<summary>details</summary>

[package](https://www.jsdelivr.com/package/npm/@fortawesome/fontawesome-free) -
[repo](https://github.com/FortAwesome/Font-Awesome/)

```html
<script
  src="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.5.1/js/fontawesome.min.js"
  integrity="sha256-6/VL/zgaVQLFCpqy4il6oVm6EB1Ts5fDz6XTHzJMscI="
  crossorigin="anonymous"
></script>

<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.5.1/css/fontawesome.min.css"
  integrity="sha256-jrW0TOWXGlAeWheVTEZLgKugxGBGdbVgOn9FZFmviKE="
  crossorigin="anonymous"
/>
```

</details>

---

### fonts

<details>
<summary>details</summary>

[Monaspace package](https://github.com/githubnext/monaspace/releases/latest) -
[Monaspace repo](https://github.com/githubnext/monaspace) -
[Inter package](https://fonts.google.com/specimen/Inter) -
[Inter repo](https://github.com/rsms/inter/)

```bash
# install font
wget $(curl -s https://api.github.com/repos/githubnext/monaspace/releases/latest | grep 'browser_' | cut -d\" -f4)

# copy all fonts from ./otf to ~/.local/share/fonts
cp ./fonts/otf/* ~/.local/share/fonts

# copy variable fonts from ./variable to ~/.local/share/fonts
cp ./fonts/variable/* ~/.local/share/fonts

# Build font information caches
fc-cache -f
```

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  href="https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap"
  rel="stylesheet"
/>
```

</details>

---

### favicon

<details>
<summary>details</summary>

[favicon](https://realfavicongenerator.net/svg-favicon/)
[icones](https://icones.js.org/collection/all/)

</details>

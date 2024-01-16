# frontend

The interactive K-dPS website which displays the backend information. For the simulation logic see backend.

## Project Setup

### Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

### Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

### run locally

```sh
npm install
```

Compile and Hot-Reload for Development:

```sh
npm run dev
```

Compile and Minify for Production:

```sh
npm run build
```

## Project structure
The components are divided by following structure:

1. App: The top Level component App.vue. Loads the different modules
2. Modules: The main parts of our application, namely: login, trainer & patient. Consists of different screens.
3. Screens: A container which may hold a specific set of pages and navigation or information bars. Fills either the whole screen or only the left or right half.
4. Pages: A UI container for a specific set of information or interactions. They are the main UI-holders and get loaded in by the screens when navigated to.
5. Widgets: Custom components which build basic views like buttons or lists.

Correspondingly, our component folder setup looks like this (note that 1, 2, A, B are just example names):
```
components/
├── ModuleLogin.vue
├── ModulePatient.vue
├── ModuleTrainer.vue
├── screensLogin/
│   ├── Screen1.vue
│   ├── Screen2.vue
│   ├── pages1
│   │   ├── PageA.vue
│   │   ├── PageB.vue
│   │   └── ...
│   └── pages2
│   │   └── ...
│   └── ...
├── screensPatient/
│   └── ...
├── screensTrainer/
│   └── ...
└── widgets/
    └── ...
```
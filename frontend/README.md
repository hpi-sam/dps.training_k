# Klinik-dPS Frontend
The interactive K-dPS website which displays the backend information. For the simulation logic see backend.

For general information on the project like e.g. licensing information or future plans, see the [Project README](../README.md).

## Project Setup

### Recommended IDE Setups

- [VSCode](https://code.visualstudio.com/) + [Vue](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + 
[TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).
- [WebStorm](https://www.jetbrains.com/webstorm/) (with Vue.js plugin installed)

### Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

For more information on the difference between `prod` and `dev`, see the [docs file](../docs/deployment-process.md).

### run locally without docker
Note that only the dev version supports e.g. hot-reloading.
Node needs to be v.20.5.0 or later. If your node package is too old, you can update the version with e.g. the n package for npm

Install dependencies:
```bash
npm install
```

Compile and start:
```bash
npm run <prod/dev>
```

### run with docker

Note that neither version supports hot-reloading.

```bash
docker-compose --env-file .env.<prod/dev> up --build -d
```

## Project structure
The components are divided by following structure:

1. App: The top Level component App.vue. Loads the different modules
2. Modules: The main parts of our application, namely: login, trainer & patient. Consists of different screens.
3. Screens: A container which may hold a specific set of pages and navigation or information bars. Fills either the whole screen or only the left 
   or right half.
4. Pages: A UI container for a specific set of information or interactions. They are the main UI-holders and get loaded in by the screens when 
   navigated to.
5. Widgets: Custom components which build basic views like buttons or lists.

Correspondingly, our component folder setup looks like this (note that 1, 2, A, B are just example names):
```
components/
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
├── widgets/
│   └── ...
├── ModuleLogin.vue
├── ModulePatient.vue
└── ModuleTrainer.vue
```

Moreover, the WebSocket communication with the backend is handled in the 'sockets' folder. And the 'stores' folder contains the pinia stores for 
managing the state of the application.
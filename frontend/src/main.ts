import './assets/main.css'

import {createApp} from 'vue'
import {createPinia} from 'pinia'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import App from "@/App.vue";

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.mount('#app')

app.use(Toast, {
    transition: "Vue-Toastification__bounce",
    maxToasts: 5,
    newestOnTop: true
});

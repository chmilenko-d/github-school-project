import "./assets/main.css";

import { createApp, provide, h } from "vue";
import App from "./App.vue";
import router from "./router/index.js";
import { apolloClient } from "./apollo.js";
import Button from '@/components/Button.vue'
import { DefaultApolloClient } from "@vue/apollo-composable";

const app = createApp({
  setup() {
    provide(DefaultApolloClient, apolloClient);
  },

  render: () => h(App),
});

app.component('AppButton', Button)
app.use(router);

app.mount("#app");
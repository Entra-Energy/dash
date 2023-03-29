import "bootstrap/dist/css/bootstrap.min.css"
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/index.js'
import Vue from 'vue'
import axios from 'axios'
import VueSidebarMenu from 'vue-sidebar-menu'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import VueScreen from 'vue-screen';
import 'v-calendar/dist/style.css';
import { SetupCalendar } from 'v-calendar';
import loader from "vue-ui-preloader";

import 'bootstrap/dist/css/bootstrap.css'
import VueGoogleHeatmap from 'vue-google-heatmap';
//import { createAuth0 } from '@auth0/auth0-vue';

//import Userfront from "@userfront/vue";





axios.defaults.baseURL = 'http://127.0.0.1:8000'

createApp(App).use(store).use(VueScreen,'bootstrap')
.use(router, axios)
.use(loader)
.use(VueSidebarMenu)
.use(VueGoogleHeatmap, {
    apiKey: 'AIzaSyBOCx0egD3RtmVHKdj_xWTdz0nKiL3l9lw',libraries: 'visualization'
  })
// .use(
//   createAuth0({
//     domain: "dev-obzzka3vt31mnk7g.us.auth0.com",
//     clientId: "VK4oBS3xzC9twi0n1SM5vryxeMsSXyj0",
//     authorizationParams: {
//       redirect_uri: window.location.origin,
//     }
//   })
// )
.use(SetupCalendar, {}).mount('#app')
import "bootstrap/dist/js/bootstrap.js"

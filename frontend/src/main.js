import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "@/router";
import store from "@/store";
import ArgonDashboard from "@/plugins/argon-dashboard";
import axios from "axios";
import dayjs from "dayjs"; // ES 2015
import VueSweetalert2 from 'vue-sweetalert2';



Vue.config.productionTip = false;
const token = localStorage.getItem('user-token')
if (token) {
  axios.defaults.headers.common['Authorization'] = token
}
Vue.prototype.$http = axios;
Vue.prototype.$qs =require('qs');
Object.defineProperties(Vue.prototype, {
  $date: {
    get() {
      return dayjs;
    }
  }
});
Vue.prototype.$api_url = process.env.VUE_APP_API_ENDPOINT;

const options = {
  toast: true,
  position: 'top-end',
  showConfirmButton: false,
  timer: 3000,
  timerProgressBar: true,
};
Vue.use(VueSweetalert2,options);

Vue.use(ArgonDashboard);
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");

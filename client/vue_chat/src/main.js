import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'  
import axios from 'axios'
import VueAxios from 'vue-axios'

// https://github.com/miaolz123/vue-markdown
Vue.config.productionTip = false

Vue.use(ElementUI)
Vue.use(VueAxios, axios)
                                  

axios.defaults.baseURL = "http://192.168.2.140:5000";

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

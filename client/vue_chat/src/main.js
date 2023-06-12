import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'  
import axios from 'axios'
import VueAxios from 'vue-axios'

// https://github.com/miaolz123/vue-markdown
// https://zhuanlan.zhihu.com/p/387315943
// import VueMarkdownEditor from '@kangc/v-md-editor';
// import '@kangc/v-md-editor/lib/style/base-editor.css';
// import vuepressTheme from '@kangc/v-md-editor/lib/theme/vuepress.js';
// import '@kangc/v-md-editor/lib/theme/style/vuepress.css';
// import Prism from 'prismjs';
// VueMarkdownEditor.use(vuepressTheme, {
//   Prism,
// });
// Vue.use(VueMarkdownEditor);

Vue.config.productionTip = false

Vue.use(ElementUI)
Vue.use(VueAxios, axios)
                                  

// axios.defaults.baseURL = "http://192.168.2.140:5000";
axios.defaults.baseURL = process.env.VUE_APP_BASE_API
console.log("IP: ", process.env.VUE_APP_BASE_API)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

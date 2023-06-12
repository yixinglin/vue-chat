import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ChatView from '../views/ChatView.vue'
import LoginPage from '../views/LoginPage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/chat',
    name: 'ChatBot',
    component: ChatView
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = new VueRouter({
  routes
})

let time = 1800*1000
router.beforeEach((to, from, next) => {
  let token = JSON.parse(localStorage.getItem('token'))
  if (token) {
    let newtime = new Date().getTime()
    if(newtime-token.time>time) {
      localStorage.removeItem('token')
      next('/login')
    } else {
      next()
    }
  } else {
    if (to.path=='/login') {
      next()
    } else {
      alert('请先登录，再访问其他页面')
      next('/login')
    }
  }

})

export default router

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterUser from '../views/RegisterUserFormView.vue'
import LoginUser from '../views/LoginFormView.vue'
import AddPost from '../views/AddPostFormView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path:'/register',
      name: 'Register',
      component: RegisterUser
    },
    {
      path:'/login',
      name: 'Login',
      component: LoginUser
    },
    {
      path:'/logout',
      name: 'Logout',
      component: HomeView
    },
    {
      path:'/explore',
      name: 'Explore',
      component: HomeView
    },
    {
      path:'/users/:user_id',
      name: 'User_Profile',
      component: HomeView
    },
    {
      path:'/posts/new',
      name: 'New_Post',
      component: AddPost
    },
  ]
})

export default router

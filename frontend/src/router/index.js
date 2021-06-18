import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import Settings from '../views/Settings.vue'
import Friend from '../views/Friend.vue'
import Group from '../views/Group.vue'
import Admin from '../views/Admin.vue'
import jwt_decode from "jwt-decode"

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage,
    meta: {
      allowedRoles: ['guest']
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      allowedRoles: ['guest']
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: {
      allowedRoles: ['guest']
    }
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: {
      allowedRoles: ['user', 'admin']
    }
  },
  {
    path: '/friend/:id',
    name: 'Friend',
    component: Friend,
    meta: {
      allowedRoles: ['user', 'admin']
    }
  },
  {
    path: '/group/:id',
    name: 'Group',
    component: Group,
    meta: {
      allowedRoles: ['user', 'admin']
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: {
      allowedRoles: ['user', 'admin']
    }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: {
      allowedRoles: ['admin']
    }
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.allowedRoles) {
    const allowedRoles = to.meta.allowedRoles;
    if (loggedIn()) {
      const user = jwt_decode(localStorage.getItem('websnap.user'))
      if (allowedRoles.includes(user.role)) {
        next()
      } else {
        next('/home')
      }
    } else if (allowedRoles.includes('guest')) {
      next()
    } else {
      next('/')
    }
  } else {
    console.error('Route', to, 'is missing allowedRoles attribute')
  }
});

const loggedIn = function() {
  return !!localStorage.getItem('websnap.user');
}

export default router

import Vue from 'vue';
import Router from 'vue-router';
import DashboardLayout from '@/layout/DashboardLayout';
import SiteLayout from '@/layout/SiteLayout';
import AuthLayout from '@/layout/AuthLayout';
import store from './store';

Vue.use(Router);

export default new Router({
  linkExactActiveClass: 'active',
  mode: 'history',
  routes: [
    {
      path: '/',
      redirect: 'dashboard',
      component: DashboardLayout,
      beforeEnter(to, from, next) {
        if (store.getters.isAuthenticated) {
          next();
        } else {
          store.dispatch('tryAutoLogin');
          if (store.getters.isAuthenticated) {
            next();
          } else {
            next('/login');
          }
        }
      },
      children: [
        {
          path: '/dashboard',
          name: 'dashboard',
          // route level code-splitting
          // this generates a separate chunk (about.[hash].js) for this route
          // which is lazy-loaded when the route is visited.
          component: () =>
            import(/* webpackChunkName: "demo" */ './views/Dashboard.vue'),
        },
        {
          path: '/profile',
          name: 'Profile',
          component: () =>
            import(/* webpackChunkName: "demo" */ './views/UserProfile.vue'),
        },
        {
          path: '/devices',
          name: 'devices',
          component: () =>
            import(/* webpackChunkName: "demo" */ './views/Devices.vue'),
        },
        {
          path: '/emergency_contacts',
          name: 'emergency contacts',
          component: () =>
            import(
              /* webpackChunkName: "demo" */ './views/EmergencyContacts.vue'
            ),
        },
      ],
    },
    {
      path: '/',
      redirect: 'login',
      component: AuthLayout,
      beforeEnter(to, from, next) {
        if (store.getters.isAuthenticated) {
          next('/dashboard');
        } else {
          store.dispatch('tryAutoLogin');
          if (store.getters.isAuthenticated) {
            next('/dashboard');
          } else {
            next();
          }
        }
      },
      children: [
        {
          path: '/login',
          name: 'login',
          component: () =>
            import(/* webpackChunkName: "demo" */ './views/Login.vue'),
        },
        {
          path: '/register',
          name: 'register',
          component: () =>
            import(/* webpackChunkName: "demo" */ './views/Register.vue'),
        },
      ],
    },
  ],
});

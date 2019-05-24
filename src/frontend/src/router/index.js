import Vue from 'vue';
import Router from 'vue-router';

import About from '@/pages/About';
import Contact from '@/pages/Contact';
import Course from '@/pages/Course';
import Edit from '@/pages/Edit';
import Create from '@/pages/Create';
import Dashboard from '@/pages/Dashboard';
import Settings from '@/pages/Settings';
import Add_Course from '@/pages/addCourse';
import Search from '@/pages/Search';
import Signout from '@/pages/Signout';
import SplashScreen from '@/pages/SplashScreen';
import SignUp from '@/pages/SignUp';
import store from '@/vuex';
import ErrorPage from '@/pages/ErrorPage';

Vue.use(Router);

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/welcome',
      name: 'SplashScreen',
      component: SplashScreen,
    },
    {
      path: '/signup',
      name: 'SignUp',
      component: SignUp,
    },
    {
      path: '/contact',
      name: 'Contact',
      component: Contact,
    },
    {
      path: '/about',
      name: 'About',
      component: About,
    },
    {
      path: '/',
      name: 'Dashboard',
      component: Dashboard,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/settings',
      name: 'Settings',
      component: Settings,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/addCourse',
      name: 'addCourse',
      component: Add_Course,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/signout',
      name: 'Signout',
      component: Signout,
    },
    {
      path: '/course/:id',
      name: 'Course',
      component: Course,
      props: true,
    },
    {
      path: '/edit/:id',
      name: 'Edit',
      component: Edit,
      props: true,
    },
    {
      path: '/create/',
      name: 'Create',
      component: Create,
      props: false,
    },
    {
      path: '/search/:query',
      name: 'Search',
      component: Search,
      props: true,
    },
    {
      path: '/error/',
      name: 'ErrorPage',
      component: ErrorPage,
    },
    { path: '*', redirect: '/error/' },
  ],
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.meta.requiresAuth;
  // Use the store to see if they are properly signed in
  let isAuthorized = false;
  if (store.state.auth.profile) {
    isAuthorized = store.state.auth.profile.email;
  }

  // console.log(store.state.auth.signedIn);

  if (requiresAuth && !isAuthorized) {
    // Update to store in vuex for better protection
    next('/welcome');
  } else {
    next();
  }
});

export default router;
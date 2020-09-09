// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
// import Vue from 'vue';
import Vue from 'vue';
import App from './App';
import router from './router';
import SuiVue from 'semantic-ui-vue';
import GSignInButton from 'vue-google-signin-button';
import 'semantic-ui-css/semantic.min.css';
import store from './vuex';
import { sync } from 'vuex-router-sync';

Vue.config.productionTip = false;

Vue.use(GSignInButton);
Vue.use(SuiVue);

sync(store, router);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
});

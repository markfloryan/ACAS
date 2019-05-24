import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';
import auth from './modules/Auth';
import settings from './modules/Settings';
import toast from './modules/Toast';


Vue.use(Vuex);

// Add the different modules into one place
const store = new Vuex.Store({
  modules: {
    auth,
    settings,
    toast,
  },
  plugins: [
    // Allow for the data to be saved on refresh
    createPersistedState({
      key: 'profile',
      paths: ['auth.profile']
    }),
  ],
});
export default store;

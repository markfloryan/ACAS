/*
For the Settings vue page, not the Settings vuex module
*/
import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import Settings from '@/pages/Settings';
import { Compact } from 'vue-color';
import store from '@/vuex/';
import SuiVue from 'semantic-ui-vue';
import 'semantic-ui-css/semantic.min.css';
import VueRouter from 'vue-router';

const router = new VueRouter();

import moxios from 'moxios';

const localVue = createLocalVue();
localVue.use(Vuex);
localVue.use(SuiVue);
localVue.use(VueRouter);

describe('Settings.vue', () => {
  // let wrapper;

  afterEach(() => {
    // import and pass your custom axios instance to this method
    moxios.uninstall();
  });
  // Resets the store for each test
  beforeEach(() => {
    moxios.install();
  });

  it('Settings: ', (done) => {
    
    store.commit('auth/signIn', {
      group: false,
      first_name: 'Jon',
      last_name: 'Snow',
    });

    const wrapper = mount(Settings, {
      propsData: {
      },
      store,
      router,
      localVue,
      components: {
        Compact,
      }
    });
    
    // const greeting = wrapper.find('.dashboard h2');

    // expect(greeting.text()).to.equal('Welcome back, Jon Snow');
    done();
  });
  
});

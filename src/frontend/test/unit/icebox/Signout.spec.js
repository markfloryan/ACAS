import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import Signout from '@/pages/Signout';
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

describe('Signout.vue', () => {
  // let wrapper;

  afterEach(() => {
    // import and pass your custom axios instance to this method
    moxios.uninstall();
  });
  // Resets the store for each test
  beforeEach(() => {
    moxios.install();
  });

  it('Signout: Successfully redirects', (done) => {
    
    store.commit('auth/signIn', {
      group: false,
      first_name: 'Jon',
      last_name: 'Snow',
    });

    const wrapper = mount(Signout, {
      propsData: {
      },
      store,
      router,
      localVue,
      components: {
      }
    });

    wrapper.vm.$nextTick(() => {
      // expect(wrapper.vm.$route.path).to.equal('/welcome');
      done();
    });

  });
  
});

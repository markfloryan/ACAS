import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import LoadingLayer from '@/components/LoadingLayer';
import Sidebar from '@/components/Sidebar';
import Dashboard from '@/pages/Dashboard';
import store from '@/vuex/';
import SuiVue from 'semantic-ui-vue';
import 'semantic-ui-css/semantic.min.css';
import VueRouter from 'vue-router';
// 
const router = new VueRouter();

import moxios from 'moxios';

const localVue = createLocalVue();
localVue.use(Vuex);
localVue.use(SuiVue);
localVue.use(VueRouter);

describe('Dashboard.vue', () => {
  // let wrapper;

  afterEach(() => {
    // import and pass your custom axios instance to this method
    moxios.uninstall();
  });
  // Resets the store for each test
  beforeEach(() => {
    moxios.install();
  });

  it('Dashboard: Greeting generated correctly (first and last name, not professor', (done) => {
    
    store.commit('auth/signIn', {
      group: false,
      first_name: 'Jon',
      last_name: 'Snow',
    });

    const wrapper = mount(Dashboard, {
      propsData: {
      },
      store,
      router,
      localVue,
      components: {
        LoadingLayer,
        Sidebar
      }
    });
    
    const greeting = wrapper.find('.dashboard h2');

    expect(greeting.text()).to.equal('Welcome back, Jon Snow');
    done();
  });

  it('Dashboard: Greeting generated correctly (first name, not professor', (done) => {
    
    store.commit('auth/signIn', {
      group: false,
      first_name: 'Jon',
      last_name: undefined,
    });

    const wrapper = mount(Dashboard, {
      propsData: {
      },
      store,
      router,
      localVue,
      components: {
        LoadingLayer,
        Sidebar
      }
    });

    const greeting = wrapper.find('.dashboard h2');

    expect(greeting.text()).to.equal('Welcome back, Jon');
    done();
  });

  it('Dashboard: Greeting generated correctly (last name, not professor', (done) => {
    
    store.commit('auth/signIn', {
      group: false,
      first_name: undefined,
      last_name: 'Snow',
    });

    const wrapper = mount(Dashboard, {
      propsData: {
      },
      store,
      router,
      localVue,
      components: {
        LoadingLayer,
        Sidebar
      }
    });

    const greeting = wrapper.find('.dashboard h2');

    expect(greeting.text()).to.equal('Welcome back, Snow');
    done();
  });

  it('Dashboard: Greeting generated correctly (no name, not professor', (done) => {
    
    store.commit('auth/signIn', {
      group: false,
      first_name: undefined,
      last_name: undefined,
    });

    const wrapper = mount(Dashboard, {
      propsData: {
      },
      store,
      router,
      localVue,
      components: {
        LoadingLayer,
        Sidebar
      }
    });

    const greeting = wrapper.find('.dashboard h2');

    expect(greeting.text()).to.equal('Welcome back!');
    done();
  });

  it('Dashboard: ', (done) => {
    
    store.commit('auth/signIn', {
      group: true,
      first_name: undefined,
      last_name: undefined,
    });

    const wrapper = mount(Dashboard, {
      propsData: {
      },
      store,
      router,
      localVue,
      components: {
        LoadingLayer,
        Sidebar
      }
    });
    
    wrapper.vm.$nextTick(() => {
      const createClassButton = wrapper.find('.to-create-class-link');
      createClassButton.trigger('click');
      
      expect(wrapper.vm.$route.path).to.equal('/create');
      done();
    });

  });
  
});

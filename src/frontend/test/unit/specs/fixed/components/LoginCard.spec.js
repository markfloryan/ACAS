import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import LoadingLayer from '@/components/LoadingLayer';
import Sidebar from '@/components/Sidebar';
import SignUp from '@/pages/SignUp';
import SplashScreen from '@/pages/SplashScreen';
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

describe('SignUp.vue', () => {
  // let wrapper;

  afterEach(() => {
    // import and pass your custom axios instance to this method
    moxios.uninstall();
  });
  // Resets the store for each test
  beforeEach(() => {
    moxios.install();
  });

  it('Sign Up: Sign up screen appears', (done) => {

    /*store.commit('auth/signIn', {
      group: false,
      first_name: 'Jon',
      last_name: 'Snow',
    });*/

    const wrapper = mount(SignUp, {
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

    const greeting = wrapper.find('.message p:nth-child(2)');

    expect(greeting.text()).to.equal('Sign up with google below');
    done();
  });
  it('Sign In: Sign in screen appears', (done) => {

    /*store.commit('auth/signIn', {
      group: false,
      first_name: 'Jon',
      last_name: 'Snow',
    });*/

    const wrapper = mount(SplashScreen, {
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

    const greeting = wrapper.find('.message p:nth-child(2)');

    expect(greeting.text()).to.equal('Sign in with google below');
    done();
  });
  it('Sign In Switch to Sign Up button test', (done) => {

    const wrapper = mount(SignUp, {
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

    const greeting = wrapper.find('.center-signin a');
    greeting.trigger('click');
    expect(wrapper.vm.$route.path).to.equal('/welcome');
    done();
  });
  it('Sign Up Switch to Sign In button test', (done) => {

    const wrapper = mount(SplashScreen, {
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

    const greeting = wrapper.find('.center-signup a');
    greeting.trigger('click');
    expect(wrapper.vm.$route.path).to.equal('/signup');
    done();
  });
  


});

import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import LoadingLayer from '@/components/LoadingLayer';
import Sidebar from '@/components/';
import TopicModal from '@/components/TopicModal';
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

  it('TopicModal: ', (done) => {
    
    // store.commit('auth/signIn', {
    //   group: false,
    //   first_name: 'Jon',
    //   last_name: 'Snow',
    // });

    const wrapper = mount(TopicModal, {
      propsData: {
        isOpen: true,
      },
      store,
      router,
      localVue,
      components: {
        LoadingLayer,
        Sidebar
      }
    });
    console.log(wrapper.html());
    
    // const greeting = wrapper.find('.dashboard h2');

    // expect(greeting.text()).to.equal('Welcome back, Jon Snow');
    done();
  });
  
});

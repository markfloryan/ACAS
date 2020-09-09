import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import LoadingLayer from '@/components/LoadingLayer';
import Sidebar from '@/components/Sidebar';
import Course from '@/pages/Course';
import AddStudentsToCourse from '@/components/AddStudentsToCourse';
import ClassGraph from '@/components/ClassGraph';
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

describe('Course.vue', () => {
  // let wrapper;

  afterEach(() => {
    // import and pass your custom axios instance to this method
    moxios.uninstall();
  });
  // Resets the store for each test
  beforeEach(() => {
    moxios.install();
  });

  it('ClassGraph: exists', (done) => {
    
    store.commit('auth/signIn', {
      group: false,
      first_name: 'Jon',
      last_name: 'Snow',
    });

    const wrapper = mount(Course, {
      propsData: {
      },
      store,
      router,
      localVue,
      components: {
        LoadingLayer,
        Sidebar,
        ClassGraph,
        AddStudentsToCourse,
      }
    });

    const greeting = wrapper.find('.class-graph');
    expect(greeting.exists()).to.equal(true);
    done();
  });

  
});

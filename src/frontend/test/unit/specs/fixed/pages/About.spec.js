// As of 2/3/19, testing this file adds nothing to coverage
import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import About from '@/pages/About';
import toastStore from '@/vuex/modules/Toast';
import settingsStore from '@/vuex/modules/Settings';
import SuiVue from 'semantic-ui-vue';
import 'semantic-ui-css/semantic.min.css';

import moxios from 'moxios';

const localVue = createLocalVue();
localVue.use(Vuex);
localVue.use(SuiVue);

describe('About.vue', () => {
  let store;
  let wrapper;

  afterEach(() => {
    // import and pass your custom axios instance to this method
    moxios.uninstall();
  });
  // Resets the store for each test
  beforeEach(() => {
    moxios.install();
    store = new Vuex.Store({
      modules: {
        toast: toastStore,
        settings: settingsStore
      },
    });
    wrapper = mount(About, {
      propsData: {
      },
      store,
      localVue,
      components: {
      }
    });
  });

  it('About: Mounts properly', () => {
    const title = wrapper.find('h2');
    expect(title.text()).to.equal('About SPT');
  });

});

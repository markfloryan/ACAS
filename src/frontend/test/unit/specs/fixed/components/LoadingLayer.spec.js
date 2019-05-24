import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import LoadingLayer from '@/components/LoadingLayer';
import SuiVue from 'semantic-ui-vue';
import 'semantic-ui-css/semantic.min.css';

const localVue = createLocalVue();

localVue.use(Vuex);
localVue.use(SuiVue);

describe('LoadingLayer.vue', () => {
  let store;

  // Resets the store for each test
  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
      },
      components: {
      }
    });
  });

  // First Unit test
  it('User should see the loading icon', () => {
    const wrapper = mount(LoadingLayer, { store, localVue });
    const loadingIcon = wrapper.find('.loading-icon');
    expect(loadingIcon.exists()).to.equal(true);
  });

  // Second Unit test
  it('User should see the default loading text', () => {
    const wrapper = mount(LoadingLayer, { store, localVue });
    const message = wrapper.find('.message');
    expect(message.text()).to.equal('Loading...');
  });
  
});

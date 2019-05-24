import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import Resources from '@/components/Resources';
import LoadingLayer from '@/components/LoadingLayer';
import { API_URL } from '@/constants';
import toastStore from '@/vuex/modules/Toast';
import settingsStore from '@/vuex/modules/Settings';
import SuiVue from 'semantic-ui-vue';
import 'semantic-ui-css/semantic.min.css';

import moxios from 'moxios';

const localVue = createLocalVue();
localVue.use(Vuex);
localVue.use(SuiVue);

const resources = [
  {pk: 2, name: 'myspace website', link: 'https://www.myspace.com', topic: 1},
  {pk: 1, name: 'facebook', link: 'https://www.facebook.com', topic: 1}
];
const topicId = 1;

describe('Resources.vue', () => {
  let store;
  let wrapper;

  afterEach(() => {
    // import and pass your custom axios instance to this method
    moxios.uninstall();
  });
  // Resets the store for each test
  beforeEach((done) => {
    moxios.install();

    store = new Vuex.Store({
      modules: {
        toast: toastStore,
        settings: settingsStore
      },
    });
    wrapper = mount(Resources, {
      propsData: {
        topicId,
        data: {
          topic: {
            id: 1,
            name: 'A',
            course: 1,
          }
        }
      },
      store,
      localVue,
      components: {
        LoadingLayer,
      }
    });
    
    // when the app requests axios.get(`${API_URL}/resources/${this.topicId}`) in mounted()
    moxios.wait(() => {
      const initialRetrieveResourceRequest = moxios.requests.mostRecent();
      
      initialRetrieveResourceRequest.respondWith({
        status: 200,
        response: {
          result: resources,
        },
      }).then(() => {
        done();
      });

    });
  });

  it('Resources: Expect resources to be mounted properly', () => {
    expect(wrapper.vm.resources).to.equal(resources);
  });

  it('Resources: Remove a resource', (done) => {

    const removeResourceButton = wrapper.find('td button');
    removeResourceButton.trigger('click');

    // Elsewhere in your code axios.get('/users/search', { params: { q: 'flintstone' } }) is called
    moxios.wait(() => {
      let deleteResourceRequest = moxios.requests.mostRecent();
      deleteResourceRequest.respondWith({
        status: 200,
        response: {},
      }).finally(() => {
        let toastState = store.state.toast;

        expect(toastState.visible).to.equal(true);
        expect(toastState.type).to.equal('success');
        done();
      });
    });
    
  });

  it('Resources: Remove a resource (server error)', (done) => {

    const removeResourceButton = wrapper.find('td button');
    removeResourceButton.trigger('click');

    // Elsewhere in your code axios.get('/users/search', { params: { q: 'flintstone' } }) is called
    moxios.wait(() => {
      let deleteResourceRequest = moxios.requests.mostRecent();
      deleteResourceRequest.respondWith({
        status: 500,
        response: {},
      }).finally(() => {
        let toastState = store.state.toast;

        expect(toastState.visible).to.equal(true);
        expect(toastState.type).to.equal('error');
        done();
      });
    });
    
  });

  it('Resources: Add a resource (fields are valid)', (done) => {

    wrapper.vm.newResource.name = 'google';
    wrapper.vm.newResource.link = 'google.com';

    const addResourceButton = wrapper.find('.btn-create');
    addResourceButton.trigger('click');

    // When the app requests axios.post(`${API_URL}/resources/`, resourceData)
    moxios.wait(() => {
      const addResourceRequest = moxios.requests.mostRecent();

      addResourceRequest.respondWith({
        status: 200,
        response: {},
      }).then(() => {
        let toastState = store.state.toast;

        expect(toastState.visible).to.equal(true);
        expect(toastState.type).to.equal('success');
        done();
      });

    });
  });

  it('Resources: Add a resource (fields are invalid)', (done) => {
    wrapper.vm.newResource.name = '';
    wrapper.vm.newResource.link = 'google.com';

    const addResourceButton = wrapper.find('.btn-create');
    addResourceButton.trigger('click');

    // When the app requests axios.post(`${API_URL}/resources/`, resourceData)
    moxios.wait(() => {
      const addResourceRequest = moxios.requests.mostRecent();

      addResourceRequest.respondWith({
        status: 200,
        response: {},
      }).then(() => {
        let toastState = store.state.toast;

        expect(toastState.visible).to.equal(true);
        expect(toastState.type).to.equal('error');
        done();
      });

    });
  });

  it('Resources: Add a resource (server error)', (done) => {

    wrapper.vm.newResource.name = 'google';
    wrapper.vm.newResource.link = 'google.com';

    const addResourceButton = wrapper.find('.btn-create');
    addResourceButton.trigger('click');

    // When the app requests axios.post(`${API_URL}/resources/`, resourceData)
    moxios.wait(() => {
      const addResourceRequest = moxios.requests.mostRecent();

      addResourceRequest.respondWith({
        status: 500,
        response: {},
      }).then(() => {
        let toastState = store.state.toast;

        expect(toastState.visible).to.equal(true);
        expect(toastState.type).to.equal('error');
        done();
      });

    });
  });

});

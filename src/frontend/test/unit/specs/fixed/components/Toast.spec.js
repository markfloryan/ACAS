import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import Vue from 'vue';
import store from '@/vuex/';
import Toast from '@/components/Toast';
import toastStore from '@/vuex/modules/Toast';
import SuiVue from 'semantic-ui-vue';
import 'semantic-ui-css/semantic.min.css';

const { openToast, closeToast, setToastInfo } = toastStore.mutations;
const localVue = createLocalVue();

localVue.use(Vuex);
localVue.use(SuiVue);

describe('Toast.vue', () => {
  // let store;

  // Resets the store for each test
  beforeEach(() => {
    // store = new Vuex.Store({
    //   modules: {
    //     toast: toastStore,
    //   },
    // });
  });

  // Atomic vuex tests
  it('Toast vuex (atomic): openToast', () => {
    let toastState = store.state.toast;

    // Make sure toast is not visible before opening, to make sure something actually happens
    toastState.visible = false;

    openToast(toastState);
    expect(toastState.visible).to.equal(true);
  });

  it('Toast vuex (atomic): closeToast', () => {
    let toastState = store.state.toast;

    // Make sure toast is visible before closing, to make sure something actually happens
    toastState.visible = true;

    closeToast(toastState);
    expect(toastState.visible).to.equal(false);
  });

  it('Toast vuex (atomic): setToastInfo', () => {
    let toastState = store.state.toast;

    setToastInfo(toastState, {
      message: 'Hello',
      title: 'Success!',
      type: 'success',
    });

    expect(toastState.message).to.equal('Hello');
    expect(toastState.title).to.equal('Success!');
    expect(toastState.type).to.equal('success');
  });

  it('Toast vuex (atomic): setToastInfo, invalid values', () => {
    let toastState = store.state.toast;

    setToastInfo(toastState, {
      message: 'Hello',
      type: 'success1212111',
    });

    expect(toastState.message).to.equal('Hello');
    expect(toastState.title).to.equal('');
    expect(toastState.type).to.equal('info');
  });

  // Test vuex interacting with markup
  it('Toast: Check that toast info is mounting into markup', () => {
    openToast(store.state.toast);
    setToastInfo(store.state.toast, {
      message: 'Hello',
      title: 'Success!',
      type: 'success',
    });

    const wrapper = mount(Toast, { store, localVue });

    const h3 = wrapper.find('h3');
    const p = wrapper.find('p');

    expect(h3.text()).to.equal('Success!');
    expect(p.text()).to.equal('Hello');
  });

  it('Toast: Clicking the close button triggers closeToast', () => {
    openToast(store.state.toast);
    setToastInfo(store.state.toast, {
      message: 'Hello',
      title: 'Success!',
      type: 'success',
    });

    const wrapper = mount(Toast, { store, localVue });

    const button = wrapper.find('i');
    button.trigger('click');
    expect(store.state.toast.visible).to.equal(false);
  });

  // it('Instance can be run', () => {
  //   const Constructor = Vue.extend(Toast);
  //   const vm = new Constructor().$mount();
  //   Vue.nextTick(() =>{
  //     expect(vm.$el.exists()).to.equal(true);
  //     done();
  //   });

  // });
});

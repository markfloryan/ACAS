
import { toastTypes } from '@/constants/';

const state = {
  message: '',
  title: '',
  type: 'info', // type can be 'success', 'error', or 'info'
  visible: false,
  duration: 3000,
};

const actions = {};

const mutations = {
  openToast(state) {
    state.visible = true;
  },
  closeToast(state) {
    state.visible = false;
  },
  setToastInfo(state, newToastinfo) { // Updates toast info and uses defaults for values not provided
    // Co-erce falsey values to default values
    state.message = newToastinfo.message ? newToastinfo.message : '';
    state.title = newToastinfo.title ? newToastinfo.title : '';
    state.duration = Number.isInteger(newToastinfo.duration) ? newToastinfo.duration : 3000;

    if (toastTypes.includes(newToastinfo.type)) {
      state.type = newToastinfo.type;
    } else {
      state.type = 'info';
    }
  },
};

const getters = {};

export default {
  namespaced: true,
  state,
  actions,
  mutations,
  getters
};
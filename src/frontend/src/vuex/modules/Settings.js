//import Vue from 'vue'
//import Vuex from 'vuex'
//Vue.use(Vuex);
// import api from '../../api';
const initialState = {
  color: '#FFF',
  nickname:'student',
  fontSize:8,
  id:null
};
const trueInitialState = {
  color: '#FFF',
  nickname:'student',
  fontSize:8,
  id:null
};
const getters={
  returnColor: (state) => {
    return state.color;
  },
  returnNickName: (state) => {
    
    return state.nickname;
  },
  returnFontSize: (state) => {
    return state.fontSize;
  },
  //makes sure that the text on colored buttons is always readable 
  returnPrimaryButtonStyle: (state) => { // Used to update each primary action button to reflect the user's preferences
    
    let computedState = {
      backgroundColor: state.color,
      'margin-left': '8pt',
    };
    if (state.color === '#FFF' || state.color === '#FFFFFF') {
      computedState.backgroundColor = 'var(--color-blue)';
    }

    return computedState;
  },
  returnExternalPrimaryButtonStyle: (state) => {
    
    let externalColor = {
      backgroundColor: state.color,
    };
    if (state.color === '#FFF' || state.color === '#FFFFFF') {
      externalColor.backgroundColor = 'var(--color-blue)';
    }

    return externalColor;
  },
};
const mutations= {
  //all the setters for color/font/nickname
  colorChange (state, colorstuff){
    state.color=colorstuff;
  },
  nicknameChange (state, name){
    state.nickname=name;
  },
  fontChange (state,size){
    state.fontSize=size;
  },
  //resets settings to factory default
  resetSettingsStore(state) {
    // acquire initial state
    const s = trueInitialState;
    
    Object.keys(s).forEach(key => {
      state[key] = s[key];
    });
  }
};
export default {
  namespaced : true,
  state: initialState, 
  mutations,
  getters,
  trueInitialState,
};
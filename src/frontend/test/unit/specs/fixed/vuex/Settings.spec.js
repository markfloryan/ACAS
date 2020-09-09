import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import Settings from '@/pages/Settings';
import { Compact } from 'vue-color';
import store from '@/vuex/';
import settingsStore from '@/vuex/modules/Settings';
import SuiVue from 'semantic-ui-vue';
import 'semantic-ui-css/semantic.min.css';
import VueRouter from 'vue-router';
const { returnColor, returnNickName, returnFontSize, returnPrimaryButtonStyle, returnExternalPrimaryButtonStyle } = settingsStore.getters;
const { colorChange, nicknameChange, fontChange, resetSettingsStore } = settingsStore.mutations;
const trueInitialState = settingsStore.trueInitialState;
const router = new VueRouter();

import moxios from 'moxios';

const localVue = createLocalVue();
localVue.use(Vuex);
localVue.use(SuiVue);
localVue.use(VueRouter);

describe('Vuex Settings.js', () => {
  // let wrapper;

  afterEach(() => {
    // import and pass your custom axios instance to this method
    moxios.uninstall();
  });
  // Resets the store for each test
  beforeEach(() => {
    moxios.install();
  });

  it('Settings vuex (atomic): Set chosen color', (done) => {
    let settingsState = store.state.settings;

    colorChange(settingsState, '#00FF00');
    
    expect(settingsState.color).to.equal('#00FF00');
    done();
  });

  it('Settings vuex (atomic): Return chosen color', (done) => {
    let settingsState = store.state.settings;

    settingsState.color = '#00FF00';
    
    expect(returnColor(settingsState)).to.equal('#00FF00');
    done();
  });

  it('Settings vuex (atomic): Set nickname', (done) => {
    let settingsState = store.state.settings;

    nicknameChange(settingsState, 'Jon Snow');
    
    expect(settingsState.nickname).to.equal('Jon Snow');
    done();
  });

  it('Settings vuex (atomic): Return nickname', (done) => {
    let settingsState = store.state.settings;

    settingsState.nickname = 'Jon Snow';
    
    expect(returnNickName(settingsState)).to.equal('Jon Snow');
    done();
  });

  it('Settings vuex (atomic): Set font size', (done) => {
    let settingsState = store.state.settings;

    fontChange(settingsState, 12);
    
    expect(settingsState.fontSize).to.equal(12);
    done();
  });

  it('Settings vuex (atomic): Return font size', (done) => {
    let settingsState = store.state.settings;

    settingsState.fontSize = 12;
    
    expect(returnFontSize(settingsState)).to.equal(12);
    done();
  });

  it('Settings vuex (atomic): Wipe settings store', (done) => {
    let settingsState = store.state.settings;

    settingsState.fontSize = 123;
    settingsState.nickname = 'Jon Snow';
    settingsState.color = '#00FF00';
    
    resetSettingsStore(settingsState);

    expect(settingsState.fontSize).to.equal(trueInitialState.fontSize);
    expect(settingsState.nickname).to.equal(trueInitialState.nickname);
    expect(settingsState.color).to.equal(trueInitialState.color);
    done();
  });

  it('Settings vuex (atomic): Return primary button style (non-white favorite color)', (done) => {
    let settingsState = store.state.settings;

    settingsState.color = '#00FF00';

    const expectedButtonStyle = {
      backgroundColor: '#00FF00',
    };

    const buttonStyle = returnPrimaryButtonStyle(settingsState);

    expect(buttonStyle.backgroundColor).to.equal(expectedButtonStyle.backgroundColor);
    done();
  });

  it('Settings vuex (atomic): Return primary button style (white is favorite color)', (done) => {
    let settingsState = store.state.settings;

    settingsState.color = '#FFFFFF';

    const buttonStyle = returnPrimaryButtonStyle(settingsState);

    expect(buttonStyle.backgroundColor).to.equal('var(--color-blue)');
    done();
  });

  it('Settings vuex (atomic): Return external primary button style (non-white favorite color)', (done) => {
    let settingsState = store.state.settings;

    settingsState.color = '#00FF00';

    const expectedButtonStyle = {
      backgroundColor: '#00FF00',
    };

    const buttonStyle = returnExternalPrimaryButtonStyle(settingsState);

    expect(buttonStyle.backgroundColor).to.equal(expectedButtonStyle.backgroundColor);
    done();
  });

  it('Settings vuex (atomic): Return external primary button style (white is favorite color)', (done) => {
    let settingsState = store.state.settings;

    settingsState.color = '#FFFFFF';

    const buttonStyle = returnExternalPrimaryButtonStyle(settingsState);

    expect(buttonStyle.backgroundColor).to.equal('var(--color-blue)');
    done();
  });

});

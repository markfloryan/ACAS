import Vue from 'vue';
import Settings from '@/pages/Settings';

describe('Settings.vue', () => {
  // First Unit test
  it('Does settings data exist', () => {
    const Constructor = Vue.extend(Settings);
    const vm = new Constructor().$mount();
    Vue.nextTick(() =>{
      expect(vm.$el.data().exists()).to.equal(true);
      done();
    });

  });
  //expect(vm.$el.querySelector('.message p').textContent).to.equal('Hello');
  it('Instance can be run', () => {
    const Constructor = Vue.extend(Settings);
    const vm = new Constructor().$mount();
    Vue.nextTick(() =>{
      expect(vm.$el.exists()).to.equal(true);
      done();
    });

  });

  it('Does color get created', () => {
    const Constructor = Vue.extend(Settings);
    const vm = new Constructor().$mount();
    Vue.nextTick(() =>{
      expect(vm.$el.data().colors.exists()).to.equal(true);
      done();
    });
  });
  it('Is initial color equal to #FFFFFF', () => {
    const Constructor = Vue.extend(Settings);
    const vm = new Constructor().$mount();
    Vue.nextTick(() =>{
      expect(vm.$el.data().colors).to.equal('#FFFFFF');
      done();
    });
  });


  it('Does function to change color exist', () => {
    const Constructor = Vue.extend(Settings);
    const vm = new Constructor().$mount();
    Vue.nextTick(() =>{
      expect(vm.$el.updateColor().exists()).to.equal(true);
      done();
    });
  });

  if('Does color picker exist', () => {
    const Constructor = Vue.extend(Settings);
    const vm = new Constructor().$mount();
    Vue.nextTick(() =>{
      expect(vm.$el.querySelector('.vc-compact-color-item').exists()).to.equal(
        true
      );
      expect(vm.$el.updateColor().exists()).to.equal(true);
      done();
    });
  });
});

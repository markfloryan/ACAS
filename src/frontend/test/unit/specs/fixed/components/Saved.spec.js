import Vue from 'vue';
import Saved from '@/components/Saved';


describe('Saved.vue', () => {
  //Sprint9 unit test 4
  it('Data table exists', () => {
    const Constructor = Vue.extend(Saved);
    const vm = new Constructor().$mount();
    Vue.nextTick(() => {
      expect(vm.$el.data().exists()).to.equal(true);
      done();
    });
  });
  //Sprint9 unit test 5
  it('Instance can be run', () => {
    const Constructor = Vue.extend(Saved);
    const vm = new Constructor().$mount();
    Vue.nextTick(() =>{
      expect(vm.$el.exists()).to.equal(true);
      done();
    });
  });
  // it('Saved Message exists', () => {
  //   const Constructor = Vue.extend(Saved);
  //   const vm = new Constructor().$mount();
  //   expect(vm.$el.querySelector('.content h1').textContent).to.equal('*Saved*');
  // });
});
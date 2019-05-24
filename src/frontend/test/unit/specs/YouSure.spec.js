import Vue from 'vue';
import YouSure from '@/components/YouSure';


describe('YouSure.vue', () => {
  //Sprint7 unit test 4
  it('Data table exists', () => {
    const Constructor = Vue.extend(YouSure);
    const vm = new Constructor().$mount();
    Vue.nextTick(() => {
      expect(vm.$el.data().exists()).to.equal(true);
      done();
    });
  });
  //Sprint7 unit test 5
  it('Instance can be run', () => {
    const Constructor = Vue.extend(YouSure);
    const vm = new Constructor().$mount();
    Vue.nextTick(() =>{
      expect(vm.$el.exists()).to.equal(true);
      done();
    });
  });
});
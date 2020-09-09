import Vue from 'vue';
import Create from '@/pages/Create';

describe('Create.vue', () => {
  // 5-1
  it('Correct Name Title', () => {
    const Constructor = Vue.extend(Create);
    const vm = new Constructor().$mount();
    Vue.nextTick(() => {
      expect(vm.$el.querySelector('.course-name').textContent).to.equal('Course Name: ');
      done();
    });
  });

  // 5-2
  it('Correct Subject Title', () => {
    const Constructor = Vue.extend(Create);
    const vm = new Constructor().$mount();
    Vue.nextTick(() => {
      expect(vm.$el.querySelector('.course-subject').textContent).to.equal('Department Code: ');
      done();
    });
  });
  // 5-3
  it('Correct Code Title', () => {
    const Constructor = Vue.extend(Create);
    const vm = new Constructor().$mount();
    Vue.nextTick(() => {
      expect(vm.$el.querySelector('.course-code').textContent).to.equal('Course Code: ');
      done();
    });
  });
  // 5-4
  it('Correct Cancel Button Title', () => {
    const Constructor = Vue.extend(Create);
    const vm = new Constructor().$mount();
    Vue.nextTick(() => {
      expect(vm.$el.querySelector('cancel-btn').textContent).to.equal('Cancel');
      done();
    });
  });
  //5-5
  it('Correct Create Button Title', () => {
    const Constructor = Vue.extend(Create);
    const vm = new Constructor().$mount();
    Vue.nextTick(() => {
      expect(vm.$el.querySelector('create-btn').textContent).to.equal('Create');
      done();
    });
  });
});

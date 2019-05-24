import Vue from 'vue';
import EditPopup from '@/components/EditPopup';

describe('EditPopup.vue', () => {
  // 2
  it('Correct Name Title', () => {
    const Constructor = Vue.extend(EditPopup);
    const vm = new Constructor().$mount();
    Vue.nextTick(() => {
      expect(vm.$el.querySelector('.topic-name').textContent).to.equal('Topic Name');
      done();
    });
  });

  // 3
  it('Correct ID Title', () => {
    const Constructor = Vue.extend(EditPopup);
    const vm = new Constructor().$mount();
    Vue.nextTick(() => {
      expect(vm.$el.querySelector('.topic-id').textContent).to.equal('Topic ID');
      done();
    });
  });
  // 4
  it('Correct ID Title', () => {
    const Constructor = Vue.extend(EditPopup);
    const vm = new Constructor().$mount();
    Vue.nextTick(() => {
      expect(vm.$el.querySelector('create-btn').textContent).to.equal('create');
      done();
    });
  });
  // 5
  it('Correct ID Title', () => {
    const Constructor = Vue.extend(EditPopup);
    const vm = new Constructor().$mount();
    Vue.nextTick(() => {
      expect(vm.$el.querySelector('cancel-btn').textContent).to.equal('cancel');
      done();
    });
  });
});

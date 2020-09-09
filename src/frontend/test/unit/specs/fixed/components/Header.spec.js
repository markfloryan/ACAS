import Vue from 'vue';
import Header from '@/components/Header';

describe('Header.vue', () => {
  // Second Unit test
  it('User should see the login button', () => {
    const Constructor = Vue.extend(Header);
    const vm = new Constructor().$mount();
    Vue.nextTick(() => {
      expect(vm.$el.querySelector('.login').textContent).to.equal('Login');
      done();
    });
  });

  // Third Unit test
  it('User should see the about button', () => {
    const Constructor = Vue.extend(Header);
    const vm = new Constructor().$mount();
    Vue.nextTick(() => {
      expect(vm.$el.querySelector('.about').textContent).to.equal('About');
      done();
    });
  });

  // Fourth Unit test
  it('User should see the Contact us button', () => {
    const Constructor = Vue.extend(Header);
    const vm = new Constructor().$mount();
    Vue.nextTick(() => {
      expect(vm.$el.querySelector('.contact-us').textContent).to.equal('Contact Us');
      done();
    });
  });
});

// import { mount, createLocalVue } from '@vue/test-utils';
// import moxios from 'moxios';
// import axios from 'axios';
// import sinon from 'sinon';
// import Vuex from 'vuex';
// import Vue from 'vue';
// import Quiz from '@/components/quiz/Quiz';
// import { API_URL } from '@/constants';
// import SuiVue from 'semantic-ui-vue';
// import 'semantic-ui-css/semantic.min.css';

// const localVue = createLocalVue();

// localVue.use(Vuex);
// localVue.use(SuiVue);

// describe('Quiz.vue', () => {
//   beforeEach(function () {
//     // import and pass your custom axios instance to this method
//     moxios.install();
//   });

//   afterEach(function () {
//     // import and pass your custom axios instance to this method
//     moxios.uninstall();
//   });
//   // Resets the store for each test
//   // Test markup
//   it('Quiz: Test data', () => {
//     const Constructor = Vue.extend(Quiz);
//     const vm = new Constructor({
//       propsData: {
//         topicId: 6,
//       },
//     }).$mount();
//     // const wrapper = mount(Quiz, {
//     //   localVue,
//     //   propsData: {
//     //     topicId: 6,
//     //   },
//     // });

//     moxios.stubRequest(`${API_URL}/quiz/6`, {
//       status: 200,
//       response: {
//         status: '200 - OK',
//         result: {
//           pk: 1,
//           name: 'Quiz for arrays',
//           topic: {},
//           questions: [
//             {
//               pk: 2,
//               text: 'The array: [\'1\', \'hello\', \'world\'] has length: [a] and last index: [b]',
//               question_type: 0,
//               total_points: 1,
//               index: 2,
//               answers: [
//                 {
//                   pk: 8,
//                   text: '[a]: 2, [b]: 2',
//                   index: 1
//                 },
//                 {
//                   pk: 7,
//                   text: '[a]: 3, [b]: 2',
//                   index: 1
//                 },
//                 {
//                   pk: 6,
//                   text: '[a]: 3, [b]: 3',
//                   index: 1
//                 }
//               ]
//             },
//             {
//               pk: 1,
//               text: 'Arrays start at what index?',
//               question_type: 0,
//               total_points: 1,
//               index: 1,
//               answers: [
//                 {
//                   pk: 5,
//                   text: '-7',
//                   index: 1
//                 },
//                 {
//                   pk: 2,
//                   text: '1',
//                   index: 1
//                 },
//                 {
//                   pk: 1,
//                   text: '0',
//                   index: 1
//                 }
//               ]
//             }
//           ]
//         }
//       }
//     });

//     let onFulfilled = sinon.spy();
//     axios.get(`${API_URL}/quiz/6`).then(onFulfilled);
//     // console.log(vm.html());
//     moxios.wait(function () {
//       // console.log('TESTIN');
//       // const h1 = vm.find('h1');
//       // console.log(vm.html());
//       // expect(h1.text()).to.equal('No Quiz for this topic yet');
//       expect(vm.$el.querySelector('h1').textContent).to.equal(
//         'No Quiz for this topic yet'
//       );
//       // done();
//     });

//   });

//   // Test markup
//   it('Quiz: Test for nonexistent quiz', () => {

//     const Constructor = Vue.extend(Quiz);
//     const vm = new Constructor({
//       propsData: {
//         topicId: 8,
//       },
//     }).$mount();
//     // const wrapper = mount(Quiz, {
//     //   localVue,
//     //   propsData: {
//     //     topicId: 8,
//     //   },
//     // });

//     moxios.stubRequest(`${API_URL}/quiz/8`, {
//       status: 200,
//       response: {
//         status: '404 - Not Found',
//         result: 'Object with given id does not exist',
//       }
//     });

//     let onFulfilled = sinon.spy();
//     axios.get(`${API_URL}/quiz/8`).then(onFulfilled);

//     moxios.wait(function () {

//       expect(vm.$el.querySelector('h1').textContent).to.equal(
//         'No Quiz for this topic yet'
//       );

//       // const h1 = wrapper.find('h1');
//       // expect(h1.text()).to.equal('No Quiz for this topic yet');
//       // done();
//     });

//   });
// });

// // const Constructor = Vue.extend(Quiz);
// // const vm = new Constructor({
// //   propsData: {
// //     topicId: 6, // No topic will have ID -1 so this will always not find a quiz
// //   }
// // }).$mount();
// // console.log('A');
// // expect(true).to.equal(true);
// // console.log('B');
// // Vue.nextTick(() => {
// //   console.log('C');
// //   console.log('HEAREEREELLLLLLOOOO');
// //   expect(false).to.equal(true);

// // });
// // console.log('D');

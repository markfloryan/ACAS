// import { mount, createLocalVue } from '@vue/test-utils';
// import Vuex from 'vuex';
// import Sidebar from '@/components/Sidebar';
// import LoadingLayer from '@/components/LoadingLayer';
// import { API_URL } from '@/constants';
// import toastStore from '@/vuex/modules/Toast';
// import settingsStore from '@/vuex/modules/Settings';
// import SuiVue from 'semantic-ui-vue';
// import 'semantic-ui-css/semantic.min.css';
// import VueRouter from 'vue-router';

// const router = new VueRouter();

// import moxios from 'moxios';

// const localVue = createLocalVue();
// localVue.use(Vuex);
// localVue.use(SuiVue);
// localVue.use(VueRouter);

// describe('Sidebar.vue', () => {
//   let store;
//   let wrapper;

//   afterEach(() => {
//     // import and pass your custom axios instance to this method
//     moxios.uninstall();
//   });
//   // Resets the store for each test
//   beforeEach((done) => {
//     moxios.install();
//     localStorage.setItem('profile', '{"auth":{"profile":{"first_name":"Jon","last_name":"Snow","email":"jsnow@virginia.edu","id_token":"afsdafsdf","group":true}}}');
//     store = new Vuex.Store({
//       modules: {
//         toast: toastStore,
//         settings: settingsStore
//       },
//     });
//     wrapper = mount(Sidebar, {
//       propsData: {
//         role: 'Student',
//       },
//       store,
//       router,
//       localVue,
//       components: {
//         LoadingLayer,
//       }
//     });

//     // Elsewhere in your code axios.get('/users/search', { params: { q: 'flintstone' } }) is called
//     moxios.wait(() => {
//       let request = moxios.requests.mostRecent();
//       request.respondWith({
//         status: 200,
//         response: {
//           result: [{
//             'pk':1,
//             'student': {
//               'id':1,
//               'password':'',
//               'last_login':null,
//               'is_superuser':false,
//               'is_staff':false,
//               'is_active':true,
//               'date_joined':'2019-02-02T16:50:01.478074Z',
//               'first_name':'Jon',
//               'last_name':'Snow',
//               'email':'js@virginia.edu',
//               'join_date':'2019-02-02T16:50:01.478410Z',
//               'id_token':'dsfasdfas',
//               'is_professor':true,
//               'username':null,
//               'groups':[],
//               'user_permissions':[]
//             },
//             'course':{
//               'id':1,
//               'name':'fake',
//               'course_code':'1234',
//               'subject_code':'cs'
//             }
//           }]
//         },
//       }).then(() => {
        
//       }).finally(() => {
//         done();
//       });
//     });
//   });

//   it('Sidebar: Mounted with courses properly', () => {
//     expect(wrapper.vm.courses.length).to.equal(1);
//   });
  
// });

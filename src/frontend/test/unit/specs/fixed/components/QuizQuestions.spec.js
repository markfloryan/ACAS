import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import LoadingLayer from '@/components/LoadingLayer';
import QuizQuestions from '@/components/quiz/QuizQuestions';
import store from '@/vuex/';
import SuiVue from 'semantic-ui-vue';
import 'semantic-ui-css/semantic.min.css';
import VueRouter from 'vue-router';
// 
const router = new VueRouter();

import moxios from 'moxios';

const localVue = createLocalVue();
localVue.use(Vuex);
localVue.use(SuiVue);
localVue.use(VueRouter);

describe('QuizQuestions.vue', () => {
  // let wrapper;

  afterEach(() => {
    // import and pass your custom axios instance to this method
    moxios.uninstall();
  });
  // Resets the store for each test
  beforeEach(() => {
    moxios.install();
  });

  it('QuizQuestions: Can\'t save quiz answers when not all questions are answered', (done) => {

    localStorage.setItem('profile', '{"auth":{"profile":{"first_name":"Jon","last_name":"Snow","email":"jsnow@virginia.edu","id_token":"afsdafsdf","group":true}}}');
    
    const wrapper = mount(QuizQuestions, {
      propsData: {
        questions: [{'pk':2,'text':'What\'s the look up time for an array','question_type':0,'total_points':1,'index':0,'answers':[{'pk':6,'text':'O(log(n))','correct':false,'question':2,'index':2},{'pk':5,'text':'Theta(n)','correct':false,'question':2,'index':1},{'pk':4,'text':'O(n)','correct':true,'question':2,'index':1}]},{'pk':1,'text':'What index do arrays start at','question_type':0,'total_points':1,'index':0,'answers':[{'pk':3,'text':'2','correct':false,'question':1,'index':2},{'pk':2,'text':'1','correct':false,'question':1,'index':1},{'pk':1,'text':'0','correct':true,'question':1,'index':0}]}],
        quizName: 'Quiz for arrays',
        role: 'professor',
        topicId: 1,
      },
      store,
      router,
      localVue,
      components: {
        LoadingLayer,
      }
    });
    
    const answerOne = wrapper.find('.answer input[type="radio"]');
    answerOne.setChecked();

    // Find submit button and press it to save quiz answers
    const submitQuizButton = wrapper.find('.actions .btn-primary');
    submitQuizButton.trigger('click');

    let toastState = store.state.toast;

    expect(toastState.visible).to.equal(true);
    expect(toastState.type).to.equal('error');
    done();
  });

  it('QuizQuestions: Save quiz answers', (done) => {

    localStorage.setItem('profile', '{"auth":{"profile":{"first_name":"Jon","last_name":"Snow","email":"jsnow@virginia.edu","id_token":"afsdafsdf","group":true}}}');
    
    const wrapper = mount(QuizQuestions, {
      propsData: {
        questions: [{'pk':2,'text':'What\'s the look up time for an array','question_type':0,'total_points':1,'index':0,'answers':[{'pk':6,'text':'O(log(n))','correct':false,'question':2,'index':2},{'pk':5,'text':'Theta(n)','correct':false,'question':2,'index':1},{'pk':4,'text':'O(n)','correct':true,'question':2,'index':1}]},{'pk':1,'text':'What index do arrays start at','question_type':0,'total_points':1,'index':0,'answers':[{'pk':3,'text':'2','correct':false,'question':1,'index':2},{'pk':2,'text':'1','correct':false,'question':1,'index':1},{'pk':1,'text':'0','correct':true,'question':1,'index':0}]}],
        quizName: 'Quiz for arrays',
        role: 'professor',
        topicId: 1,
      },
      store,
      router,
      localVue,
      components: {
        LoadingLayer,
      }
    });

    const questionOne = wrapper.findAll('.question').at(0);
    const questionTwo = wrapper.findAll('.question').at(1);
    
    const q1answerOne = questionOne.find('.answer input[type="radio"]');
    q1answerOne.setChecked();

    const q2answerOne = questionTwo.find('.answer input[type="radio"]');
    q2answerOne.setChecked();

    // Find submit button and press it to save quiz answers
    const submitQuizButton = wrapper.find('.actions .btn-primary');
    submitQuizButton.trigger('click');

    moxios.wait(() => {
      let saveQuizRequest = moxios.requests.mostRecent();
      saveQuizRequest.respondWith({
        status: 200,
        response: {},
      }).finally(() => {
        expect(wrapper.emitted()['contextChange'].length).to.equal(1);
        done();
      });
    });
  });

  it('QuizQuestions: Save quiz answers (server error)', (done) => {

    localStorage.setItem('profile', '{"auth":{"profile":{"first_name":"Jon","last_name":"Snow","email":"jsnow@virginia.edu","id_token":"afsdafsdf","group":true}}}');
    
    const wrapper = mount(QuizQuestions, {
      propsData: {
        questions: [{'pk':2,'text':'What\'s the look up time for an array','question_type':0,'total_points':1,'index':0,'answers':[{'pk':6,'text':'O(log(n))','correct':false,'question':2,'index':2},{'pk':5,'text':'Theta(n)','correct':false,'question':2,'index':1},{'pk':4,'text':'O(n)','correct':true,'question':2,'index':1}]},{'pk':1,'text':'What index do arrays start at','question_type':0,'total_points':1,'index':0,'answers':[{'pk':3,'text':'2','correct':false,'question':1,'index':2},{'pk':2,'text':'1','correct':false,'question':1,'index':1},{'pk':1,'text':'0','correct':true,'question':1,'index':0}]}],
        quizName: 'Quiz for arrays',
        role: 'professor',
        topicId: 1,
      },
      store,
      router,
      localVue,
      components: {
        LoadingLayer,
      }
    });

    const questionOne = wrapper.findAll('.question').at(0);
    const questionTwo = wrapper.findAll('.question').at(1);
    
    const q1answerOne = questionOne.find('.answer input[type="radio"]');
    q1answerOne.setChecked();

    const q2answerOne = questionTwo.find('.answer input[type="radio"]');
    q2answerOne.setChecked();

    // Find submit button and press it to save quiz answers
    const submitQuizButton = wrapper.find('.actions .btn-primary');
    submitQuizButton.trigger('click');

    moxios.wait(() => {
      let saveQuizRequest = moxios.requests.mostRecent();
      saveQuizRequest.respondWith({
        status: 500,
        response: {},
      }).finally(() => {
        let toastState = store.state.toast;

        expect(toastState.visible).to.equal(true);
        expect(toastState.type).to.equal('error');
        done();
      });
    });
  });
  
  it('QuizQuestions: contextChange to EditQuiz.vue', (done) => {

    const wrapper = mount(QuizQuestions, {
      propsData: {
        questions: [{'pk':2,'text':'What\'s the look up time for an array','question_type':0,'total_points':1,'index':0,'answers':[{'pk':6,'text':'O(log(n))','correct':false,'question':2,'index':2},{'pk':5,'text':'Theta(n)','correct':false,'question':2,'index':1},{'pk':4,'text':'O(n)','correct':true,'question':2,'index':1}]},{'pk':1,'text':'What index do arrays start at','question_type':0,'total_points':1,'index':0,'answers':[{'pk':3,'text':'2','correct':false,'question':1,'index':2},{'pk':2,'text':'1','correct':false,'question':1,'index':1},{'pk':1,'text':'0','correct':true,'question':1,'index':0}]}],
        quizName: 'Quiz for arrays',
        role: 'professor',
        topicId: 1,
      },
      store,
      router,
      localVue,
      components: {
        LoadingLayer,
      }
    });
    
    const editQuizButton = wrapper.find('.actions .btn-plain');
    editQuizButton.trigger('click');
    // assert event has been emitted
    expect(wrapper.emitted()['contextChange'].length).to.equal(1);
    done();
  });
});

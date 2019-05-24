import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import LoadingLayer from '@/components/LoadingLayer';
import QuizResults from '@/components/quiz/QuizResults';
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

describe('QuizResults.vue', () => {
  // let wrapper;

  afterEach(() => {
    // import and pass your custom axios instance to this method
    moxios.uninstall();
  });
  // Resets the store for each test
  beforeEach(() => {
    moxios.install();
    localStorage.setItem('profile', '{"auth":{"profile":{"first_name":"Jon","last_name":"Snow","email":"jsnow@virginia.edu","id_token":"afsdafsdf","group":true}}}');

  });

  it('QuizResults: ', (done) => {

    const wrapper = mount(QuizResults, {
      propsData: {
        studentQuizData: {'pk':1,'student':{'id':1,'password':'','last_login':null,'is_superuser':false,'is_staff':false,'is_active':true,'date_joined':'2019-02-12T17:10:09.898746Z','first_name':'Jon','last_name':'Snow','email':'jsnow@virginia.edu','join_date':'2019-02-12T17:10:09.899524Z','id_token':'asdfsd','is_professor':true,'username':null,'groups':[],'user_permissions':[]},'quiz':{'pk':1,'name':'Quiz for arrays','topic':{'id':1,'name':'dsaf','course':{'id':2,'name':'CS','course_code':'dsfasdf','subject_code':'afd'}},'questions':[{'pk':2,'text':'What\'s the look up time for an array','question_type':0,'total_points':1,'index':0,'answers':[{'pk':6,'text':'O(log(n))','correct':false,'question':2,'index':2},{'pk':5,'text':'Theta(n)','correct':false,'question':2,'index':1},{'pk':4,'text':'O(n)','correct':true,'question':2,'index':1}]},{'pk':1,'text':'What index do arrays start at','question_type':0,'total_points':1,'index':0,'answers':[{'pk':3,'text':'2','correct':false,'question':1,'index':2},{'pk':2,'text':'1','correct':false,'question':1,'index':1},{'pk':1,'text':'0','correct':true,'question':1,'index':0}]}]},'grade':100,'student_answers':[{'pk':1,'student':1,'question':1,'answer':1,'correct':false},{'pk':2,'student':1,'question':2,'answer':4,'correct':true}]},
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

    // console.log(wrapper.html());
    
    // const answerOne = wrapper.find('.answer input[type="radio"]');
    // answerOne.setChecked();

    // // Find submit button and press it to save quiz answers
    // const submitQuizButton = wrapper.find('.actions .btn-primary');
    // submitQuizButton.trigger('click');

    // let toastState = store.state.toast;

    // expect(toastState.visible).to.equal(true);
    // expect(toastState.type).to.equal('error');
    done();
  });

  
  it('QuizResults: contextChange to Quiz.vue', (done) => {

    const wrapper = mount(QuizResults, {
      propsData: {
        studentQuizData: {'pk':1,'student':{'id':1,'password':'','last_login':null,'is_superuser':false,'is_staff':false,'is_active':true,'date_joined':'2019-02-12T17:10:09.898746Z','first_name':'Jon','last_name':'Snow','email':'jsnow@virginia.edu','join_date':'2019-02-12T17:10:09.899524Z','id_token':'asdfsd','is_professor':true,'username':null,'groups':[],'user_permissions':[]},'quiz':{'pk':1,'name':'Quiz for arrays','topic':{'id':1,'name':'dsaf','course':{'id':2,'name':'CS','course_code':'dsfasdf','subject_code':'afd'}},'questions':[{'pk':2,'text':'What\'s the look up time for an array','question_type':0,'total_points':1,'index':0,'answers':[{'pk':6,'text':'O(log(n))','correct':false,'question':2,'index':2},{'pk':5,'text':'Theta(n)','correct':false,'question':2,'index':1},{'pk':4,'text':'O(n)','correct':true,'question':2,'index':1}]},{'pk':1,'text':'What index do arrays start at','question_type':0,'total_points':1,'index':0,'answers':[{'pk':3,'text':'2','correct':false,'question':1,'index':2},{'pk':2,'text':'1','correct':false,'question':1,'index':1},{'pk':1,'text':'0','correct':true,'question':1,'index':0}]}]},'grade':100,'student_answers':[{'pk':1,'student':1,'question':1,'answer':1,'correct':true},{'pk':2,'student':1,'question':2,'answer':4,'correct':true}]},
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
    
    const quizButton = wrapper.findAll('.actions .btn-plain').at(0);
    quizButton.trigger('click');
    // assert event has been emitted
    expect(wrapper.emitted()['contextChange'].length).to.equal(1);
    done();
  });

  it('QuizResults: contextChange to EditQuiz.vue', (done) => {

    const wrapper = mount(QuizResults, {
      propsData: {
        studentQuizData: {'pk':1,'student':{'id':1,'password':'','last_login':null,'is_superuser':false,'is_staff':false,'is_active':true,'date_joined':'2019-02-12T17:10:09.898746Z','first_name':'Jon','last_name':'Snow','email':'jsnow@virginia.edu','join_date':'2019-02-12T17:10:09.899524Z','id_token':'asdfsd','is_professor':true,'username':null,'groups':[],'user_permissions':[]},'quiz':{'pk':1,'name':'Quiz for arrays','topic':{'id':1,'name':'dsaf','course':{'id':2,'name':'CS','course_code':'dsfasdf','subject_code':'afd'}},'questions':[{'pk':2,'text':'What\'s the look up time for an array','question_type':0,'total_points':1,'index':0,'answers':[{'pk':6,'text':'O(log(n))','correct':false,'question':2,'index':2},{'pk':5,'text':'Theta(n)','correct':false,'question':2,'index':1},{'pk':4,'text':'O(n)','correct':true,'question':2,'index':1}]},{'pk':1,'text':'What index do arrays start at','question_type':0,'total_points':1,'index':0,'answers':[{'pk':3,'text':'2','correct':false,'question':1,'index':2},{'pk':2,'text':'1','correct':false,'question':1,'index':1},{'pk':1,'text':'0','correct':true,'question':1,'index':0}]}]},'grade':100,'student_answers':[{'pk':1,'student':1,'question':1,'answer':1,'correct':false},{'pk':2,'student':1,'question':2,'answer':4,'correct':true}]},
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
    
    const editQuizButton = wrapper.findAll('.actions .btn-plain').at(1);
    editQuizButton.trigger('click');
    // assert event has been emitted
    expect(wrapper.emitted()['contextChange'].length).to.equal(1);
    done();
  });
});

import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import QuizNotFound from '@/components/quiz/QuizNotFound';
import CreateQuiz from '@/components/quiz/CreateQuiz';
import EditQuiz from '@/components/quiz/EditQuiz';
import LoadingLayer from '@/components/LoadingLayer';
import QuizQuestions from '@/components/quiz/QuizQuestions';
import QuizResults from '@/components/quiz/QuizResults';
import Quiz from '@/components/quiz/Quiz';
import store from '@/vuex/';
import SuiVue from 'semantic-ui-vue';
import 'semantic-ui-css/semantic.min.css';
import VueRouter from 'vue-router';

const router = new VueRouter();

import moxios from 'moxios';

const localVue = createLocalVue();
localVue.use(Vuex);
localVue.use(SuiVue);
localVue.use(VueRouter);

const retrieveQuizResponse = {
  'status':'200 - OK',
  'result': {'pk':1,'name':'quiz for arrays','topic':{'id':1,'name':'a','course':{'id':1,'name':'b','course_code':'j','subject_code':'j'}},'questions':[{'pk':2,'text':'What\'s the lookup time for an element in an array?','question_type':0,'total_points':1,'index':0,'answers':[{'pk':6,'text':'Theta(n)','correct':false,'question':2,'index':2},{'pk':5,'text':'O(n)','correct':true,'question':2,'index':1},{'pk':4,'text':'O(log(n))','correct':false,'question':2,'index':1}]},{'pk':1,'text':'What index do arrays start at?','question_type':0,'total_points':1,'index':0,'answers':[{'pk':3,'text':'2','correct':false,'question':1,'index':2},{'pk':2,'text':'1','correct':false,'question':1,'index':1},{'pk':1,'text':'0','correct':true,'question':1,'index':0}]}]}
};

const retrieveStudentAnswersResponse = {
  'status':'200 - OK',
  'result':{'pk':1,'student':{'id':1,'password':'','last_login':null,'is_superuser':false,'is_staff':false,'is_active':true,'date_joined':'2019-02-14T21:01:59.050122Z','first_name':'Jon','last_name':'Snow','email':'jsnow@virginia.edu','join_date':'2019-02-14T21:01:59.050625Z','id_token':'adfasd','is_professor':true,'username':null,'groups':[],'user_permissions':[]},'quiz':{'pk':1,'name':'quiz for arrays','topic':{'id':1,'name':'a','course':{'id':1,'name':'b','course_code':'j','subject_code':'j'}},'questions':[{'pk':2,'text':'What\'s the lookup time for an element in an array?','question_type':0,'total_points':1,'index':0,'answers':[{'pk':6,'text':'Theta(n)','correct':false,'question':2,'index':2},{'pk':5,'text':'O(n)','correct':true,'question':2,'index':1},{'pk':4,'text':'O(log(n))','correct':false,'question':2,'index':1}]},{'pk':1,'text':'What index do arrays start at?','question_type':0,'total_points':1,'index':0,'answers':[{'pk':3,'text':'2','correct':false,'question':1,'index':2},{'pk':2,'text':'1','correct':false,'question':1,'index':1},{'pk':1,'text':'0','correct':true,'question':1,'index':0}]}]},'grade':100.0,'student_answers':[{'pk':1,'student':1,'question':1,'answer':1,'correct':true},{'pk':2,'student':1,'question':2,'answer':5,'correct':true}]}
};

describe('Quiz.vue', () => {
  let wrapper;

  afterEach(() => {
    // import and pass your custom axios instance to this method
    moxios.uninstall();
  });
  // Resets the store for each test
  beforeEach(() => {
    moxios.install();

    store.commit('auth/signIn', {
      group: true,
      first_name: 'Jon',
      last_name: 'Snow',
    });


    localStorage.setItem('profile', '{"auth":{"profile":{"first_name":"Jon","last_name":"Snow","email":"jsnow@virginia.edu","id_token":"afsdafsdf","group":true}}}');
    
    wrapper = mount(Quiz, {
      propsData: {
        topicId: 1,
      },
      store,
      router,
      localVue,
      components: {
        CreateQuiz,
        EditQuiz,
        LoadingLayer,
        QuizNotFound,
        QuizQuestions,
        QuizResults,
      }
    });
  });

  it('Quiz: Quiz found and student\'s answers found', (done) => {
    
    // when the app requests the quiz information
    moxios.wait(() => {
      const quizRequest = moxios.requests.mostRecent();
      quizRequest.respondWith({
        status: 200,
        response: retrieveQuizResponse,
      }).then(() => {
        const studentAnswersRequest = moxios.requests.mostRecent();
        studentAnswersRequest.respondWith({
          status: 200,
          response: retrieveStudentAnswersResponse
        }).then(() => {
          // const tryAgainButton = wrapper.findAll('.actions .btn-plain').at(0);
          // tryAgainButton.trigger('click');
          done();
        });
      });
      
    });
  });

  it('Quiz: Quiz found but student\'s answers not found', (done) => {
    
    // when the app requests the quiz information
    moxios.wait(() => {
      const quizRequest = moxios.requests.mostRecent();
      quizRequest.respondWith({
        status: 200,
        response: retrieveQuizResponse,
      }).then(() => {
        const studentAnswersRequest = moxios.requests.mostRecent();
        studentAnswersRequest.respondWith({
          status: 404,
          response: {}
        }).then(() => {
          done();
        });
      });
      
    });
  });

  it('Quiz: Test quiz not found', (done) => {

    // when the app requests the quiz information
    moxios.wait(() => {
      const quizRequest = moxios.requests.mostRecent();
      quizRequest.respondWith({
        status: 404,
        response: {
        },
      }).then(() => {
        
      }).finally(() => {
        done();
      });
    });
  });

  it('Quiz: Navigate to try again when you\'ve already taken the quiz', (done) => {
    
    // when the app requests the quiz information
    moxios.wait(() => {
      const quizRequest = moxios.requests.mostRecent();
      quizRequest.respondWith({
        status: 200,
        response: retrieveQuizResponse,
      }).then(() => {
        const studentAnswersRequest = moxios.requests.mostRecent();
        studentAnswersRequest.respondWith({
          status: 200,
          response: retrieveStudentAnswersResponse
        }).then(() => {
          const tryAgainButton = wrapper.findAll('.actions .btn-plain').at(0);
          tryAgainButton.trigger('click');

          const quizQuestionsRequest = moxios.requests.mostRecent();
          quizQuestionsRequest.respondWith({
            status: 200,
            response: retrieveQuizResponse
          }).then(() => {
            
            done();
          });
        });
      });
      
    });
  });

  it('Quiz: Navigate to edit quiz', (done) => {
    
    // when the app requests the quiz information
    moxios.wait(() => {
      const quizRequest = moxios.requests.mostRecent();
      quizRequest.respondWith({
        status: 200,
        response: retrieveQuizResponse,
      }).then(() => {
        const studentAnswersRequest = moxios.requests.mostRecent();
        studentAnswersRequest.respondWith({
          status: 200,
          response: retrieveStudentAnswersResponse
        }).then(() => {
          const editQuizButton = wrapper.findAll('.actions .btn-plain').at(1);
          editQuizButton.trigger('click');
          done();
        });
      });
      
    });
  });

  it('Quiz: Answer quiz questions and submit', (done) => {
    
    // when the app requests the quiz information
    moxios.wait(() => {
      const quizRequest = moxios.requests.mostRecent();
      quizRequest.respondWith({
        status: 200,
        response: retrieveQuizResponse,
      }).then(() => {
        const studentAnswersRequest = moxios.requests.mostRecent();
        studentAnswersRequest.respondWith({
          status: 404,
          response: {}
        }).then(() => {
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
              let retrieveNewAnswersRequest = moxios.requests.mostRecent();
              retrieveNewAnswersRequest.respondWith({
                status: 200,
                response: retrieveStudentAnswersResponse,
              }).finally(() => {
                done();
              });
            });
          });
        });
      });
      
    });
  });

  


});

import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import QuizNotFound from '@/components/quiz/QuizNotFound';
import CreateQuiz from '@/components/quiz/CreateQuiz';
import LoadingLayer from '@/components/LoadingLayer';
import QuizQuestions from '@/components/quiz/QuizQuestions';
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

describe('QuizNotFound.vue', () => {
  // let wrapper;

  afterEach(() => {
    // import and pass your custom axios instance to this method
    moxios.uninstall();
  });
  // Resets the store for each test
  beforeEach(() => {
    moxios.install();
  });

  it('QuizNotFound: changeContext to quizCreater', (done) => {

    const wrapper = mount(QuizNotFound, {
      propsData: {
        role: 'professor',
      },
      store,
      router,
      localVue,
      components: {
        CreateQuiz,
        LoadingLayer,
        QuizQuestions,
        QuizResults,
      }
    });
    
    const addQuizButton = wrapper.find('.actions .btn-create');
    addQuizButton.trigger('click');
    // assert event has been emitted
    expect(wrapper.emitted()['contextChange'].length).to.equal(1);
    done();
  });

  
});

import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import EditQuiz from '@/components/quiz/EditQuiz';
import LoadingLayer from '@/components/LoadingLayer';
import { API_URL } from '@/constants';
import toastStore from '@/vuex/modules/Toast';
import settingsStore from '@/vuex/modules/Settings';
import SuiVue from 'semantic-ui-vue';
import 'semantic-ui-css/semantic.min.css';

import moxios from 'moxios';

const localVue = createLocalVue();
localVue.use(Vuex);
localVue.use(SuiVue);

describe('EditQuiz.vue', () => {
  let store;
  let wrapper;

  afterEach(() => {
    // import and pass your custom axios instance to this method
    moxios.uninstall();
  });
  // Resets the store for each test
  beforeEach(() => {
    moxios.install();
    store = new Vuex.Store({
      modules: {
        toast: toastStore,
        settings: settingsStore
      },
    });
    wrapper = mount(EditQuiz, {
      propsData: {
        initialQuestions: [
          {
            pk: 2,
            text: 'Lookup time for element in array',
            question_type: 0,
            total_points: 1,
            index: 0,
            answers: [
              { pk:5, text: 'O(log(n))', correct:false, question: 2, index:2 },
              { pk:4, text: 'O(n)', correct: true, question:2, index:1 }
            ]
          },
          {
            pk: 1,
            text: 'Arrays start at what',
            question_type: 0,
            total_points: 1,
            index:0,
            answers:[
              { pk:3, text: '2', correct: false, question: 1, index: 2 },
              { pk:2, text: '1', correct: false, question: 1, index: 1},
              { pk:1, text: '0', correct: true, question:1, index:0 }
            ]
          }
        ],
        initialQuizName: 'Quiz for arrays',
        role: 'professor',
        topicId: 1
      },
      store,
      localVue,
      components: {
        LoadingLayer,
      }
    });
  });

  it('EditQuiz: Clicking the remove answer button removes an answer', () => {
    const oldQuestionLength = wrapper.vm.form.questions.length;

    const removeAnswer = wrapper.find('.question i.minus.icon');
    removeAnswer.trigger('click');
    
    expect(wrapper.vm.form.questions.length).to.equal(oldQuestionLength - 1);
  });

  it('EditQuiz: Clicking the add question button adds a question', () => {
    const oldAmountOfQuestions = wrapper.vm.form.questions.length;
    const button = wrapper.find('.btn-create');
    button.trigger('click');
    expect(wrapper.vm.form.questions.length).to.equal(oldAmountOfQuestions + 1);
  });

  it('EditQuiz: Clicking the remove question button removes a question', () => {
    const oldAmountOfAnswers = wrapper.vm.form.questions[0].answers.length;

    const removeAnswer = wrapper.find('.answer i.minus.icon');
    removeAnswer.trigger('click');
    
    expect(wrapper.vm.form.questions[0].answers.length).to.equal(oldAmountOfAnswers - 1);
  });

  it('EditQuiz: Select answer as correct one', () => {
    const setAsCorrectAnswerCheckBox = wrapper.find('.answer input[type="radio"]');
    setAsCorrectAnswerCheckBox.setChecked();
    expect(wrapper.vm.form.questions[0].answers[0].correct).to.equal(true);
  });

  it('EditQuiz: Save quiz changes', (done) => {
    
    // Save this new quiz
    const addQuizButton = wrapper.find('button.btn-primary');
    addQuizButton.trigger('click');
    
    // Create the fake request for saving the quiz
    moxios.stubRequest(`${API_URL}/quiz/${wrapper.vm.topicId}`, wrapper.vm.form, {
      status: 200,
      response: {
        id: 1, owners: [{ name: 'Test', address: '123 Test St.' }]
      }
    });

    // Wait for the fake request to finish and chekc the component's state
    moxios.wait(() => {
      expect(wrapper.vm.loading).to.equal(false);
      done();
    });
  });

  it('EditQuiz: Can\'t save quiz changes without a quiz name', (done) => {
    // Remove quiz name
    const quizNameTextField  = wrapper.find('input[placeholder="Name"]');
    quizNameTextField.setValue('');

    // Save this new quiz
    const addQuizButton = wrapper.find('button.btn-primary');
    addQuizButton.trigger('click');
    
    // Create the fake request for saving the quiz
    moxios.stubRequest(`${API_URL}/quiz/${wrapper.vm.topicId}`, wrapper.vm.form, {
      status: 200,
      response: {
        id: 1, owners: [{ name: 'Test', address: '123 Test St.' }]
      }
    });

    // Wait for the fake request to finish and chekc the component's state
    moxios.wait(() => {
      expect(wrapper.vm.loading).to.equal(false);
      done();
    });
  });

  it('EditQuiz: Can\'t save quiz changes without zero questions', (done) => {
    // Remove first question
    const removeQuestionOne = wrapper.find('.question i.minus.icon');
    removeQuestionOne.trigger('click');

    // Remove second question
    const removeQuestionTwo = wrapper.find('.question i.minus.icon');
    removeQuestionTwo.trigger('click');

    // Save this new quiz
    const addQuizButton = wrapper.find('button.btn-primary');
    addQuizButton.trigger('click');
    
    // Create the fake request for saving the quiz
    moxios.stubRequest(`${API_URL}/quiz/${wrapper.vm.topicId}`, wrapper.vm.form, {
      status: 200,
      response: {
        id: 1, owners: [{ name: 'Test', address: '123 Test St.' }]
      }
    });

    // Wait for the fake request to finish and chekc the component's state
    moxios.wait(() => {
      expect(wrapper.vm.loading).to.equal(false);
      done();
    });
  });

  it('EditQuiz: Can\'t save quiz changes with a question that has no text', (done) => {
    const questionTextField  = wrapper.find('input[placeholder="Question text"]');
    questionTextField.setValue('');

    // Save this new quiz
    const addQuizButton = wrapper.find('button.btn-primary');
    addQuizButton.trigger('click');
    
    // Create the fake request for saving the quiz
    moxios.stubRequest(`${API_URL}/quiz/${wrapper.vm.topicId}`, wrapper.vm.form, {
      status: 200,
      response: {
        id: 1, owners: [{ name: 'Test', address: '123 Test St.' }]
      }
    });

    // Wait for the fake request to finish and chekc the component's state
    moxios.wait(() => {
      expect(wrapper.vm.loading).to.equal(false);
      done();
    });
  });

  it('EditQuiz: Can\'t save quiz changes with a question that has no answers', (done) => {
    wrapper.vm.form.questions[0].answers = [];

    // Save this new quiz
    const addQuizButton = wrapper.find('button.btn-primary');
    addQuizButton.trigger('click');
    
    // Create the fake request for saving the quiz
    moxios.stubRequest(`${API_URL}/quiz/${wrapper.vm.topicId}`, wrapper.vm.form, {
      status: 200,
      response: {
        id: 1, owners: [{ name: 'Test', address: '123 Test St.' }]
      }
    });

    // Wait for the fake request to finish and chekc the component's state
    moxios.wait(() => {
      expect(wrapper.vm.loading).to.equal(false);
      done();
    });
  });

  it('EditQuiz: Change context', (done) => {
    // Need to actually test its been unmounted
    const cancelButton = wrapper.find('.actions .btn-plain');
    cancelButton.trigger('click');

    wrapper.vm.$nextTick(() => {
      done();
    });
  });
  
});

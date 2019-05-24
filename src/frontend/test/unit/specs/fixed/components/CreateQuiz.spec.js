import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import CreateQuiz from '@/components/quiz/CreateQuiz';
import LoadingLayer from '@/components/LoadingLayer';
import { API_URL } from '@/constants';
import toastStore from '@/vuex/modules/Toast';
import settingsStore from '@/vuex/modules/Settings';
import SuiVue from 'semantic-ui-vue';
import 'semantic-ui-css/semantic.min.css';

import moxios from 'moxios';

const localVue = createLocalVue();
// jest.mock('axios');
localVue.use(Vuex);
localVue.use(SuiVue);
localVue.use(LoadingLayer);

describe('CreateQuiz.vue', () => {
  let store;

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
      components: {
        LoadingLayer
      }
    });
  });

  it('CreateQuiz: Clicking the add question button adds a question', () => {
    const wrapper = mount(CreateQuiz, { store, localVue });
    const button = wrapper.find('.btn-create');
    button.trigger('click');
    expect(wrapper.vm.form.questions.length).to.equal(1);
  });

  it('CreateQuiz: Clicking the remove question button removes a question', () => {
    const wrapper = mount(CreateQuiz, { store, localVue });
    const button = wrapper.find('.btn-create');
    button.trigger('click');
    const deleteQuestion = wrapper.find('.minus.icon');
    deleteQuestion.trigger('click');
    expect(wrapper.vm.form.questions.length).to.equal(0);
  });

  it('CreateQuiz: Clicking add answer button with text for a question adds an answer', () => {
    const wrapper = mount(CreateQuiz, { store, localVue });
    const button = wrapper.find('.btn-create');
    button.trigger('click');
    const addAnswerButton = wrapper.find('.answer .plus');
    const answerTextField = wrapper.find('.answer input');
    
    answerTextField.setValue('helloworld');
    addAnswerButton.trigger('click');
    expect(wrapper.vm.form.questions[0].answers.length).to.equal(1);
  });

  it('CreateQuiz: Clicking add answer button without text for a question doesn\'t add an answer', () => {
    const wrapper = mount(CreateQuiz, { store, localVue });
    const button = wrapper.find('.btn-create');
    button.trigger('click');
    const addAnswerButton = wrapper.find('.answer .plus');
    
    addAnswerButton.trigger('click');
    expect(wrapper.vm.form.questions[0].answers.length).to.equal(0);
  });

  it('CreateQuiz: Select answer as correct one', () => {
    const wrapper = mount(CreateQuiz, { store, localVue });
    const button = wrapper.find('.btn-create');
    button.trigger('click');
    const addAnswerButton = wrapper.find('.answer .plus');
    const answerTextField = wrapper.find('.answer input');
    
    answerTextField.setValue('helloworld');
    addAnswerButton.trigger('click');

    const setAsCorrectAnswerCheckBox = wrapper.find('.answer input[type="radio"]');
    setAsCorrectAnswerCheckBox.setChecked();
    expect(wrapper.vm.form.questions[0].answers[0].correct).to.equal(true);
  });

  it('CreateQuiz: Remove answer', () => {
    const wrapper = mount(CreateQuiz, { store, localVue });
    const button = wrapper.find('.btn-create');
    button.trigger('click');
    const addAnswerButton = wrapper.find('.answer .plus');
    const answerTextField = wrapper.find('.answer input');
    
    answerTextField.setValue('helloworld');
    addAnswerButton.trigger('click');

    const removeAnswerButton = wrapper.find('.answer .minus');
    removeAnswerButton.trigger('click');

    expect(wrapper.vm.form.questions[0].answers.length).to.equal(0);
  });

  it('CreateQuiz: Create quiz', (done) => {
    
    const wrapper = mount(CreateQuiz, { 
      components: {
        LoadingLayer 
      },
      store,
      localVue
    });

    // Set quiz name
    const quizNameTextField  = wrapper.find('input[placeholder="Name"]');
    quizNameTextField.setValue('quiz for arrays');

    // Add a question
    const button = wrapper.find('.btn-create');
    button.trigger('click');

    // Set the question's text
    const questionTextField = wrapper.find('.question input[placeholder="Question text"]');
    questionTextField.setValue('what index do arrays start at');
    
    // Set the answer's text
    const answerTextField = wrapper.find('.answer input');
    answerTextField.setValue('arrays start at 0');
    
    // Add answer
    const addAnswerButton = wrapper.find('.answer .plus');
    addAnswerButton.trigger('click');

    // Set that answer as correct
    const setAsCorrectAnswerCheckBox = wrapper.find('.answer input[type="radio"]');
    setAsCorrectAnswerCheckBox.setChecked();

    // Save this new quiz
    const addQuizButton = wrapper.find('button.btn-primary');
    addQuizButton.trigger('click');
    
    // Create the fake request for saving the quiz
    moxios.stubRequest(`${API_URL}/quiz/`, wrapper.vm.form, {
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

  it('CreateQuiz: Can\'t save quiz changes without a quiz name', (done) => {
    const wrapper = mount(CreateQuiz, { 
      components: {
        LoadingLayer 
      },
      store,
      localVue
    });

    // Set quiz name
    const quizNameTextField  = wrapper.find('input[placeholder="Name"]');
    quizNameTextField.setValue('quiz for arrays');

    // Add a question
    const button = wrapper.find('.btn-create');
    button.trigger('click');

    // Set the question's text
    const questionTextField = wrapper.find('.question input[placeholder="Question text"]');
    questionTextField.setValue('what index do arrays start at');
    
    // Set the answer's text
    const answerTextField = wrapper.find('.answer input');
    answerTextField.setValue('arrays start at 0');
    
    // Add answer
    const addAnswerButton = wrapper.find('.answer .plus');
    addAnswerButton.trigger('click');

    // Set that answer as correct
    const setAsCorrectAnswerCheckBox = wrapper.find('.answer input[type="radio"]');
    setAsCorrectAnswerCheckBox.setChecked();
    
    // Remove quiz name
    // const quizNameTextField  = wrapper.find('input[placeholder="Name"]');
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

  it('CreateQuiz: Can\'t save quiz changes without zero questions', (done) => {
    const wrapper = mount(CreateQuiz, { 
      components: {
        LoadingLayer 
      },
      store,
      localVue
    });

    // Set quiz name
    const quizNameTextField  = wrapper.find('input[placeholder="Name"]');
    quizNameTextField.setValue('quiz for arrays');

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

  it('CreateQuiz: Can\'t save quiz changes with a question that has no text', (done) => {
    const wrapper = mount(CreateQuiz, { 
      components: {
        LoadingLayer 
      },
      store,
      localVue
    });

    // Set quiz name
    const quizNameTextField  = wrapper.find('input[placeholder="Name"]');
    quizNameTextField.setValue('quiz for arrays');

    // Add a question
    const button = wrapper.find('.btn-create');
    button.trigger('click');
    
    // Set the answer's text
    const answerTextField = wrapper.find('.answer input');
    answerTextField.setValue('arrays start at 0');
    
    // Add answer
    const addAnswerButton = wrapper.find('.answer .plus');
    addAnswerButton.trigger('click');

    // Set that answer as correct
    const setAsCorrectAnswerCheckBox = wrapper.find('.answer input[type="radio"]');
    setAsCorrectAnswerCheckBox.setChecked();

    // Save this new quiz
    const addQuizButton = wrapper.find('button.btn-primary');
    addQuizButton.trigger('click');
    
    // Create the fake request for saving the quiz
    moxios.stubRequest(`${API_URL}/quiz/ `, wrapper.vm.form, {
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

  it('CreateQuiz: Can\'t save quiz changes with a question that has no answers', (done) => {
    const wrapper = mount(CreateQuiz, { 
      components: {
        LoadingLayer 
      },
      store,
      localVue
    });

    // Set quiz name
    const quizNameTextField  = wrapper.find('input[placeholder="Name"]');
    quizNameTextField.setValue('quiz for arrays');

    // Add a question
    const button = wrapper.find('.btn-create');
    button.trigger('click');

    // Set the question's text
    const questionTextField = wrapper.find('.question input[placeholder="Question text"]');
    questionTextField.setValue('what index do arrays start at');
    
    // Save this new quiz
    const addQuizButton = wrapper.find('button.btn-primary');
    addQuizButton.trigger('click');
    
    // Create the fake request for saving the quiz
    moxios.stubRequest(`${API_URL}/quiz/`, wrapper.vm.form, {
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

});

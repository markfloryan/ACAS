<template>
  <!-- EditQuiz.vue
    This is the form to edit a pre-existing quiz in Quiz.vue

    It prepopulates itself with the current questions/answers of the Quiz and allows
    you edit/delete those as well as add new ones
   -->
  <div >
    <div class="quiz-header">
      <h2 class="title">No quiz yet</h2>
      <div class="actions">
        <button class="btn btn-primary"
          :style="returnPrimaryButtonStyle"
          @click="saveQuizChanges()" v-if="role === 'professor'">Save quiz</button>
        <button class="btn btn-plain"
          @click="changeContext('quiz')">Cancel</button>
      </div>
    </div>
    <sui-form @submit.prevent class="create-quiz">
      <sui-form-field>
        <label>Name</label>
        <input placeholder="Name" v-model="form.name">
      </sui-form-field>
       <sui-form-field>
        <label>Weight (in Topic)</label>
        <input placeholder="0.3, 0.25, 1" v-model="form.weight">
      </sui-form-field>
      <sui-form-field>
        <label>Questions</label>
        <ol class="quiz-questions">
          <li v-for="(question, questionIndex) in form.questions"
            :key="`quiz-question-${question.pk}`"
            class="question">
            <sui-icon name="minus icon" @click="removeQuestion(questionIndex)"/>
            <sui-form-field style="width: 80%; display: inline-block;">
              <input style="width: 100%; display: inline-block;" placeholder="Question text" v-model="question.text">
            </sui-form-field>
            <ol type="a" class="answers-list">
              <li v-for="(answer, index) in question.answers"
                :key="`quiz-question-current-answer-${answer.pk}`"
                class="answer">
                <sui-icon
                  @click="removeAnswer(questionIndex, index)"
                  name="minus icon" />
                {{ answer.text }}
    
                <input type="radio" style="margin-left: 18pt;"
                  @click="selectAsCorrectAnswer(questionIndex, index)"
                  :checked="answer.correct">
                <sui-icon v-if="answer.correct"
                  @click="addAnswer(questionIndex)"
                  name="check icon" style="color: var(--color-green-40);" />
              </li>
              <li class="answer">
                <sui-icon 
                  @click="addAnswer(questionIndex)"
                  name="plus icon" />
                <sui-form-field style="width: 80%; display: inline-block;">
                  <input style="width: 100%; display: inline-block;" placeholder="Answer text" v-model="question.currentAnswer.text">
                </sui-form-field>
              </li>
            </ol>
          </li>
        </ol>
      </sui-form-field>
      <div style="text-align: center;">
        <button type="button" class="btn btn-create" @click="addQuestion()">Add question</button>
      </div>
    </sui-form>
      
    <LoadingLayer v-if="loading"
      :message="'Saving quiz answers...'" />
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapMutations } from 'vuex';
import LoadingLayer from '@/components/LoadingLayer';
import { API_URL } from '@/constants';

export default {
  components: {
    LoadingLayer,
  },
  props: {
    initialQuestions: {
      type: Array,
    },
    initialQuizName: {
      type: String,
    },
    role: {
      type: String,
    },
    topicId: {
      type: Number,
    },
    weight: {
      type: Number,
    },
  },
  data() {
    return {
      loading: false,
      form: {
        name: '',
        topic: '',
        questions: [],
        deletedQuestions: [],
      },
    };
  },
  computed: {
    ...mapGetters( 'settings', [
      'returnPrimaryButtonStyle'
    ]),
  },
  created() {
    this.form.topic = this.topicId;
    this.form.name = this.initialQuizName;
    this.form.weight = this.weight;
    this.form.questions = this.initialQuestions.map((question) => {
      return {
        ...question,
        currentAnswer: {
          text: '',
          correct: false,
          index: question.answers.length,
        },
        deletedAnswers: [],
      };
    });
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    selectAsCorrectAnswer(questionIndex, answerIndex) {
      const questionAnswers = this.form.questions[questionIndex].answers;
      const newAnswers = [];
      // This version of updating each answer's 'correct' field is a bit overly complicated but fixes a rerendering issue.
      questionAnswers.forEach((answer, index) => {
        newAnswers.push({
          ...answer,
          correct: answer.correct = (index === answerIndex),
        });
      });
      this.form.questions[questionIndex].answers = newAnswers;
    },
    changeContext(context) {
      this.$emit('contextChange', context);
    },
    addAnswer(index) {
      if (this.form.questions[index].currentAnswer.text) {
        this.form.questions[index].answers.push({
          ...this.form.questions[index].currentAnswer,
        });
        this.form.questions[index].currentAnswer = {
          text: '',
          correct: false,
          index: this.form.questions[index].answers.length,
        };
      } else {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Couldn\'t add answer',
          message: 'Please make sure the answer has text before adding it',
          duration: 6000,
        });
      }
    },
    removeAnswer(questionIndex, index) {
      this.form.questions[questionIndex].deletedAnswers.push({
        ...this.form.questions[questionIndex].answers[index],
      });
      this.form.questions[questionIndex].answers.splice(index, 1);
    },
    addQuestion(index) {
      this.form.questions.push({
        text: undefined,
        question_type: 0,
        total_points: 1,
        index: 0,
        answers: [],
        currentAnswer: {
          correct: false,
          text: '',
          question_type: 0,
          total_points: 1,
          index: this.form.questions.length,
        },
      });
    },
    removeQuestion(index) {
      this.form.deletedQuestions.push({
        ...this.form.questions[index],
      });
      this.form.questions.splice(index, 1);
    },
    saveQuizChanges() {

      // Form validation making sure nothing invalid gets successfully saved
      const data = this.form;
      if (data.name === '') {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Couldn\'t save the quiz!',
          message: 'Please provide a name for the quiz.',
          duration: 6000,
        });
        return;
      }
      if (data.questions.length < 1) {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Couldn\'t save your quiz answers!',
          message: 'Please make sure that the quiz has questions',
          duration: 6000,
        });
        return;
      }
      for (let i = 0 ; i < data.questions.length ; i++) {
        let question = data.questions[i];
        if (!question.text) {
          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'Couldn\'t save your quiz answers!',
            message: 'Please make sure that every question has text',
            duration: 6000,
          });
          return;
        }
        if (question.answers.length < 1) {
          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'Couldn\'t save your quiz answers!',
            message: 'Please make sure that every question has answers',
            duration: 6000,
          });
          return;
        }
      };
      // End validation
      this.loading = true;

      // Once we have validated the info, we can send the request to save our edit
      axios.put(`${API_URL}/quiz/${this.topicId}`, data)
        .then(() => {
          this.$emit('contextChange', 'quiz');
        })
        .catch((error) => { alert(error); })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<style scoped>
  .question-answer {
    width: 60%;
    display: inline-block;
  }
  .quiz-questions, .quiz-results {
    height: initial;
    overflow-y: initial;
  }
  div.question-answer.ui.input > input {
    width: 100%;
  }
  .answers-list, .quiz-questions {
    line-height: 25.5pt;
  }
  .quiz-questions .ui.input input {
    width: 300pt;
  }
  .create-quiz {
    max-height: 375pt;
    overflow-y: scroll;
  }
  .minus.icon.icon {
    color: var(--color-red-30);
    margin-right: 8pt;
    cursor: pointer;
  }
  .plus.icon.icon {
    color: var(--color-green-40);
    margin-right: 8pt;
    cursor: pointer;
  }
  .quiz-questions .ui.input {
    width: 80% !important;
    display: inline-block !important;
  }
  .quiz-questions .ui.input input {
    background-color: blue !important;
    width: 300pt !important;
  }
</style>
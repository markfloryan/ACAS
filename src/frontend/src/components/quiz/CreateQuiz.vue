<template>
  <!-- CreateQuiz.vue
    This is create quiz form conditionally shown in Quiz.vue

   -->
  <div>
    <div class="quiz-header">
      <h2 class="title">No quiz yet</h2>
      <div class="actions">
        <button class="btn btn-primary"
          :style="returnPrimaryButtonStyle" 
          @click="createQuiz()">Create quiz</button>
      </div>
    </div>
    <sui-form class="create-quiz" @submit.prevent>
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
            <sui-form-field>
              <input placeholder="Question text"
                v-model="question.text">
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

                <sui-form-field>
                  <input placeholder="Answer text"
                    v-model="question.currentAnswer.text">
                </sui-form-field>
              </li>
            </ol>
          </li>
        </ol>
      </sui-form-field>
      <div style="text-align: center;">
        <button type="button" style="width: 100%; margin-bottom: 8pt;" class="btn btn-create" @click="addQuestion()">Add question</button>
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
    topicId: {
      type: Number,
    }
  },
  data() {
    return {
      loading: false,
      form: {
        name: '',
        topic: '',
        questions: [],
        weight: 0,
      },
      responseResult: undefined
    };
  },
  computed: {
    ...mapGetters( 'settings', [
      'returnPrimaryButtonStyle'
    ]),
  },
  created() {
    this.form.topic = this.topicId; 
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    selectAsCorrectAnswer(questionIndex, answerIndex) {
      this.form.questions[questionIndex]
        .answers.forEach((answer, index) => {
          answer.correct = (index === answerIndex);
        });
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
      this.form.questions.splice(index, 1);
    },
    createQuiz() {
      this.responseResult = 'Beginning';
      const data = this.form;
      
      // The following if block is form validation to prevent invalid info about the quiz being saved
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
      this.responseResult = 'Middle';
      // Once we've gone through the validation, we can send the network request with our data to create the quiz
      axios.post(`${API_URL}/quiz/`, data)
        .then((response) => {
          this.responseResult = 'End';
          this.responseResult = response;
          this.$emit('contextChange', 'quiz');
        })
        .catch((error) => {
          this.responseResult = 'End - error';
          alert(error);
        })
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
  .quiz-questions .field {
    width: 90%;
    display: inline-block;
  }
  .quiz-questions .field input {
    width: 100%;
    display: inline-block;
  }
</style>
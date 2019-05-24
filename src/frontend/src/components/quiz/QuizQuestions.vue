<template>
  <!-- QuizQuestions.vue
    This is the "main" view for a quiz, as in this is what you see when you're taking a quiz
   -->
  <div class="quiz">
    <div class="quiz-header">
      <h2 class="title">{{ quizName }}</h2>
      <div class="actions">
        <button class="btn btn-primary" :style="returnPrimaryButtonStyle"
          @click="sendQuizAnswers" v-if="notViewingAsStudent">Submit quiz</button>
        <button class="btn btn-plain" v-if="role === 'professor' && notViewingAsStudent"
          @click="changeContext('quizEditor')">Edit</button>
      </div>
    </div>
    <ol class="quiz-questions">
      <li v-for="question in questions"
        :key="`quiz-question-${question.pk}`"
        class="question">
        <p>{{ question.text }}</p>
        <ol type="a" class="answers-list">
          <li v-for="answer in question.answers"
            :key="`quiz-question-${question.pk}-answer-${answer.pk}`"
            class="answer">
            <input type="radio" :id="answer.pk"
              :value="answer.pk"
              v-model="selectedAnswers[question.pk]">

            <label :for="answer.pk">{{ answer.text }}</label>
          </li>
        </ol>
      </li>
    </ol>
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
    questions: {
      type: Array,
    },
    quizName: {
      type: String,
    },
    role: {
      type: String,
    },
    topicId: {
      type: Number,
    },
  },
  data() {
    return {
      selectedAnswers: {},
    };
  },
  computed: {
    ...mapGetters(
      'settings', ['returnPrimaryButtonStyle'],
    ),
    notViewingAsStudent() {
      return !this.$route.query || !this.$route.query.viewAs;
    },
  },
  created() {
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    changeContext(context) {
      this.$emit('contextChange', context);
    },
    // This takes your answers and sends saves them in the db
    sendQuizAnswers() {
      this.$emit('loadingChange', true);
      const profile = JSON.parse(localStorage.getItem('profile'));
      const data = {
        answers: Object.keys(this.selectedAnswers).map((key) => ({
          question_id: key,
          answer_id: this.selectedAnswers[key],
        })),
        topic_id: this.topicId,
        id_token: profile.auth.profile.id_token,
      };

      if (data.answers.length !== this.questions.length) {
        this.sendingAnswersInProgress = false;
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Couldn\'t save your quiz answers!',
          message: 'Please answer all the questions before saving.',
          duration: 6000,
        });
        this.$emit('loadingChange', false);
        return false;
      }

      axios.post(`${API_URL}/student/quiz/${this.topicId}`, data)
        .then((response) => {
          this.$emit('contextChange', 'quizResults');
        })
        .catch((error) => {
          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'Couldn\'t save your quiz answers!',
            message: 'There was an error on our end, please try again later.',
            duration: 6000,
          });
        })
        .finally((response) => {
          this.$emit('loadingChange', false);
        });
    },
  },
};
</script>

<style scoped>
  .quiz .quiz-questions, .quiz-results {
    
    height: 340pt;
    overflow-y: scroll;
  }
  .quiz-header {
    display: grid;
    grid-template-areas: 'title actions';
    grid-template-columns: 1fr 1fr;
  }
  .quiz-header > .title { grid-area: title; }
  .quiz-header > .actions { grid-area: actions; }
  .quiz {
  }
  .actions button {
    float: right;
    margin-left: 8pt;
  }
  .question {
    margin-top: 8pt;
  }
  .question > p {
    margin: 0pt;
    margin-bottom: 3pt;
  }
  .answers-list > .answer {
    padding-left: 8pt;
    padding-bottom: 3pt;
  }
</style>
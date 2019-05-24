<template>
  <!-- QuizResults.vue
    This is the view of a quiz which shows whether or not you got questions on
    the quiz right or wrong.

    You can be jumped to this screen automatically if you have already taken the given quiz 
    or after you press submit when taking a quiz.
   -->
  <div class="quiz">
    <div class="quiz-header">
      <h2 class="title">Quiz</h2>
      <div class="actions">
        <button class="btn btn-plain"
          @click="changeContext('quiz')" v-if="notViewingAsStudent">Try again</button>
        <button class="btn btn-plain" v-if="role === 'professor' && notViewingAsStudent"
          @click="changeContext('quizEditor')">Edit</button>
      </div>
    </div>
    <ol class="quiz-results">
      <p>Results</p>
      <li v-for="question in questions"
        :key="`quiz-result-${question.pk}`"
        class="question">

        <p>{{ question.text }}</p>

        <ol type="a" class="answers-list">
          <li v-for="(answer, index) in question.answers"
            :key="`quiz-result-${question.uuid}-answer-${index}`"
            class="answer">

            <input disabled type="radio"
              :checked="isTheChosenAnswer(question, answer)"
              :id="answer.uuid" 
              :value="answer.uuid" >

            <label :for="answer.uuid">
              {{ answer.text }}
              <span v-if="isTheChosenAnswer(question, answer)">

                <sui-icon v-if="chosenAnswers[question.pk].correct"
                  name="check" style="color: var(--color-green)"/>
                <sui-icon v-else
                  name="close icon" style="color: var(--color-red)"/>

              </span>
            </label>
          </li>
        </ol>
      </li>
    </ol>
  </div>
</template>

<script>
import axios from 'axios';
import LoadingLayer from '@/components/LoadingLayer';
import { API_URL } from '@/constants';

export default {
  components: {
    LoadingLayer,
  },
  props: {
    role: {
      type: String,
    },
    studentQuizData: {
      type: Object,
      required: true,
    },
    topicId: {
      type: Number,
      required: true,
    }
  },
  data() {
    return {
      questions: [],
      chosenAnswers: {},
    };
  },
  computed: {
    notViewingAsStudent() {
      return !this.$route.query || !this.$route.query.viewAs;
    },
  },
  created() {
    const answers = {};

    this.studentQuizData.student_answers.forEach((answer) => {
      answers[answer.question] = answer;
    });

    this.chosenAnswers = answers;
    this.questions = this.studentQuizData.quiz.questions;
  },
  methods: {
    changeContext(context) {
      this.$emit('contextChange', context);
    },
    // Small helper method that conditionally renders the check or 'x' mark only
    // if the given question was the one the user chose
    isTheChosenAnswer(question, answer) {
      const questionId = question.pk;
      if (this.chosenAnswers && this.chosenAnswers[question.pk]) {
        const chosenAnswer = this.chosenAnswers[question.pk].answer;

        return answer.pk === chosenAnswer;
      }
      
      return false;
    }
  },
};
</script>

<style>
  .quiz-results {
    height: 340pt;
    overflow-y: scroll;
  }
</style>
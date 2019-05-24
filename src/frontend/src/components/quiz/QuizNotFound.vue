<template>
  <!-- QuizNotFound.vue
    Pretty straightforward, if we couldn't find the quiz in the db, we show this component.

    If the user is a professor, it gives them the option to add a quiz
   -->
  <div class="quiz">
    <div class="quiz-header">
      <h2 class="title">No quiz yet</h2>
      <div class="actions">
        <button class="btn btn-create"
          @click="changeContext('quizCreater')" v-if="role === 'professor'">Add quiz</button>
      </div>
    </div>

    <h1>No Quiz for this topic yet</h1>

  </div>
</template>

<script>
import axios from 'axios';
import { mapMutations } from 'vuex';
import CreateQuiz from '@/components/quiz/CreateQuiz';
import LoadingLayer from '@/components/LoadingLayer';
import QuizQuestions from '@/components/quiz/QuizQuestions';
import QuizResults from '@/components/quiz/QuizResults';
import { API_URL } from '@/constants';

export default {
  components: {
    CreateQuiz,
    LoadingLayer,
    QuizQuestions,
    QuizResults,
  },
  props: {
    role: {
      type: String,
      default: 'student',
    }
  },
  methods: {
    changeContext(context) {
      this.$emit('contextChange', context);
    },
  },
};
</script>

<style scoped>
  h1 {
    text-align: center;
    margin-top: 25%;
  }
</style>